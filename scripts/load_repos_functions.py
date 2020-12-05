import configparser
import os
import subprocess
import json
import requests


from dbOperations import con, db, app, config, ALLOWED_EXTENSIONS, ALLOWED_ARCHIVES, addOneFile, addManyFiles, addManyFilesByList
from flask import request, jsonify



def get_org_settings():
    
    with open(os.path.join(os.getcwd(), "..", "scripts", "org_download_settings.json"), "r") as read_file:
        settings = json.load(read_file)
    return settings


def find_files(catalog):
    find_files = []
    files_to_add = []
    for root, dirs, files in os.walk(catalog):
        find_files += [os.path.join(root, name) for name in files if not name.endswith(tuple(ALLOWED_EXTENSIONS))]
        files_to_add += [os.path.join(root, name) for name in files if name.endswith(tuple(ALLOWED_EXTENSIONS))]
    print(files_to_add)
    return (find_files, files_to_add)

@app.route('/load_repo', methods=['GET'])
def load_repo():
    url = request.form['url']
    repo_full_name = url.replace("https://github.com/", "").replace(".git", "")
    if check_repo_exist(repo_full_name):
        subprocess.run(["git", "clone", url, os.path.join(app.config['UPLOAD_FOLDER'], repo_full_name)])
        finded_files = find_files(os.path.join(app.config['UPLOAD_FOLDER'], repo_full_name))
        #for path in finded_files[0]:
            #os.remove(path) ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        addManyFilesByList(finded_files[1], repo_full_name)
        return jsonify({"ok":"ok"})
    else:
        # такого репозитория нет, сообщить об этом пользователю
        print('git repositories is incorrect')
        return jsonify({"error": "git repositories is incorrect"})


def load_repo_from_org(repo_full_name, path):
    settings = get_org_settings()
    subprocess.run(["git", "clone", "https://" + settings['login'] + ":" + settings[
        'token'] + "@github.com/" + repo_full_name + ".git", os.path.normpath(path + '/' + repo_full_name)])
    finded_files = find_files(os.path.normpath(path + '/' + repo_full_name))
    #for path in finded_files[0]:
        #os.remove(path) ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    addManyFilesByList(finded_files[1], repo_full_name)

@app.route('/load_repos_from_org', methods=['GET'])
def load_repos_from_org():
    repo_full_names = request.form.getlist('url')
    for repo_full_name in repo_full_names:
        load_repo_from_org(repo_full_name, app.config['UPLOAD_FOLDER'])
    return jsonify({"ok":"ok"})


def get_all_repos_from_org():
    settings = get_org_settings()
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token ' + settings['token']
    }
    response = requests.get('https://api.github.com/orgs/' + settings['organization'] + '/repos', headers=headers)
    repositories = json.loads(response.content)
    repos_full_names = []
    for repo in repositories:
        repos_full_names.append(repo['full_name'])
    return repos_full_names

@app.route('/update_org_settings', methods=['POST'])
def update_org_settings():
    login = request.form['login']
    token = request.form['token']
    organization = request.form['organization']
    if check_org_settings(login, token, organization):
        settings = get_org_settings()
        settings['login'] = login
        settings['token'] = token
        settings['organization'] = organization
        with open(os.path.join(os.getcwd(), "..", "scripts", "org_download_settings.json"), 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        return jsonify({"ok":"ok"})
    else:
        # данные организации неверны, сообщить об этом пользователю
        print('Org data is incorrect')
        return jsonify({"error": "Org data is incorrect"})


def check_repo_exist(repo_full_name):
    return "id" in requests.get('https://api.github.com/repos/' + repo_full_name).content.decode()


def check_org_settings(login, token, organization):
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token ' + token
    }
    user_response = requests.get('https://api.github.com/user', headers=headers)
    org_response = requests.get('https://api.github.com/orgs/' + organization, headers=headers)

    if "login" in user_response.content.decode() and "login" in org_response.content.decode():
        user = json.loads(user_response.content)
        if user['login'] == login:
            # логин совпал
            return True
        else:
            # логин не совпал
            return False
    else:
        # токен не действителен
        return False

####Неактуально
# load_repo("https://github.com/Heliconter/floyd-warshall-visualizer", "some path")

# load_repos_from_org(
#     ['Artex-Test-Organization/Test-Repository-A-Private', 'Artex-Test-Organization/Test-Repository-B-Public',
#      'Artex-Test-Organization/Test-Repository-C-Public'], "some path")

# update_org_settings("AlexRyzhickov", "fb464859ebc0740b7f841f2cd950c47d6f7ca627", "Artex-Test-Organization")
