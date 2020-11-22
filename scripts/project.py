# import requests
#
# # response = requests.get('https://api.github.com')
# #
# # print(response.content)
#
#
# response = requests.get('https://github.com/login/oauth/authorize')
#
# print(response.content)



#
# headers = {
#     'Authorization': 'token fb464859ebc0740b7f841f2cd950c47d6f7ca627',
# }
#
# response = requests.get('https://api.github.com/user', headers=headers)
#
# print(response.content)

# settings = json.loads("org_download_settings.json")

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
    print(repo['full_name'])

# orgs/acme/repos?access_token=your_access_token


# "git clone https://AlexRyzhickov:fb464859ebc0740b7f841f2cd950c47d6f7ca627@github.com/Artex-Test-Organization/Test-Repository-A-Private.git"
#
#
# # git clone https://AlexRyzhickov:ab4a75e7bf43b49f63f283fdb972dc031eacd963@github.com/Artex-Test-Organization/Test-Repository-A-Private.git
#
# https://ab4a75e7bf43b49f63f283fdb972dc031eacd963@github.com/AlexRyzhickov/Artex-Test-Organization/Test-Repository-A-Private.git
#
# https://AlexRyzhickov:ab4a75e7bf43b49f63f283fdb972dc031eacd963@github.com/AlexRyzhickov/JavaUniversityProject.git
