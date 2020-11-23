import os
import sys
import subprocess
import json

subprocess.run(["git", "clone",sys.argv[1],sys.argv[2]])

with open("files_types.json", "r") as read_file:
    files_types = json.load(read_file)

def find_files(catalog):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        find_files += [os.path.join(root, name) for name in files if not name.endswith(tuple(files_types))]
    return find_files

for path in find_files(sys.argv[2]):
    # print(path)
    os.remove(path)


