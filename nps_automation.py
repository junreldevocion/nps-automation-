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


# return survey responses based on survey id


def survey_responses(survey_id):
    page_end = False
    page = 0
    data = {}
    new_url = "https://api.surveymonkey.com/v3/surveys/307288910/responses/bulk?simple=true&start_created_at=2021-05-01&end_created_at=2021-06-30"
    while not page_end:  # loop the pages of survey responses
        page += 1
        url = "https://api.surveymonkey.com/v3/surveys/%s/responses/bulk?page=%s&per_page=50&simple=true" % (
            survey_id, page)
        response = api_request(url)
        total_page = (response['total'] / response['per_page'])

        for key in response['data']:  # loop for getting the responses

            data = {
                'respondend_id': key['id'],
                'collector_id': key['collector_id'],
                'start_date': '0',
                'end_date': '0',
                'ip_address': key['ip_address'],
                'email_address': key['email_address'],
                'response': '',
                'response_answer': '',
                'open_ended_response': '',
                'open_ended_response_email': ''
            }

            if key['collector_id'] == '406443209':
                print('found you collector_id: %s' %
                      (json.dumps(key, indent=2)))
                page_end = True
                break

        if page == round(total_page) or page_end == True:
            page_end = True

    return True


def nps_automation():
    page_end = False
    page = 0
    while not page_end:  # loop the survey pages
        page += 1
        url = "https://api.surveymonkey.com/v3/surveys/?page=%s&per_page=50" % (
            page)
        response = api_request(url)
        # print(response)
        # break

        result = response['data']
        total_page = (response['total'] / response['per_page'])

        for key in result:  # loop for ids
            response = survey_responses(key['id'])
            if response:
                page_end = True
                break

        if page == round(total_page) or page_end == True:
            page_end = True

    return "exit"


print(nps_automation())
