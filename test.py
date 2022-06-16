import requests

"""url = 'http://127.0.0.1:8000/load_image/date_id/2'
file = {"file": open('2.png', 'rb')}
resp = requests.post(url=url, files=file)
print(resp.text)"""

url = 'http://127.0.0.1:8000/add_date/uid/12355123145'
resp = requests.post(url=url, json={
    'date': '22.01.2022', 'title': 'Абоба', 'description': 'ыпывпывпыпывп'
})
img_url = 'http://127.0.0.1:8000/load_image/uid/12355123145/date_id/' + str(resp.json()['id'])
file = {'file': open('2.png', 'rb')}
img_resp = requests.post(url=img_url, files=file)
print(resp.text, img_resp.text)