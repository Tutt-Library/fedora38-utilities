"""
 :mod:`helpers` Fedora Batch App Helpers
"""
__author__ = "Jeremy Nelson"

import datetime
from . import forms
import json
import mimetypes
import os
import requests
import shutil
import urllib.parse
import xml.etree.ElementTree as etree
import xml.dom.minidom
from flask import Response
from jinja2 import Environment, FileSystemLoader
from types import SimpleNamespace

JINJA_ENV = Environment(loader=FileSystemLoader(
    os.path.dirname(os.path.abspath(__file__))))

DEFAULT_NS = {
    "fedora_manage": "http://www.fedora.info/definitions/1/0/management/",
    "mods": 'http://www.loc.gov/mods/v3'}

for key, value in DEFAULT_NS.items():
    etree.register_namespace(key, value)

def __create_name__(mods, name_str, type_, role_str):
    if len(name_str) < 1:
        return
    name = etree.SubElement(mods, 
         "mods:name", 
         attrib={"type": type_})
    name_part = etree.SubElement(name, "mods:namePart")
    name_part.text = name_str
    role = etree.SubElement(name, "mods:role")
    role_term = etree.SubElement(role,
        "mods:roleTerm",
        attrib={"type": "text",
                "authority": "marcrelator"})
    role_term.text = role_str

def __create_origin_info__(form, mods):
    origin_info = etree.SubElement(mods, "mods:originInfo")
    if len(form.date_created.data) > 0:
        date_created = etree.SubElement(origin_info,
            "mods:dateCreated",
            attrib={"keyDate": "yes"})
        date_created.text = form.date_created.data
    if len(form.publisher.data) > 0:
        publisher = etree.SubElement(origin_info,
            "mods:publisher")
        publisher.text = form.publisher.data
    if len(form.publication_place.data) > 0:
        place = etree.SubElement(origin_info,
            "mods:place")
        place_term = etree.SubElement(place,
            "mods:placeTerm")
        place_term.text = form.publication_place.data
    if len(form.frequency.data) > 0:
        frequency = etree.SubElement(origin_info,
            "mods:frequency")
        frequency.text = form.frequency.data

def __create_phy_desc__(form, mods):
    phys_desc = etree.SubElement(mods, "mods:physicalDescription")
    if len(form.form.data) > 0:
        form_bib = etree.SubElement(phys_desc,
            "mods:form")
        form_bib = form.form.data
    if len(form.digital_origin.data) > 0:
        dig_origin = etree.SubElement(phys_desc, "mods:digitalOrigin")
        dig_origin.text = form.digital_origin.data
    

def __create_title__(mods, title_str, type_=None, subtitle=None):
    title_info = etree.SubElement(mods,
        "mods:titleInfo")
    if type_ is not None:
        title_info.attrib["type"] = type_
    title = etree.SubElement(title_info,
        "mods:title")
    title.text = title_str
    if subtitle is not None:
        sub_title = etree.SubElement(title_info,
            "mods:subTitle")
        sub_title.text = subtitle


def build_mods(form):
    """Builds a MODS etree populated on WTform values"""
    mods = etree.XML(
        """<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" />""")
    for row in form.admin_notes.data:
        if len(row) < 1:
            continue
        note = etree.SubElement(mods, 
            "mods:note", 
            attrib={"type": "admin"})
        note.text = row
    if len(form.abstract.data) > 0:
        abstract = etree.SubElement(mods, "mods:abstract")
        abstract.text = form.abstract.data
    if len(form.alt_title.data) > 0:
        __create_title__(mods, form.alt_title.data, "alternate")
    for row in form.creators.data:
        __create_name__(mods, row, "personal", "creator")
    for row in form.contributors.data:
        __create_name__(mods, row, "personal", "contributor")
    for row in form.corporate_contributors.data:
        __create_name__(mods, row, "corporate", "contributor")
    for row in form.corporate_creators.data:
        __create_name__(mods, row, "corporate", "creator")
    __create_origin_info__(form, mods) 
    __create_phy_desc__(form, mods)
    if len(form.title.data) > 0:
        __create_title__(mods, 
            form.title.data, 
            subtitle=form.sub_title.data)
    reparsed = xml.dom.minidom.parseString(
        etree.tostring(mods, "unicode"))
    return reparsed.toprettyxml(encoding='utf-8').decode()

