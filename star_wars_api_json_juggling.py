import re
import requests
import json
import csv

SWAPI_PEOPLE = 'https://swapi.co/api/people/'
SWAPI_PLANETS = 'https://swapi.co/api/planets/'
all_people_list = []
all_planets_list = []


def parse_intermediate_result(raw_data, target, parsing_type):
    if parsing_type == 'person':
        for person in raw_data['results']:
            target.append((
                person['name'],
                person['height'],
                re.findall('\d{1,2}', person['homeworld'])[0],
                person['gender']))
    elif parsing_type == 'planet':
        for planet in raw_data['results']:
            target.append((
                planet['name'],
                planet['climate'],
                planet['population'],
                re.findall('\d{1,2}', planet['url'])[0]))
    else:
        raise NotImplementedError


def get_data(source, target_loc, target_type):
    data = requests.get(source).json()
    parse_intermediate_result(raw_data=data, target=target_loc, parsing_type=target_type)

    while data['next'] is not None:
        next_page = data['next']
        data = requests.get(next_page).json()
        parse_intermediate_result(raw_data=data, target=target_loc, parsing_type=target_type)


def save_data_to_csv(filename, data_headers, data_values):
    with open(filename, mode='w', encoding='utf-8', newline='') as people_file:
        people_writer = csv.writer(people_file)
        people_writer.writerow(data_headers)
        people_writer.writerows(data_values)


def merge_into_json(planets, people):
    output = {'planets': []}

    with open(planets, mode='r', encoding='utf-8', newline='') as planets_data:
        planets_reader = csv.reader(planets_data)
        planets = [x for x in planets_reader][1:]

    for planet in planets:
        output['planets'].append({
            'name': planet[0],
            'climate': planet[1],
            'population': planet[2],
            '_temp_id': planet[3],
            'residents': []
        })

    with open(people, mode='r', encoding='utf-8', newline='') as people_data:
        people_reader = csv.reader(people_data)
        people = [x for x in people_reader][1:]

    for person in people:
        for planet in output['planets']:
            if person[2] == planet['_temp_id']:
                planet['residents'].append({'name': person[0], 'height': person[1], 'gender': person[3]})
                break

    for planet in output['planets']:
        del planet['_temp_id']

    with open('star.json', mode='w', encoding='utf-8') as output_file:
        json.dump(output, output_file, indent=2, ensure_ascii=False)


get_data(source=SWAPI_PEOPLE, target_loc=all_people_list, target_type='person')
get_data(source=SWAPI_PLANETS, target_loc=all_planets_list, target_type='planet')

save_data_to_csv('people.csv', ['name', 'height', 'planet_id', 'gender'], all_people_list)
save_data_to_csv('planets.csv', ['name', 'climate', 'population', 'planet_id'], all_planets_list)

merge_into_json('planets.csv', 'people.csv')
