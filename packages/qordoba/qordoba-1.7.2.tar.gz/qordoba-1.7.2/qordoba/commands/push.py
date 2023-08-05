from __future__ import unicode_literals, print_function

import logging
import os
import threading
from qordoba.commands.utils import ask_question, ask_select_multiple, ask_select
from qordoba.languages import get_source_language, init_language_storage, get_destination_languages
from qordoba.project import ProjectAPI
from qordoba.settings import get_push_pattern, get_project_file_formats, backslash
from qordoba.sources import find_files_by_pattern, validate_path, validate_push_pattern, get_content_type_code, \
    get_mimetype, add_project_file_formats

log = logging.getLogger('qordoba')

slash = backslash()

class FilesNotFound(Exception):
    """
    Files not found
    """

def select_version_tag(file_name, version_tags):
    log.info('File `{}` already exists with tags {}. Please setup new version tag:'
             .format(file_name, ', '.join(version_tags)))

    version_tag = None
    while not version_tag:
        user_tag = ask_question('VersionTag: ')
        if user_tag not in version_tags:
            version_tag = user_tag

    return version_tag


def select_source_columns(columns):
    """
    Ask user to set source columns or reference column for csv/xlsx files.
    :param columns: column list from response
    :return: list of column IDs
    """
    if len(columns) == 1:
        return {
            'source_columns': [columns[0]['id'], ]
        }

    log.info('Please select columns as sources: ')

    reference_columns = None

    format_select = {
        True: '{} (empty)',
        False: '{}'
    }

    columns_all = dict()

    question_list = []
    for ix, column in enumerate(columns, start=1):
        column_name = format_select[column['empty']].format(column['name'])
        column_id = column['id']
        columns_all[column_id] = column_name

        question_list.append((column_id, column_name))

    answers = ask_select_multiple(question_list, 'Set: ')
    source_columns = [column_id for column_id, _ in answers]

    left_columns = set(columns_all.keys()).difference(set(source_columns))
    if left_columns:
        log.info('Please select column as reference: ')

        question_list = [(cid, name) for cid, name in columns_all.items() if cid in left_columns]
        question_list.append((-1, 'Skip'))
        answer_id, _ = ask_select(question_list)

        if answer_id != -1:
            reference_columns = answer_id

    if reference_columns is not None:
        # @todo issue in qordoba API. always add reference_column as source column
        source_columns.append(reference_columns)

    return {
        'reference_columns': reference_columns,
        'source_columns': source_columns
    }


def upload_file(api, path, remote_content_type_codes, file_path, version=None, **kwargs):
    log.info('Uploading {}'.format(path.native_path))

    file_path_name = None
    if file_path:
        file_path_name = 'file_' + str(slash).join(path.path_parts[:-1]) + slash
    file_name = path.unique_name
    content_type_code = get_content_type_code(path, remote_content_type_codes)
    version_tag = version

    with open(path.native_path, 'rb') as f:
        resp = api.upload_anytype_file(f, file_name, file_path_name, content_type_code, mimetype=get_mimetype(content_type_code),
                                       **kwargs)
    log.debug('File `{}` uploaded. Name - `{}`. Adding to the project...'.format(path.native_path, file_name))

    # if resp.get('version_tags') or resp.get('version_tags') == []:
    if resp.get('version_tags', ()):
        if version_tag is None or version_tag == 'None' or version_tag in resp.get('version_tags'):
            version_tag = select_version_tag(file_name, resp.get('version_tags'))

    if resp.get('columns'):
        kwargs.update(select_source_columns(resp.get('columns')))

    resp = api.append_file(resp['upload_id'], file_name, version_tag=version_tag, **kwargs)

    if version:
        log.info('Uploaded {} successfully as {} with version tag `{}`'.format(path.native_path, file_name, version_tag))
    else:
        log.info('Uploaded {} successfully as {}'.format(path.native_path, file_name))



def update_file(api, path, remote_files, version=None):
    file_name = path.unique_name

    log.info('Updating {}'.format(path.unique_name))
    if version:
        remote_file = next((f for f in remote_files if f.get('version_tag', None) == version), None)
        if not remote_file:
            raise FilesNotFound('File {} with version {} not found'.format(file_name, version))
    else:
        remote_file = remote_files[0]

    with open(path.native_path, 'rb') as f:
        resp = api.update_upload_anyType_file(f, file_name, remote_file['page_id'])

    resp = api.apply_upload_file(resp['id'], remote_file['page_id'])

    log.info('Updated {} successfully.'.format(file_name))


def find_directories(pattern, slash):
    directory = pattern.split(slash)
    del directory[-1]
    directory = slash.join(directory) + slash
    directory_list = list()
    directory_list.append(directory)
    directory_listing = [x[0] for x in os.walk(directory)]
    if not directory_listing:
        return directory_list
    return directory_listing

def hello():
    log.info("Waiting for file to upload/update")

def final_push(project, curdir, pattern, api,  update, version, remote_content_type_codes, file_path):
    """"Sleep functionality is waiting to upload each file step by step.
    This will prevent file to overwrite each other if many files are pushed in a very short time frame"""
    source_lang = get_source_language(project)
    lang = next(get_destination_languages(project))
    files = list(find_files_by_pattern(curdir, pattern, source_lang, remote_content_type_codes))

    if len(files) == 0:
        log.info('Files for the given push pattern `{}` do not exists.' .format(pattern))

    for file in files:
        sleep = threading.Timer(0.5, hello)
        sleep.start()

        path = validate_path(curdir, file, source_lang)

        file_name = path.unique_name

        remote_file_pages = list(api.page_search(language_id=lang.id, search_string=file_name))

        if remote_file_pages and update:
            update_file(api, path, remote_file_pages,  version=version)
        else:
            upload_file(api, path, remote_content_type_codes, file_path, version=version)



def push_command(curdir, config, update, file_path=False, version=None, files=()):
    api = ProjectAPI(config)
    project = api.get_project()
    remote_content_type_codes = project['content_type_codes']
    init_language_storage(api)
    add_project_file_formats(get_project_file_formats(config))

    if not files:
        pattern_list = get_push_pattern(config)
        if pattern_list is None:
            log.info("No push pattern found in config. Taking files from current directory")
            files = os.listdir(curdir)
            files = [file for file in files if os.path.isfile(file) and not str(file).startswith(".") and not str(file).startswith("__")]

    if files:
        pattern_list = []
        for file_ in files:
            pattern_list.append(file_)

    for pattern in pattern_list:
        assert len(pattern_list) != 0
        if pattern[-2:] == slash + '*':
            pattern_extension = pattern.split(slash)[-1]
            directory_list = find_directories(pattern, slash)
            for dir_ in directory_list:
                if dir_.endswith(slash):
                    dir_ = dir_ + pattern_extension
                else:
                    dir_ = dir_ + slash + pattern_extension
                final_push(project, curdir, dir_, api,  update, version, remote_content_type_codes, file_path)
        else:
            final_push(project, curdir, pattern, api, update, version, remote_content_type_codes, file_path)