def create_mods(form):
    """Creates a MODS xml document based on form values

    Args:
        form(flask.request.form): Form
    
    Returns:
        str: Raw XML string of MODS document
    """ 
    mods_context = {'dateCreated': form.get('date_created'),
        'digital_origin': form.get('digital_origin'),
                      'contributors': [],
                      'corporate_contributors': [],
                      'creators': [],
                      'corporate_creators': [],
                      'languages': [],
                      'organizations': [],
                      'schema_type': 'CreativeWork', # Default,
                      'subject_dates': [],
                      'subject_people': [],
                      'subject_places': [],
                      'subject_topics': [],
                      'title': form.get('title'),
                      'typeOfResource': []
                      }
    for row in form.getlist('creators'):
        if len(row) > 0:
            mods_context['creators'].append(row)
    for row in form.getlist('corporate_creators'):
        if len(row) > 0:
            mods_context['corporate_creators'].append(row)
    for row in form.getlist('contributors'):
        if len(row) > 0:
            mods_context['contributors'].append(row)
    for row in form.getlist('corporate_contributors'):
        if len(row) > 0:
            mods_context['corporate_contributors'].append(row)
    for row in form.getlist('subject_people'):
        if len(row) > 0:
            mods_context['subject_people'].append(row)
    for row in form.getlist('organizations'):
        if len(row) > 0:
            mods_context['organizations'].append(row)
    for row in form.getlist('subject_places'):
        if len(row) > 0:
            mods_context['subject_places'].append(row)
    for row in form.getlist('subject_dates'):
        if len(row) > 0:
            mods_context['subject_dates'].append(row)

    for row in form.getlist('subject_topics'):
        if not row is None and len(row) > 0:
            mods_context['subject_topics'].append(row)
    type_res = form.getlist("type_of_resources")
    for key in form.keys():
        print("{}={}".format(key, form.get(key)))
    print("Type of Resources {}".format(type_res))
    for row in type_res:
        if len(row) > 0:
            mods_context['typeOfResource'].append(row)
    genre = form.get('genre', '')
    if len(genre) > 0 and not genre.startswith('choose'):
        mods_context['genre'] = genre
    admin_note = form.get('admin_note', '')
    if len(admin_note) > 0:
        mods_context['admin_note'] = admin_note
    description = form.get('description', '')
    if len(description) > 0:
        mods_context['description'] = description
    #alt_title = add_obj_template_form.cleaned_data[
    #      'alt_title']
    #if len(alt_title) > 0:
    #    mods_context['alt_title'] = alt_title
    rights_stmt = form.get('rights_statement', '')
    if len(rights_stmt) > 0:
        mods_context['rights_statement'] = rights_stmt
    mods_context['form'] = form.get('form', '')
    for row in form.getlist("languages"):
        mods_context['languages'].append(row)
    mods_context['publication_place'] = forms.PUBLICATION_PLACE
    mods_context['publisher'] = forms.PUBLISHER
    if len(form.get('extent', '')) > 0:
        mods_context['extent'] = form.get('extent')
    mods_context['subject_topics'] = list(set(mods_context['subject_topics']))
    mods_context['subject_places'] = list(set(
              mods_context['subject_places']))
    mods_xml_template = JINJA_ENV.get_template(
        'templates/fedora_utilities/mods-stub.xml')
    
    mods_xml = mods_xml_template.render(**mods_context)
    return mods_xml

