"""
 :mod:`helpers` Fedora Batch App Helpers
"""
__author__ = "Jeremy Nelson"

import forms
import mimetypes
import os
import requests
import shutil
import urllib.parse
import xml.etree.ElementTree as etree

from jinja2 import Environment, FileSystemLoader


JINJA_ENV = Environment(loader=FileSystemLoader(
    os.path.dirname(os.path.abspath(__file__))))

DEFAULT_NS = {
    "fedora_manage": "http://www.fedora.info/definitions/1/0/management/",
    "mods": 'http://www.loc.gov/mods/v3'}

def create_mods(form):
    """Creates a MODS xml document based on form values

    Args:
        form(flask.request.form): Form
    
    Returns:
        str: Raw XML string of MODS document
    """ 
    mods_context = {'dateCreated': [],
        'digital_origin': form.get('digital_origin'),
                      'contributors': [],
                      'corporate_contributors': [],
                      'creators': [],
                      'corporate_creators': [],
                      'genre': form.get('genre'),
                      'organizations': [],
                      'schema_type': 'CreativeWork', # Default,
                      'subject_people': [],
                      'subject_places': [],
                      'subject_topics': [],
                      'title': form.get('title')
                      }
    for row in form.getlist('creators'):
        mods_context['creators'].append(row)
    for row in form.getlist('corporate_creators'):
        mods_context['corporate_creators'].append(row)
    for row in form.getlist('contributors'):
        mods_context['contributors'].append(row)
    for row in form.getlist('corporate_contributors'):
        mods_context['corporate_contributors'].append(row)
    for row in form.getlist('subject_people'):
        mods_context['subject_people'].append(row)
    for row in form.getlist('organizations'):
        mods_context['organizations'].append(row)
    for row in form.getlist('subject_people'):
        mods_context['subject_people'].append(row)
    for row in form.getlist('subject_topics'):
        mods_context['subject_topics'].append(row)
    if len(form.get('genre')) > 0:
        mods_context['genre'] = form.get('genre')
    #if len(admin_note) > 0:
    #    mods_context['admin_note'] = admin_note
    #description = add_obj_template_form.cleaned_data[
    #      'description']
    #if len(description) > 0:
    #    mods_context['description'] = description
    #alt_title = add_obj_template_form.cleaned_data[
    #      'alt_title']
    #if len(alt_title) > 0:
    #    mods_context['alt_title'] = alt_title
    #rights_holder = add_obj_template_form.cleaned_data[
    #      'rights_holder']
    #if len(rights_holder) > 0:
    #    mods_context['rights_statement'] = rights_holder
    #collection_pid = add_obj_template_form.cleaned_data[
    #      'collection_pid']
    #number_stub_recs = add_obj_template_form.cleaned_data[
    #      'number_objects']
    #mods_context['form'] = add_obj_template_form.cleaned_data['form']
    #mods_context['typeOfResource'] = add_obj_template_form.cleaned_data[
    #      'type_of_resource']
    #for row in forms.DIGITAL_ORIGIN:
    #    if row[0] == int(digital_origin_id):
    #        mods_context['digitalOrigin'] = row[1]
    mods_context['language'] = 'English'
    mods_context['publication_place'] = forms.PUBLICATION_PLACE
    mods_context['publisher'] = forms.PUBLISHER
    if len(form.get('extent')) > 0:
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

def __new_pid__():
    pid_result = requests.post(
        "{0}nextPID?format=xml&namespace=coccc".format(app.config.get('FEDORA_URL')),
         auth=app.config.get('FEDORA_AUTH'))
    if pid_result.status_code > 399:
        raise ValueError("Could not retrieve nextPID, HTTP Code {}".format(
            pid_result.status_code))
    pid_doc = etree.XML(pid_result.text)
    pid = pid_doc.find("fedora_manage:pid", DEFAULT_NS)
    if pid is not None:
        return pid.text

def create_stubs(mods_xml,
                 title,
                 parent_pid,
                 num_objects,
                 content_model='compoundCModel'):
    """Function creates 1-n number of basic Fedora Objects in a repository

    Parameters:
    mods_xml -- MODS XML used for all stub MODS datastreams
    title -- Title of Fedora Object
    parent_pid -- PID of Parent collection
    num_objects -- Number of stub records to create in the parent collection
    content_model -- Content model for the stub records, defaults to
                     compound object
    """
    auth = app.config.get('FEDORA_AUTH')
    for i in range(0, int(num_objects)):
        new_pid = __new_pid__()
        # Add a label to new PID using the title
        params = urllib.parse.urlencode({"label": title})
        add_label_url = "{0}{1}?{2}".format(
            app.config.get('FEDORA_URL'),
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
            app.config.get('FEDORA_URL'),
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
                            'parent_pid':parent_pid}
        rels_ext = rels_ext_template.render(**rels_ext_context)
        params = urllib.parse.urlencode({
            "controlGroup": "M",
            "dsLabel": "RELS-EXT",
            "mimeType": "application/rdf+xml"})
        rels_url = "{0}{1}/datastreams/RELS-EXT?{2}".format(
            app.config.get('FEDORA_URL'),
            new_pid,
            params)
        rels_result = requests.post(rels_url,
            data=rels_ext,
            auth=auth)
    return True


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


# SPARQL Queries
NEWEST_SPARQL = """SELECT DISTINCT ?s ?date
WHERE {{ ?s <fedora-model:createdDate> ?date . }}
ORDER BY DESC(?date)
LIMIT 100
OFFSET {0}"""

from app import app
