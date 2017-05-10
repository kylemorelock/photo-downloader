"""
Script to download and organize files from URLs recorded from Google Scholar profiles.
The files are renamed to indicate they came from Google Scholar.
"""

import json
import logging
import os
import pymongo
import url_download as ud

from datetime import datetime

print("url_download namespace:")
print(dir(ud))

script_path = os.path.realpath(__file__)
project_path = os.path.realpath(os.path.join(script_path, os.pardir, os.pardir))
# csv_path = os.path.realpath(os.path.join(project_path, 'files', 'bios_scided.csv - bios_scided.csv.csv'))
env_vars_path = os.path.abspath(os.path.join(project_path, os.pardir, "config", 'env.json'))

with open(env_vars_path) as env_json_file:
    env = json.load(env_json_file)

client = pymongo.MongoClient(env["db_uri"])
db = client[env["db_name"]]

repo_path = os.path.realpath(os.path.join(project_path, 'gs_photos'))
log_file_name = 'gs_images_' + datetime.now().strftime('%Y%m%s') + '.log'
log_path = os.path.realpath(os.path.join(project_path, 'log', log_file_name))

logging.basicConfig(level=logging.DEBUG, filename=log_path)
logger = logging.getLogger('url_download')

cursor = db.gs_profiles.find({})

ext = "jpg"
gs_base_url = "https://scholar.google.com/"

for doc in cursor:
    if ud.is_valid_string(doc['gs_image_url']) and \
        doc['gs_image_url'] != "/citations/images/avatar_scholar_150.jpg":
        file_name = ud.construct_file_name(ext, "gs", doc["scid"])
        path = ud.construct_file_path(repo_path, doc["scid"], file_name)
        image_url = doc['gs_image_url'].replace("view_photo", "medium_photo")
        # logger.debug(path)
        url = "{}{}".format(gs_base_url, image_url)
        ud.download_file(url, path, logger=logger)