def handle_uploaded_zip(file_request,parent_pid):
    """
    Function takes a compressed file object from the Request
    (should be either a .zip, .tar, .gz, or .tgz), opens
    and extracts contents to a temp upload directory. Iterates
    through and attempts to ingest each folder into the
    repository. Returns a list of status for each
    attempted ingestion.

    :param file_request: File from request
    :param parent_pid: PID of parent collection
    :rtype: List of status from ingesting subfolders
    """
    statuses = []
    zip_filepath = os.path.join(settings.MEDIA_ROOT,file_request.name)
    zip_filename,zip_extension = os.path.splitext(file_request.name)
    zip_destination = open(zip_filepath,"wb")
    for chunk in file_request.chunks():
        zip_destination.write(chunk)
    zip_destination.close()
    if zip_extension == ".zip":
        import zipfile
        new_zip = zipfile.ZipFile(zip_filepath,'r')
    elif [".gz",".tar",".tgz"].count(zip_extension) > 0:
        import tarfile
        new_zip = tarfile.open(zip_filepath)
    else:
        raise ValueError("File {0} in handle_uploaded_zip not recognized".format(zip_filepath))
    zip_contents = os.path.join(settings.MEDIA_ROOT,zip_filename)
    new_zip.extractall(path=zip_contents)
    zip_walker = next(os.walk(zip_contents))[1]
    for folder in zip_walker:
        full_path = os.path.join(zip_contents,folder)
        if os.path.isdir(full_path) and not folder.startswith(".git"):
            statuses.append(ingest_folder(full_path,parent_pid))
        #shutil.rmtree(full_path)
    #os.remove(zip_contents)
    return statuses

def __new_pid__(fedora_url, auth):
    pid_result = requests.post(
        "{0}new?namespace=coccc".format(fedora_url),
         auth=auth)
    if pid_result.status_code > 399:
        raise ValueError("Could not retrieve nextPID, HTTP Code {}".format(
            pid_result.status_code))
    return pid_result.text

def create_stubs(**kwargs):
    """Function creates 1-n number of basic Fedora Objects in a repository

    Keyword args:
    mods_xml -- MODS XML used for all stub MODS datastreams
    title -- Title of Fedora Object
    parent_pid -- PID of Parent collection
    num_objects -- Number of stub records to create in the parent collection
    content_model -- Content model for the stub records, defaults to
                     compound object
    """
    config = kwargs.get("config")
    mods_xml = kwargs.get('mods_xml')
    title = kwargs.get('title')
    parent_pid = kwargs.get('parent_pid') 
    num_objects = kwargs.get('num_objects')
    content_model = kwargs.get("content_model", 'compoundCModel')
    auth = config.get('FEDORA_AUTH')
    pids = []
    for i in range(0, int(num_objects)):
        new_pid = __new_pid__(config.get("REST_URL"), 
            config.get("FEDORA_AUTH"))
        # Add a label to new PID using the title
        params = urllib.parse.urlencode({"label": title})
        add_label_url = "{0}{1}?{2}".format(
            config.get('REST_URL'),
            new_pid,
            params)
        add_label_result = requests.put(add_label_url,
            auth=auth)
        # Adds MODS datastream to the new object
        params = urllib.parse.urlencode({
            "controlGroup": "M",
            "dsLabel": "MODS",
            "mimeType": "text/xml"})
        new_mods_url = "{0}{1}/datastreams/MODS?{2}".format(
            config.get('REST_URL'),
            new_pid,
            params)
        mods_ds_result = requests.post(new_mods_url,
            data=mods_xml,
            auth=auth)
        # Add RELS-EXT datastream
        rels_ext_template = JINJA_ENV.get_template(
            'templates/fedora_utilities/rels-ext.xml')
        rels_ext_context = {'object_pid':new_pid,
                            'content_model':content_model,
                            'collection_pid':parent_pid}
        rels_ext = rels_ext_template.render(**rels_ext_context)
        params = urllib.parse.urlencode({
            "controlGroup": "M",
            "dsLabel": "RELS-EXT",
            "mimeType": "application/rdf+xml"})
        rels_url = "{0}{1}/datastreams/RELS-EXT?{2}".format(
            config.get('REST_URL'),
            new_pid,
            params)
        rels_result = requests.post(rels_url,
            data=rels_ext,
            auth=auth)
        #yield json.dumps(
        pids.append(
            {"pid": new_pid, 
             "completed": datetime.datetime.utcnow().isoformat()})
    return pids

def generate_stubs(**kwargs):
    return create_stubs(**kwargs)

