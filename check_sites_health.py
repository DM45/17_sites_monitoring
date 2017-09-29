import requests
import whois
import datetime
import os
from requests.exceptions import ConnectionError


def get_current_date_plus_month():
    delta_time_month = 1
    add_year_value = 1
    ordinal_december = 12
    current_data = datetime.datetime.today()
    if current_data.month == ordinal_december:
        delta_year = current_data.year + add_year_value
    else:
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


def get_servers_respond(urls_list):
    urls_respond_list = []
    for url in urls_list:
        try:
            request_info = requests.get(url)
            server_status = request_info.status_code
            urls_respond_list.append(server_status)
        except ConnectionError:
            urls_respond_list.append(None)
    return urls_respond_list


def format_servers_respond(servers_respond):
    format_respond = []
    respond_200 = 200
    for respond in servers_respond:
        if respond == respond_200:
            format_respond.append('Respond is 200')
        elif respond is None:
            format_respond.append('Cant get answer for respond 200 check')
        else:
            format_respond.append('Respond is not 200')
    return format_respond


def get_domains_expiration(urls_list):
    urls_expiration_list = []
    for_untypical_expiration_date = 0
    for url in urls_list:
        expiration_date = whois.whois(url).expiration_date
        if type(expiration_date) == list:
            expiration_date = expiration_date[for_untypical_expiration_date]
        urls_expiration_list.append(expiration_date)
    return urls_expiration_list


def format_domains_expiration(domains_expiration, delta_time):
    format_expiration = []
    for position in domains_expiration:
        try:
            if position > delta_time:
                format_expiration.append('Expiration check passed')
            else:
                format_expiration.append('Expiration check not passed')
        except TypeError:
            format_expiration.append('Cant pass expiration check')
    return format_expiration


if __name__ == '__main__':
    urls_filepath = input('Enter filepath to file with urls: ')
    delta_time = get_current_date_plus_month()
    load_urls4check = load_urls4check(urls_filepath)
    if load_urls4check:
        print('Please wait...')
        servers_respond = get_servers_respond(load_urls4check)
        domains_expiration = get_domains_expiration(load_urls4check)

        format_servers_respond = format_servers_respond(servers_respond)
        format_domains_expiration = format_domains_expiration(
                domains_expiration, delta_time)

        sites_health = zip(
                load_urls4check, 
                format_servers_respond, 
                format_domains_expiration)
        for site in sites_health:
            print(' '.join(site))
    else:
        print('Wrong filepath')


