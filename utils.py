import random
import string
import logging
import requests
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


PATH_TO_USED_IPS = 'files/used_ip.txt'
PATH_TO_TRIED_PROXY = 'files/tried_proxy.txt'

def generate_email(domain):
    return ''.join([random.choice(string.ascii_letters) for iter in range(8)]) + \
            str(random.randint(1,5000)) + '@' + domain

def generate_password():
    return ''.join([random.choice(string.ascii_lowercase) for iter in range(5)]) + \
           ''.join([random.choice(string.ascii_uppercase) for iter in range(5)]) + \
           str(random.randint(1,5000))

def _get_used_ip_list(file_with_ips):
    ip_list = list()
    with open(file_with_ips) as ip_file:
        ip_list = ip_file.readlines()
    return [ip.strip() for ip in ip_list]

def _save_ip_to_file(file_name, ip_address):
    with open(file_name, 'a') as ip_file:
        ip_file.write(ip_address + '\n')

def _get_working_proxy(proxies):
    used_ips = _get_used_ip_list(PATH_TO_USED_IPS)
    headers = {'User-Agent': "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0"}
    response = ''
    tried_proxy = _get_used_ip_list(PATH_TO_TRIED_PROXY)
    for proxy in proxies:
        if proxy.ip not in tried_proxy:
            proxy_dict = {
                          "http"  : f"http://{proxy.ip}:{proxy.port}",
                          "https" : f"https://{proxy.ip}:{proxy.port}",
                         }
            try:
                response = requests.get('https://api.ipify.org/',
                                        headers=headers,
                                        proxies=proxy_dict,
                                        timeout=5)
            except:
                _save_ip_to_file(PATH_TO_TRIED_PROXY, proxy.ip)
                print('invalid proxy: ', proxy.ip)
            else:
                current_ip = response.text
                if current_ip not in used_ips:
                    _save_ip_to_file(PATH_TO_USED_IPS, current_ip)
                    return f"{proxy.ip}:{proxy.port}"
    return None

def get_proxy():
    req_proxy = RequestProxy()
    proxies = req_proxy.get_proxy_list()
    return _get_working_proxy(proxies)

def get_logger(log_file, name):
    logger = logging.getLogger(name)
    f_handler = logging.FileHandler(log_file)
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    return logger
