import glob
import os
import re

script_path = os.path.realpath(__file__)
project_path = os.path.realpath(os.path.join(script_path, os.pardir, os.pardir))
file_path_dir = os.path.realpath(os.path.join(project_path, "gs_photos"))
print(file_path_dir)

glob_list = glob.glob(os.path.join(file_path_dir, "*.jpg"))
print(glob_list[:2])

scid_pattern = re.compile(r'^gs_')

for file_path in glob_list:
    (dir_path, file_name) = os.path.split(file_path)
    scid_ext = file_name.split("_", maxsplit=1)[1]
    scid = scid_ext.rsplit(".")[0]
    new_dir_path = os.path.join(dir_path, scid)

    if not os.path.exists(new_dir_path):
        try:
            os.makedirs(new_dir_path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    new_file_path = os.path.join(new_dir_path, file_name)
    os.rename(file_path, new_file_path)
    print(new_file_path)
