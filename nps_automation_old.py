import requests
import json

token = "Ch6Kjyxa8FCalykqyZP0TrZlTWsW7.7c6mfN2.0pcFZ2UUM3.AhOl.OhqucywAvroUAzdEh2Sc-lVsBnq2W4InMhzR2dY7WeFmzGuAlGoFkJ5kXgNRRY-Bjv7VJ6SAjv"

# return api response


def api_request(url):
    s = requests.session()
    s.headers.update({
        "Authorization": "Bearer %s" % token,
        "Content-Type": "application/json"
    })

    response = s.get(url)
    return response.json()

# return the survey ids


def survey_ids():
    page_end = False
    page = 0
    list_ids = []
    while not page_end:
        page += 1
        url = "https://api.surveymonkey.com/v3/surveys/?page=%s&per_page=100" % (
            page)
        response = api_request(url)
        result = response['data']
        total_page = round(response['total'] / response['per_page'])
        for key in result:
            list_ids.append(key['id'])

        if page == total_page:
            page_end = True

    return list_ids

# return survey responses based on survey id


def survey_responses():

    ids = survey_ids()
    page = 0

    for key in ids:
        page += 1
        url = "https://api.surveymonkey.com/v3/surveys/%s/responses/bulk?page=%s&per_page=50&status=completed" % (
            key, page)
        response = api_request(url)
        total_page = (response['total'] / response['per_page'])

        if response['data'][0]['collector_id'] == '405375644':
            print('found you collector_id: %s' %
                  (json.dumps(response['data'][0], indent=2)))
            return
        if round(total_page) == page:
            break

    print('No found')


print(survey_responses())
