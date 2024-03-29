import concurrent.futures
from typing import Dict

import requests

from service.file_handling import load_data, save_data

# https://developers.lingvolive.com/ru-ru
URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
URL_TRANSLATE = 'https://developers.lingvolive.com/api/v1/Minicard'
KEY = 'YjlkMjk0YTgtZGI3NS00NGE0LWJlNDUtYjkzMDU5Mzc5YTNkOjE2ODE3ZGM4OTI3OTQ4YWE5ZTBlYmJmYTZmMmY5YjZh'  # TODO


def get_word_translation_from_abbyy_api(key: str) -> str:
    headers_auth = {'Authorization': 'Basic ' + KEY}
    auth = requests.post(URL_AUTH, headers=headers_auth)
    if auth.status_code == 200:
        token = auth.text
        headers_translate = {
            'Authorization': 'Bearer ' + token
        }
        params: Dict[str, str] = {
            'text': key,
            'srcLang': '1033',
            'dstLang': '1049'
        }
        req = requests.get(
            URL_TRANSLATE, headers=headers_translate, params=params)
        res = req.json()
        try:
            if res == 'No translations found for text \\"{}\\" among available dictionaries'.format(key):
                translate_error_message = ('Error! -> translate not found')
                return translate_error_message
            else:
                value = res['Translation']['Translation']
                return value
        except TypeError:
            if res == 'Incoming request rate exceeded for 50000 chars per day pricing tier':
                return res
            else:
                return None
    else:
        error_message = ('Error! -> ' + str(auth.status_code))
        return error_message
    return res


def get_duplicates(check_these, check_here) -> list:
    not_translated_words = []
    for key in check_these:
        if key in check_here:
            continue
        else:
            not_translated_words.append(key)
    return not_translated_words


def get_duplicate(check_word, check_here):
    if check_word == "":
        check_word = "Enter word"
        return check_word
    if check_word in check_here:
        translated = check_here.get(check_word)
        return translated
    else:
        translated_word = get_word_translation_from_abbyy_api(check_word)
        if translated_word is None:
            check_here[check_word] = "None"
        if translated_word == "Error! -> translate not found":
            return translated_word
        else:
            check_here[check_word] = translated_word
    return translated_word


def get_translation_with_concurrent_futures(
        word_translation_from_api,
        not_translated_words: list,
        translated_words: dict,
        translated_words_json_file_name) -> dict:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for en, ru in zip(
                not_translated_words,
                executor.map(
                    word_translation_from_api,
                    not_translated_words)):
            print(en, ru)
            if ru == 'Incoming request rate exceeded \
                        for 50000 chars per day pricing tier':
                break
            translated_words[en] = ru
            save_data(
                translated_words_json_file_name, translated_words)
    return translated_words


def get_translation_with_concurrent(
        word_translation_from_api,
        not_translated_words: list) -> dict:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for en, ru in zip(
                not_translated_words,
                executor.map(word_translation_from_api, not_translated_words)):
            print(en, ru)
            if ru == 'Incoming request rate exceeded \
                        for 50000 chars per day pricing tier':
                break
    return


class TypeError(Exception):
    pass


if __name__ == "__main__":
    not_translated_words = load_data(
        'data/not_translated_words.json')
    get_translation_with_concurrent(
        get_word_translation_from_abbyy_api, not_translated_words)
    get_word_translation_from_abbyy_api("rewgwwwwee")
