import requests
import json

from requests.models import requote_uri

token = "Ch6Kjyxa8FCalykqyZP0TrZlTWsW7.7c6mfN2.0pcFZ2UUM3.AhOl.OhqucywAvroUAzdEh2Sc-lVsBnq2W4InMhzR2dY7WeFmzGuAlGoFkJ5kXgNRRY-Bjv7VJ6SAjv"

# return api response


def api_request(url):
    s = requests.session()
    s.headers.update({
        "Authorization": "Bearer %s" % token,
        "Content-Type": "application/json"
    })

    return s.get(url).json()


def survey_ids():
    page_end = False
    page = 0
    ids = []

    while not page_end:  # loop the survey pages
        page += 1
        url = "https://api.surveymonkey.com/v3/surveys/?page=%s&per_page=50" % (
            page)
        response = api_request(url)
        total_page = round((response['total'] / response['per_page']))

        if 'data' not in response:
            page_end = True

        for key in response['data']:  # append all the ids in list
            ids.append(key['id'])

        if page == total_page:
            page_end = True

    return ids


def write_file(file, text):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(text, f)


def read_file(file):
    f = open(file, 'r', encoding='utf-8')
    return json.loads(f.read())


def responses(survey_id, start_created_at, end_created_at):
    page_end = False
    page = 0
    data = []

    while not page_end:
        page += 1
        url = "https://api.surveymonkey.com/v3/surveys/%s/responses/bulk?page=%s&per_page=50&simple=true&start_created_at=%s&end_created_at=%s" % (
            survey_id, page, start_created_at, end_created_at)
        response = api_request(url)
        total_page = round((response['total'] / response['per_page']))

        print('responses page: %s' % page)

        if 'data' not in response:
            page_end = True
        count = 0
        for key in response['data']:
            count += 1
            print('printing responses... %s\n' % count)
            answers = []
            headings = []

            for val in key['pages']:
                answer = []
                heading = []

                if len(val['questions']):
                    answer = val['questions'][0]['answers'][0]['simple_text']
                    heading = val['questions'][0]['heading']

                answers.append(answer)
                headings.append(heading)

            respondent_id = key['id']
            collector_id = key['collector_id']
            start_date = start_created_at
            end_date = end_created_at
            ip_address = key['ip_address']
            email_address = key['email_address']
            first_name = key['first_name']
            last_name = key['last_name']
            custom_data = key['custom_value']
            response = "" if not answers[0] else answers[0]
            response_answer = "" if not answers[1] else answers[1]
            open_end_response = "" if not answers[2] else answers[2]
            open_ended_response_email = "" if not answers[3] else answers[3]
            heading_response = "" if not headings[0] else headings[0]
            heading_response_answer = "" if not headings[1] else headings[1]
            heading_open_end_response = "" if not headings[2] else headings[2]
            heading_open_ended_response_email = "" if not headings[3] else headings[3]

            data_obj = {
                'respondent_id': respondent_id,
                'collector_id': collector_id,
                'start_date': start_date,
                'end_date': end_date,
                'ip_address': ip_address,
                'email_address': email_address,
                'first_name': first_name,
                'last_name': last_name,
                'custom_data': custom_data,
                'response': response,
                'response_answer': response_answer,
                'open_ended_response': open_end_response,
                'open_ended_response_email': open_ended_response_email,
                'heading_response': heading_response,
                'heading_response_answer': heading_response_answer,
                'heading_open_end_response': heading_open_end_response,
                'heading_open_ended_response_email': heading_open_ended_response_email
            }

            data.append(data_obj)

        if page == total_page or page == 2:
            page_end = True

    return data


def survey_responses():

    response = read_file('survey_ids.txt')

    ids = []
    for key in response['data']:  # append all the ids in list
        ids.append(key['id'])

    # ids = survey_ids()
    data = []
    count = 0
    start_created_at = "2021-06-01"
    end_created_at = "2021-06-05"
    for key in ids:  # loop all the survey ids
        count += 1
        print('survey: %s' % (count))
        result = responses(key, start_created_at, end_created_at)
        data.append(result)
        if count == 2:
            break

    print(json.dumps(data, indent=2))
    write_file('response.json', data)
    print('success...')


survey_responses()
