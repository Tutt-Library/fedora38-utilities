"""Module repairs errors with MODS metadata"""
__author__ = "Jeremy Nelson, Sarah Bogard"

import datetime
import os
import requests
import sys
import zipfile

import xml.etree.ElementTree as etree
import rdflib
import urllib.parse

MODS = rdflib.Namespace("http://www.loc.gov/mods/v3")
etree.register_namespace("mods", str(MODS))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

class RepairMODSError(Exception):

    def __init__(self, pid, message):
        self.pid = pid
        self.message = message

    def __str__(self):
        return "Error with {}'s MODS\n{}".format(self.pid, self.message)

def update_mods(**kwargs):
    """Function takes pid, field, and old_value, replaces with
	a new_value.

    Args:
        pid -- 
		field_xpath -- 
		old_value -- 
		new_value --
    """
    app = kwargs.get('app')
    pid = kwargs.get("pid")
    field_xpath = kwargs.get("xpath") 
    old_value = kwargs.get("old")
    new_value = kwargs.get("new")
    start = datetime.datetime.utcnow()
    rest_url = kwargs.get("rest_url", app.config.get("FEDORA_URL"))
    auth = kwargs.get("auth", app.config.get("FEDORA_AUTH"))
    backup = kwargs.get("backup", False)
    mods_base_url = "{}{}/datastreams/MODS".format(
        rest_url,
        pid)
    get_mods_url = "{}/content".format(mods_base_url)
    mods_result = requests.get(
        get_mods_url,
        auth=auth)
    if mods_result.status_code > 399:
        err_title = """"Failed to replace {} with {} for PID {}, 
error={} url={}""".format(
            old_value, 
            new_value, 
            pid,
            mods_result.status_code,
            mods_url)
    raw_xml = mods_result.text
    mods_xml = etree.XML(raw_xml)
    # Create backup of MODS
    if backup is True:
        backup_filename = "{}-mods-{}.xml".format(
            pid, 
	    start.strftime("%Y-%m-%d")).replace(":", "_")
        backup_mods_filepath = os.path.join(
            BASE_DIR, 
            "repair",
            "backups",
            backup_filename)
        if not os.path.exists(backup_mods_filepath):
            with open(backup_mods_filepath, "wb+") as mods_file:
                mods_file.write(raw_xml.encode())
    old_value_elements = mods_xml.findall(field_xpath)
    for element in old_value_elements:
        if element.text == old_value:
            element.text = new_value
    mods_update_url = "{}?{}".format(
        mods_base_url,
        urllib.parse.urlencode({"controlGroup": "M",
            "dsLabel": "MODS",
            "mimeType": "text/xml"}))
    raw_xml = etree.tostring(mods_xml)
    put_result = requests.post(
        mods_update_url,
		files={"content":  raw_xml},
        auth=CONF.FEDORA_AUTH)
    if put_result.status_code < 300:
        return True
    else:
        raise RepairMODSError(
            pid, 
            "Failed to update MODS with PUT\nStatus code {}\n{}".format(
                put_result.status_code,
                put_result.text))

def update_multiple(
    pid_list,
    field_xpath,
    old_value,
    new_value):
    """Function takes a list of PIDs, the MODS field xpath, the old value to be 
    replaced by the new value.

    Args:
        pid_list -- Listing of PIDs
        field_xpath -- Field XPath
        old_value -- Old string value to be replaced
        new_value -- New string value
    """
    start = datetime.datetime.utcnow()
    print("Starting MODS update for {} PIDS at {}".format(
        len(pid_list), 
        start.isoformat()))
    errors = []
    for i, pid in enumerate(pid_list):
        if not update_mods(pid, field_xpath, old_value, new_value):
            print("Could update MODS for PID {}".format(pid))
            errors.append(pid)
        if not i%25:
            print(i, end="")
        elif not i%10:
            print(".", end="")
    end = datetime.datetime.utcnow()
    print("Finished updating MODS for {}, errors {} at {}, total {}".format(
        len(pid_list),
        len(errors),
        end.isoformat(),
        (end-start).seconds / 60.0))