def repository_move(source_pid,collection_pid):
    """
    Helper view function takes a source_pid and collection_pid,
    retrives source_pid RELS-EXT and updates
    fedora:isMemberOfCollection value with new collection_pid

    :param source_pid: Source Fedora Object PID
    :param collection_pid: Collection Fedora Object PID
    """
    ns = {'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
          'fedora':'info:fedora/fedora-system:def/relations-external#'}

    repository = Repository(root=settings.FEDORA_ROOT,
                            username=settings.FEDORA_USER,
                            password=settings.FEDORA_PASSWORD)
    raw_rels_ext = repository.api.getDatastreamDissemination(pid=source_pid,
                                                             dsID='RELS-EXT')
    rels_ext = etree.XML(raw_rels_ext[0])
    collection_of = rels_ext.find('{%s}Description/{%s}isMemberOfCollection' %\
                                  (ns['rdf'],ns['fedora']))
    if collection_of is not None:
        collection_of.attrib['{%s}resource' % ns['rdf']] = "info:fedora/%s" % collection_pid
    repository.api.modifyDatastream(pid=source_pid,
                                    dsID="RELS-EXT",
                                    dsLabel="RELS-EXT",
                                    mimeType="application/rdf+xml",
                                    content=etree.tostring(rels_ext))

def repository_update(pid,mods_snippet):
    """
    Helper function takes a pid and a mods_snippet and either replaces the
    existing mods or adds the mods snippet to the MODS datastream.

    :param pid: PID of Fedora object
    :param mods_snippet: MODS snippet
    """
    pass

def extract_creators(mods_xml):
    """Extracts all creators from a mods_xml file

    Parameters:
    mods_xml -- MODS XML
    """
    creators = []
    names = mods_xml.findall('{{{0}}}name'.format(MODS_NS))
    for name in names:
        creator = None
        role = name.find('{{{0}}}role/{{{0}}}roleTerm'.format(MODS_NS))
        name_parts = name.findall('{{{0}}}namePart'.format(MODS_NS))
        if role is None or role.text != 'creator':
            continue
        for part in name_parts:
            creator = part.text
            creators.append(creator)
    return creators

def extract_title(mods_xml):
    title_entities = []
    titleInfos = mods_xml.findall('{{{0}}}titleInfo'.format(MODS_NS))
    for titleInfo in titleInfos:
        output = {}
        if titleInfo.attrib.get('type')is None:
            # equalvant to MARC 245 $a
            titleValue = titleInfo.find('{{{0}}}title'.format(MODS_NS))
            if titleValue is not None and len(titleValue.text) > 0:
                output['titleValue'] = titleValue.text
                output['label'] = output['titleValue']
            # equalvant to MARC 245 $b
            subtitle = titleInfo.find('{{{0}}}subTitle'.format(MODS_NS))
            if subtitle is not None and len(subtitle.text) > 0:
                output['subtitle'] = subtitle.text
                output['label'] = '{0}: {1}'.format(output.get('label'),
                                                    output['subtitle'])
            # equalivant to MARC 245 $p
            partTitle = titleInfo.find('{{{0}}}partName'.format(MODS_NS))
            if partTitle is not None and len(partTitle.text) > 0:
                output['partTitle'] = partTitle.text
            if len(output) > 0:
                title_entities.append(output)
    return title_entities

def load_edit_form(config, pid):
    mods_url = "{}{}/datastreams/MODS/content".format(
        config.get("REST_URL"),
        pid)
    mods_result = requests.get(mods_url,
        auth=config.get("FEDORA_AUTH"))
    if mods_result.status_code == 404:
        return
    mods_result.encoding = 'utf-8'
    mods_xml = etree.XML(mods_result.text)
    return etree.tostring(mods_xml).decode()

