import os
import sys
import subprocess
import json

with open("org_download_settings.json", "r") as read_file:
    settings = json.load(read_file)

with open("files_types.json", "r") as read_file:
    files_types = json.load(read_file)

subprocess.run(["git", "clone", "https://" + settings['login'] + ":" + settings[
    'token'] + "@github.com/" + sys.argv[1] +".git", sys.argv[2]])


def find_files(catalog):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        find_files += [os.path.join(root, name) for name in files if not name.endswith(tuple(files_types))]
    return find_files


for path in find_files(sys.argv[2]):
    # print(path)
    os.remove(path)
