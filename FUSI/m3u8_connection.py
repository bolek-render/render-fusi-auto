import requests
import DATA.common_globals as cg
from COMMON.now_is import now_is


def m3u8_test(bot, link):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; ASUS_Z01QD) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Mobile Safari/537.36'}

    try:
        temp_link = link.split('?')
        url = temp_link[0]
        query = temp_link[1].split('&')
        sign = query[0].split('=')
        t = query[1].split('=')
        querystring = {sign[0]: sign[1], t[0]: t[1]}
    except IndexError:
        return False

    try:
        with requests.get(url, params=querystring, headers=headers) as response:
            if response.status_code == 200:
                return True
            else:
                return False

    except Exception as e:
        print(f'{now_is()} - {cg.RED}M3U8 connection test exception{cg.RESET} : {e}\n')
        bot.send_message(cg.errors, f'M3U8 connection test exception : {e}')
        return False