def old_load_edit_form(config, pid):
    mods_url = "{}{}/datastreams/MODS/content".format(
        config.get("REST_URL"),
        pid)
    mods_result = requests.get(mods_url,
        auth=config.get("FEDORA_AUTH"))
    mods_xml = etree.XML(mods_result.text)
    creators, contributors, thesis_advisors = [], [], []
    for name in mods_xml.findall("mods:name[@type='personal']", DEFAULT_NS):
        role = name.find("mods:role/mods:roleTerm", DEFAULT_NS)
        name_part = name.find("mods:namePart", DEFAULT_NS)
        if name_part.text is not None and len(name_part.text) > 0:
            if role.text.startswith("creator"):
                creators.append(name_part.text)
            if role.text.startswith("contributor"):
                contributors.append(name_part.text)
            if role.text.startswith("thesis advisor"):
                thesis_advisors.append(name_part.text)
    corporate_creators, corporate_contributors = [], []
    sponsor, degree_grantor = None, None
    for name in mods_xml.findall("mods:name[@type='corporate']", DEFAULT_NS):
        role = name.find("mods:role/mods:roleTerm", DEFAULT_NS)
        name_part = name.find("mods:namePart", DEFAULT_NS)
        if name_part.text is not None and len(name_part.text) > 0:
            if role.text.startswith("creator"):
                corporate_creators.append(name_part.text)
            if role.text.startswith("contributor"):
                corporate_contributors.append(name_part.text)
            if role.text.startswith("degree grantor"):
                degree_grantor = name_part.text
            if role.text.startswith("sponsor"):
                sponsor = name_part.text
    date_created_val = mods_xml.find("mods:originInfo/mods:dateCreated",
        DEFAULT_NS)
    if date_created_val is None:
        date_created = forms.DateCreatedForm()
    else:
        date_created = forms.DateCreatedForm()
        date_created.process(date=date_created_val.text,
            key_date=date_created_val.attrib.get("keyDate", "no"))
            
    date_issued=mods_xml.find("mods:originInfo/mods:dateIssued",
        DEFAULT_NS)
    if date_issued is None:
        date_issued = forms.DateIssuedForm()
    else:
        date_issued = forms.DateIssuedForm(date=date_issued.text,
            key_date=date_issued.attrib.get("keyDate", "no"))
    type_of_resources = []
    for row in mods_xml.findall("mods:typeOfResource", DEFAULT_NS):
        type_of_resources.append(row.text)
    abstract = mods_xml.find("mods:abstract", DEFAULT_NS)
    admin_notes = []
    for row in mods_xml.findall("mods:note[@type='admin']", DEFAULT_NS):
        admin_notes.append(row.text)
    degree_name, degree_type, thesis_notes = None, None, []
    for row in mods_xml.findall("mods:note[@type='thesis']", DEFAULT_NS):
        display_label = row.get("displayLabel")
        if display_label is None:
            thesis_notes.append(row.text)
        elif "degree name" in display_label.lower():
            degree_name = row.text
        elif "degree type" in display_label.lower():
            degree_type = row.text
    extent = mods_xml.find("mods:physicalDescription/mods:extent", DEFAULT_NS)
    publisher = mods_xml.find("mods:originInfo/mods:publisher", DEFAULT_NS)
    publication_place = mods_xml.find(
        "mods:originInfo/mods:place/mods:placeTerm",
        DEFAULT_NS)
    sub_title = mods_xml.find("mods:titleInfo/mods:subTitle", DEFAULT_NS)
    if sub_title is None:
        sub_title = SimpleNamespace()
        sub_title.text = ""
    subject_topics = []
    for row in mods_xml.findall("mods:subject/mods:topic", DEFAULT_NS):
        subject_topics.append(row.text)
    edit_form = forms.EditFedoraObjectFromTemplate(
        title=mods_xml.find("mods:titleInfo/mods:title", DEFAULT_NS).text,
        sub_title=sub_title.text,
        admin_notes=admin_notes,
        abstract=abstract.text,
        pid=pid,
        creators=creators,
        contributors=contributors,
        degree_grantor=degree_grantor,
        degree_name=degree_name,
        degree_type=degree_type,
        extent=extent.text,
        publisher=publisher.text,
        publication_place=publication_place.text,
        sponsor=sponsor,
        subject_topics=subject_topics,
        thesis_advisors=thesis_advisors,
        thesis_notes=thesis_notes,
        type_of_resources=type_of_resources) 
    return edit_form

def save_mods_xml(config, pid, mods_xml):
    mods_url = "{}{}/datastreams/MODS?versionable=true".format(
        config.get("REST_URL"),
        pid)
    result = requests.put(mods_url,
        data=mods_xml,
        auth=config.get("FEDORA_AUTH"))
    if result.status_code > 399:
        raise ValueError("Failed to save MODS XML for {}".format(pid))
    return True

# SPARQL Queries
NEWEST_SPARQL = """SELECT DISTINCT ?s ?date
WHERE {{ ?s <fedora-model:createdDate> ?date . }}
ORDER BY DESC(?date)
LIMIT 100
OFFSET {0}"""
