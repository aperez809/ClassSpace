import requests
import os
import json

def get_data():
    curr_dir = os.path.dirname(__file__)
    target_path = os.path.join(curr_dir, 'data_files/raw_schedule.json')
    cookie = r"""JSESSIONID=13EE6CD6C78437EB7DEDA8605459F199; _ga=GA1.2.1105893269.1568241142; optimizelyEndUserId=oeu1573612106771r0.6526580846976628; amplitude_id_408774472b1245a7df5814f20e7484d0neu.edu=eyJkZXZpY2VJZCI6IjRmYjU4MzM1LTFlY2MtNGRmZi1hODAxLTk2YzNlZjBlYjVkZVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU3MzYxMjEwNzYyNiwibGFzdEV2ZW50VGltZSI6MTU3MzYxMjEwNzY4NCwiZXZlbnRJZCI6MSwiaWRlbnRpZnlJZCI6NCwic2VxdWVuY2VOdW1iZXIiOjV9; s_pers=%20c19%3Dsd%253Abrowse%253Ajournal%253Ahome%7C1573614109490%3B%20v68%3D1573612307911%7C1573614109511%3B%20v8%3D1573612309573%7C1668220309573%3B%20v8_s%3DFirst%2520Visit%7C1573614109573%3B; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-1712354808%7CMCIDTS%7C18214%7CMCMID%7C87240451365381732263057587544115417146%7CMCAAMLH-1574217109%7C7%7CMCAAMB-1574217109%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1573619509s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1991142991%7CvVersion%7C4.3.0; nubanner-cookie=3709804955.36895.0000; _gid=GA1.2.1505099379.1574996500; _gat_Ellucian=1"""
    temp = []
    page_size = 500

    for i in range(15):
        print(f"Starting Page {i}...")
        req_url = f"https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_term=202030&startDatepicker=&endDatepicker=&pageOffset={page_size * i}&pageMaxSize={page_size}&sortColumn=subjectDescription&sortDirection=asc"

        res = requests.get(req_url, headers={'Cookie': cookie})
        print(res)
        to_dict = json.loads(res.content)
        temp.extend(to_dict['data'])

    with open(target_path, 'w') as f:
        f.write(json.dumps(temp))


def check_dupes():
    curr_dir = os.path.dirname(__file__)
    target_path = os.path.join(curr_dir, 'data_files/raw_schedule.json')
    with open(target_path, 'r') as f:
        to_dict = json.loads(f.read())

    seen = set()
    dupes = []

    for elem in to_dict:
        if elem['id'] in seen:
            dupes.append(elem['id'])
        else:
            seen.add(elem['id'])

    return f"Seen: {len(seen)}, Dupes: {len(dupes)}"

get_data()
print(check_dupes())