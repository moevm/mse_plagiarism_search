import configparser
import os
import subprocess
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')
ALLOWED_EXTENSIONS = set(config["allowed_extensions"].keys())


def get_org_settings():
    with open("org_download_settings.json", "r") as read_file:
        settings = json.load(read_file)
    return settings


def find_files(catalog):
    find_files = []
    for root, dirs, files in os.walk(catalog):
        find_files += [os.path.join(root, name) for name in files if not name.endswith(tuple(ALLOWED_EXTENSIONS))]
    return find_files


def load_repo(url, path):
    repo_full_name = url.replace("https://github.com/", "").replace(".git", "")
    if check_repo_exist(repo_full_name):
        subprocess.run(["git", "clone", url, os.path.normpath(path + '/' + repo_full_name)])
        for path in find_files(os.path.normpath(path + '/' + repo_full_name)):
            os.remove(path)
    else:
        # такого репозитория нет, сообщить об этом пользователю
        print('git repositories is incorrect')


def load_repo_from_org(repo_full_name, path):
    settings = get_org_settings()
    subprocess.run(["git", "clone", "https://" + settings['login'] + ":" + settings[
        'token'] + "@github.com/" + repo_full_name + ".git", os.path.normpath(path + '/' + repo_full_name)])

    for path in find_files(os.path.normpath(path + '/' + repo_full_name)):
        os.remove(path)


def load_repos_from_org(repo_full_names, path):
    for repo_full_name in repo_full_names:
        load_repo_from_org(repo_full_name, path)


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


def update_org_settings(login, token, organization):
    if check_org_settings(login, token, organization):
        settings = get_org_settings()
        settings['login'] = login
        settings['token'] = token
        settings['organization'] = organization
        with open('org_download_settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
    else:
        # данные организации неверны, сообщить об этом пользователю
        print('Org data is incorrect')


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


# load_repo("https://github.com/Heliconter/floyd-warshall-visualizer", "some path")

# load_repos_from_org(
#     ['Artex-Test-Organization/Test-Repository-A-Private', 'Artex-Test-Organization/Test-Repository-B-Public',
#      'Artex-Test-Organization/Test-Repository-C-Public'], "some path")

# update_org_settings("AlexRyzhickov", "fb464859ebc0740b7f841f2cd950c47d6f7ca627", "Artex-Test-Organization")
