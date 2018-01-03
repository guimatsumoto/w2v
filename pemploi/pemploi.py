import requests
import json
import codecs
import time


def generate_string_to_file(id_x,id_y,n_repeated):
    string = ""
    for i in range(n_repeated):
        string = string + id_x + " " + id_y + " "
    return string


# defining the api-endpoint 
API_ENDPOINT = "https://api.emploi-store.fr/partenaire/offresdemploi/v1/rechercheroffres"


headers = {
"Authorization": "Bearer af2ef438-3e7d-4f8d-b700-feb901d90e96",
"Content-Type" : "application/json"
}

# data to be sent to api
data = {}
data['technicalParameters'] = {}
data['technicalParameters']['page'] = 1
data['technicalParameters']['per_page'] = 150
data['technicalParameters']['sort'] = 0

ids_offres = []
dicti = {}
with codecs.open('skills.txt', 'w', encoding='utf-8') as the_file:
    for i in range(1, 8):
        data['technicalParameters']['page'] = i
        print("Requesting new jobs")

        # sending post request and saving response as response object
        r = requests.post(url = API_ENDPOINT, data = json.dumps(data), headers = headers)

        # extracting response text
        content = r.text
        body = json.loads(content)

        if len(body['results']) == 0:
            break

        for offre in body['results']:
            if offre not in ids_offres:
                ids_skills = []
                ids_offres.extend(offre)
                for skill in offre['skills']:
                    for skill2 in offre['skills']:
                        if 'skillCode' in skill and 'skillCode' in skill2:
                            if skill['skillCode'] != skill2['skillCode'] and not ids_skills.__contains__(skill2):
                                the_file.write(generate_string_to_file(skill['skillCode'], skill2['skillCode'], 1))
                    ids_skills.extend(skill)
                    if 'skillCode' in skill:
                        dicti[skill['skillCode']] = skill['skillName']

        print("%i Page finished" % i)
        time.sleep(1)
    data['technicalParameters']['sort'] = 1
    for i in range(1, 8):
        data['technicalParameters']['page'] = i
        print("Requesting new jobs")

        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, data=json.dumps(data), headers=headers)

        # extracting response text
        content = r.text
        body = json.loads(content)

        if len(body['results']) == 0:
            break

        for offre in body['results']:
            if offre not in ids_offres:
                ids_skills = []
                ids_offres.extend(offre)
                for skill in offre['skills']:
                    for skill2 in offre['skills']:
                        if 'skillCode' in skill and 'skillCode' in skill2:
                            if skill['skillCode'] != skill2['skillCode'] and not ids_skills.__contains__(skill2):
                                the_file.write(generate_string_to_file(skill['skillCode'], skill2['skillCode'], 1))
                    ids_skills.extend(skill)
                    if 'skillCode' in skill:
                        dicti[skill['skillCode']] = skill['skillName']

        print("%i Page finished" % i)
        time.sleep(1)
    data['technicalParameters']['sort'] = 2
    for i in range(1, 8):
        data['technicalParameters']['page'] = i
        print("Requesting new jobs")

        # sending post request and saving response as response object
        r = requests.post(url=API_ENDPOINT, data=json.dumps(data), headers=headers)

        # extracting response text
        content = r.text
        body = json.loads(content)

        if len(body['results']) == 0:
            break

        for offre in body['results']:
            if offre not in ids_offres:
                ids_skills = []
                ids_offres.extend(offre)
                for skill in offre['skills']:
                    for skill2 in offre['skills']:
                        if 'skillCode' in skill and 'skillCode' in skill2:
                            if skill['skillCode'] != skill2['skillCode'] and not ids_skills.__contains__(skill2):
                                the_file.write(generate_string_to_file(skill['skillCode'], skill2['skillCode'], 1))
                    ids_skills.extend(skill)
                    if 'skillCode' in skill:
                        dicti[skill['skillCode']] = skill['skillName']

        print("%i Page finished" % i)
        time.sleep(1)

with codecs.open('dictionaire.txt', 'wb', encoding='utf-8') as the_file:
    for key, value in dicti.items():
        the_file.write(key + " " + value + "\n")

print("%i offerts analysed" % len(ids_offres))
print("%i unique skills" % len(dicti))