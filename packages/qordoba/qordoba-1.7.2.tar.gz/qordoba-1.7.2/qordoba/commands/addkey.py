from __future__ import unicode_literals, print_function

import logging

from qordoba.project import ProjectAPI
from qordoba.languages import get_destination_languages

log = logging.getLogger('qordoba')


"""
The add feature enables developers to upload single keys to project files

"""

def filelist(curdir, config,file_name):
    api = ProjectAPI (config)
    project = api.get_project()

    lang = next(get_destination_languages(project))
    remote_file_pages = list (api.page_search(language_id=lang.id, search_string=file_name))
    list_of_remote_files = list()

    for remote_file in remote_file_pages:
        file_name_ = remote_file.get('url', None)
        version_tag = remote_file.get('version_tag', None)
        page_id = remote_file.get('page_id', None)

        list_of_remote_files.append([file_name_, version_tag, page_id])

    from tabulate import tabulate
    log.info(tabulate(list_of_remote_files, headers=['filename', 'version', 'page_id']))


def addkey_command(curdir, config, key, value, file_id):
    api = ProjectAPI(config)
    status_response = api.status_single_key(file_id, key)
    if not status_response['success']:
        if status_response['error'] == "Key  is pointing to an existing node.":
            log.info("Key already exists.")
        else:
            log.info("You may not be formatting your key correctly for use with Qordoba.")
            log.info("Please see https://dev.qordoba.com/docs/key-reference for key syntax.".format(key))
        log.info("The key could not be added.".format(key))
    else:
        if status_response['success']:
            log.info("Key has been added successfully")
        if not status_response['success']:
            log.info("Key upload failed")

        api.upload_single_key(file_id, key, value)