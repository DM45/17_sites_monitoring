import requests
import whois
import datetime
import os
from requests.exceptions import ConnectionError


def get_current_date_plus_month():
    delta_time_month = 1
    current_data = datetime.datetime.today()
    delta_year = current_data.year
    delta_month = current_data.month + delta_time_month
    delta_day = current_data.day
    delta_date = datetime.datetime(delta_year, delta_month, delta_day)
    return delta_date


def load_urls4check(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        urls_list = file_handler.read().splitlines()
    return urls_list


def get_server_respond(urls_list):
    respond_urls_list = {}
    respond_200 = 200
    for url in urls_list:
        try:
            request_info = requests.get(url)
            respond_200_check = request_info.status_code
            if respond_200_check == respond_200:
                respond_urls_list[url] = 'Respond is 200'
            else:
                respond_urls_list[url] = 'Respond is not 200'
        except ConnectionError:
            respond_urls_list[url] = 'Cant get answer for respond 200 check'
    return respond_urls_list


def get_domain_expiration_check(urls_list, delta_time):
    expiration_urls_list = {}
    for_untypical_expiration_date = 0
    for url in urls_list:
        expiration_date = whois.whois(url).expiration_date
        if type(expiration_date) == list:
            expiration_date = expiration_date[for_untypical_expiration_date]
        try:
            if expiration_date > delta_time:
                expiration_urls_list[url] = 'Expiration check passed'
            else:
                expiration_urls_list[url] = 'Expiration check not passed'
        except TypeError:
            expiration_urls_list[url] = 'Cant pass expiration check'
    return expiration_urls_list


def get_merged_status_dict(urls_list, respond_200_dict, expiration_check_dict):
    status_dict = {}
    for url in urls_list:
        status_dict[url] = (
            respond_200_dict.get(url),
            expiration_check_dict.get(url)
            )
    return status_dict


if __name__ == '__main__':
    urls_filepath = input('Enter filepath to file with urls: ')
    delta_time = get_current_date_plus_month()
    load_urls4check = load_urls4check(urls_filepath)
    if load_urls4check:
        print('Please wait...')
        server_respond_with_200 = get_server_respond(load_urls4check)
        domain_expiration_check = get_domain_expiration_check(
                load_urls4check,
                delta_time
                )
        merged_status_dict = get_merged_status_dict(
                load_urls4check,
                server_respond_with_200,
                domain_expiration_check
                )
        for url, url_status in merged_status_dict.items():
            print(url, url_status[0], url_status[1])
    else:
        print('Wrong filepath')


