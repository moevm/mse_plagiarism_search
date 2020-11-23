import requests
import json

with open("org_download_settings.json", "r") as read_file:
    settings = json.load(read_file)

headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'token ' + settings['token']
}

response = requests.get('https://api.github.com/orgs/' + settings['organization'] + '/repos', headers=headers)
repositories = json.loads(response.content)

for repo in repositories:
    # print(repo['name'])
    print(repo['full_name'])
