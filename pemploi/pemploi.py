import requests
import json
import codecs
import time
import math


def generate_string_to_file(id_x,id_y,n_repeated):
    string = ""
    for i in range(n_repeated):
        string = string + id_x + " " + id_y + " "
    return string


# defining the api-endpoint 
API_ENDPOINT = "https://api.emploi-store.fr/partenaire/offresdemploi/v1/rechercheroffres"


headers = {
"Authorization": "Bearer 855617ab-73a1-4fb1-8398-06bfb5681129",
"Content-Type" : "application/json"
}

# departments in France
departs = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","2A","2B","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95"]

# metiers
metiers = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N"]

# data to be sent to api
data = {}
data['technicalParameters'] = {}
data['technicalParameters']['page'] = 1
data['technicalParameters']['per_page'] = 150
data['technicalParameters']['sort'] = 0
data['criterias'] = {}

ids_offres = []
dicti = {}
num_req = 0
with codecs.open('skills.txt', 'w', encoding='utf-8') as the_file:
    for dep in departs:
        if dep == "50" or dep == "74":
            var = input("Please enter new auth (Bearer xxxx): ")
            headers = {
                "Authorization": str(var),
                "Content-Type": "application/json"
            }
        print("Requesting new jobs in department %s " % dep)
        if 'criterias' not in data:
            data['criterias'] = {}
        data['criterias']['departmentCode'] = dep
        # sending post request and saving response as response object
        if num_req == 3:
            time.sleep(1)
            num_req = 0
        r = requests.post(url = API_ENDPOINT, data = json.dumps(data), headers = headers, timeout=100)
        num_req += 1

        # extracting response text
        content = r.text
        try:
            body = json.loads(content)

            big = False
            if body['technicalParameters']['totalNumber']>1000:
                big = True

            if big:
                for metier in metiers:
                    data['criterias']['largeAreaCode'] = metier
                    if num_req == 3:
                        time.sleep(1)
                        num_req = 0
                    r = requests.post(url=API_ENDPOINT, data=json.dumps(data), headers=headers, timeout=100)
                    num_req += 1
                    content = r.text
                    print("%s  %s" % (metier, content))
                    try:
                        body = json.loads(content)
                        num_pag_max = math.ceil(body['technicalParameters']['totalNumber'] / data['technicalParameters']['per_page'])
                        for i in range(1, num_pag_max):
                            for offre in body['results']:
                                if offre not in ids_offres:
                                    ids_skills = []
                                    ids_offres.extend(offre)
                                    for skill in offre['skills']:
                                        for skill2 in offre['skills']:
                                            if 'skillCode' in skill and 'skillCode' in skill2:
                                                if skill['skillCode'] != skill2['skillCode'] and not ids_skills.__contains__(
                                                        skill2):
                                                    the_file.write(
                                                        generate_string_to_file(skill['skillCode'], skill2['skillCode'], 1))
                                        ids_skills.extend(skill)
                                        if 'skillCode' in skill:
                                            dicti[skill['skillCode']] = skill['skillName']

                            print("%i Page finished" % i)
                    except ValueError:
                        print('Error')


            else:
                data.pop('criterias', None)
                num_pag_max = math.ceil(body['technicalParameters']['totalNumber']/data['technicalParameters']['per_page'])
                for i in range(1, num_pag_max):
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
        except ValueError:
            print('Error')

with codecs.open('dictionaire.txt', 'wb', encoding='utf-8') as the_file:
    for key, value in dicti.items():
        the_file.write(key + " " + value + "\n")

print("%i offerts analysed" % len(list(set(ids_offres))))
print("%i unique skills" % len(dicti))