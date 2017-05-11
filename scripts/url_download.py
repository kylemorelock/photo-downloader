"""
Script to download and organize files from a csv file. The csv file has a column containing
urls to the images and scids.
"""

import csv, logging, os, shutil, urllib.request
from datetime import datetime

def construct_file_name(ext, *args):
    """
    Acquire the extension as the first argument, and use *args in order to create the file name
    """
    file_name = '_'.join(args) + '.' + ext
    return file_name

def construct_file_name_from_row(row):
    #data to be used to construct the filename
    row_fields = ['scid', 'department_abbr']
    file_name_parts = []

    for field in row_fields:
        if is_valid_string(row[field]):
            file_name_parts.append(row[field])
        else:
            file_name_parts.append('unk')

    #extension string checking
    ext = row['photo_format']

    return construct_file_name(ext, *file_name_parts)

def construct_file_path(*args):
    """
    Obtain the full file path with *args as strings naming the directories (the last
    is the file name). If the directory path doesn't exist, create it.
    """
    full_path = os.path.realpath(os.path.join(*args))
    dir_path = os.path.dirname(full_path)
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    return full_path

def construct_file_path_from_row(row, base_path, file_name, logger=None):
    #file repo path
    #constructs the path based on the scid. If scid is not found, name_seperated_underscore is used
    if is_valid_string(row['scid']):
        user = row['scid']
    else:
        user = 'name_seperated_underscore'
        logger.info("Path has no scid for " + user + " from source " + row['photo_URL'])

    return construct_file_path(base_path, user, file_name)

def download_file(source, dest, logger=None):
    """
    Retrieve response data from a URL as a file object, open a new file,
    and copy the contents of the response f.o. into the new file.
    """
    if os.path.exists(dest):
        logger.info('File already exists. From: ' + source + 'In: ' + dest)
    try:
        with urllib.request.urlopen(source) as response, open(dest, 'wb') as file_obj:
            shutil.copyfileobj(response,file_obj)
            logger.debug('Downloaded {} to {}'.format(source, dest))
    except TimeoutError:
        logger.error('Timeout:' + source)
    except urllib.error.URLError:
        logger.error('URLError(Timeout):' + source)
    except Exception as e:
        logger.error('Exception:' + source + 'and' + dest)
        logger.error(e)

def is_valid_string(input_str):
    return isinstance(input_str, str) and len(input_str) > 0 and input_str not in ["http://isri.cmu.edu/images/people/75px/_blank-75.jpg"]

def main():
    #this script's path

    script_path = os.path.realpath(__file__)
    project_path = os.path.realpath(os.path.join(script_path, os.pardir, os.pardir))
    csv_path = os.path.realpath(os.path.join(project_path, 'files', 'bios_scided.csv - bios_scided.csv.csv'))

    repo_path = os.path.realpath(os.path.join(project_path, 'faculty_photos'))
    log_file_name = 'url_dl_' + datetime.now().strftime('%Y%m%s') + '.log'
    log_path = os.path.realpath(os.path.join(project_path, 'log', log_file_name))

    logging.basicConfig(level=logging.DEBUG, filename=log_path)
    logger = logging.getLogger('url_download')

    with open(csv_path) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if is_valid_string(row['photo_URL']):
                file_name = construct_file_name_from_row(row)
                path = construct_file_path_from_row(row, repo_path, file_name)
                download_file(row['photo_URL'], path, logger=logger)

if __name__ == "__main__":
    main()
