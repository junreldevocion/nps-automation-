import json


def read_file(file):
    f = open(file, 'r', encoding='utf-8')
    return json.loads(f.read())


def write_file(file, text):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(text, f)


def survey_ids():
    json_obj = read_file('survey_ids.txt')

    if 'datas' not in json_obj:
        print('wala')
        return
    else:
        print('naa')
        return

    for key in json_obj['data']:
        print(key['id'])


def responses():
    json_obj = read_file('simple_response.txt')
    data = []
    for key in json_obj['data']:

        # print(key['pages'][0]['questions'][0]['heading'])
        # return     response_answer = key['pages'][1]['questions'][0]['answers'][0]['simple_text']

        answers = []
        headings = []
        for page in key['pages']:

            answer = ''
            heading = ''

            if(len(page['questions']) > 0):
                answer = page['questions'][0]['answers'][0]['simple_text']
                heading = page['questions'][0]['heading']

            answers.append(answer)
            headings.append(heading)

        respondent_id = key['id']
        collector_id = key['collector_id']
        start_date = ""
        end_date = ""
        ip_address = key['ip_address']
        email_address = key['email_address']
        first_name = key['first_name']
        last_name = key['last_name']
        custom_data = key['custom_value']
        response = answers[0]
        response_answer = answers[1]
        open_end_response = answers[2]
        open_ended_response_email = answers[3]
        heading_response = headings[0]
        heading_response_answer = headings[1]
        heading_open_end_response = headings[2]
        heading_open_ended_response_email = headings[3]

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
        # print(json.dumps(data, indent=2))
        data.append(data_obj)
        write_file('write.json', data)
    # print(data)
    print(json.dumps(data, indent=2))


responses()
