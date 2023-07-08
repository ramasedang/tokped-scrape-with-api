import requests
import random
import re


def find_key(data, key):
    if isinstance(data, dict):
        if key in data:
            yield data[key]
        for k, v in data.items():
            if isinstance(v, dict):
                for result in find_key(v, key):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in find_key(d, key):
                        yield result
    elif isinstance(data, list):
        for item in data:
            for result in find_key(item, key):
                yield result


def find_value(data, value):
    if isinstance(data, dict):
        for k, v in data.items():
            if v == value:
                yield data
            if isinstance(v, dict):
                for result in find_value(v, value):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in find_value(d, value):
                        yield result
    elif isinstance(data, list):
        for item in data:
            for result in find_value(item, value):
                yield result


def find_dict(data, key_value):
    for item in find_key(data, key_value[0]):
        if item == key_value[1]:
            yield item


def to_int(s):
    numeric_string = re.sub(r"\D", "", s)
    amount = int(numeric_string)
    return amount


def search_key_value(obj, variable):
    for key in obj:
        if isinstance(obj[key], dict):
            result = search_key_value(obj[key], variable)
            if result:
                return result
        elif key == variable:
            return str(obj[key])
    return None


def search_key_value_double(obj, variable, scd_var):
    for key in obj:
        if isinstance(obj[key], dict):
            result = search_key_value_double(obj[key], variable, scd_var)
            if result:
                return result
        elif key == variable and scd_var in obj:
            return str(obj[key])
    return None


def search_key_value_obj(obj, variable):
    for key in obj:
        if key == variable:
            return obj[key]
        if isinstance(obj[key], dict):
            result = search_key_value_obj(obj[key], variable)
            if result:
                return result
    return None


def search_key_value_rgx(obj, regex):
    for key in obj:
        if re.match(regex, key):
            return obj[key]
        if isinstance(obj[key], dict):
            result = search_key_value_rgx(obj[key], regex)
            if result:
                return result
    return None


def random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    ]
    return random.choice(user_agents)


def request_auto_to(config, retry_count=0):
    if retry_count > 3:
        return {}
    try:
        res = requests.request(
            config["method"], config["url"], headers=config["headers"]
        )
        return res
    except requests.exceptions.RequestException:
        print("request timout, retry count", retry_count + 1)
        return request_auto_to(config, retry_count + 1)


import requests
import json


def send_webhook_message(webhook_url, content):
    data = {"content": content}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("Pesan berhasil dikirim ke webhook.")
    else:
        print("Terjadi kesalahan saat mengirim pesan ke webhook.")
