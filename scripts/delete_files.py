import os
import sys
import subprocess

subprocess.run(["git", "clone", sys.argv[1], sys.argv[2]], )


def find_files(catalog):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        find_files += [
            os.path.join(root, name) for name in files
            if not name.endswith(('.c', '.cpp', '.h', '.py', '.java', '.js'))
        ]
    return find_files


for path in find_files(sys.argv[2]):
    # print(path)
    os.remove(path)
