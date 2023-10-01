import requests
import DATA.common_globals as cg


def userinfo(fid):
    url = cg.user_url
    querystring = {"lang": "1",
                   "os": "h5",
                   "cid": "ftsH5",
                   "webVersion": "1000",
                   "fid": fid,
                   "pageID": cg.user_page_id}
    headers = {"referer": cg.referer}

    try:
        with requests.get(url, params=querystring, headers=headers) as response:
            response = response.json()

            try:
                nick = response['zoneInfo']['nickname']
                country = response['zoneInfo']['addr']
                followme = response['zoneData']['followme']
                myfollow = response['zoneData']['myfollow']
                text = (f'{fid} | {nick}'
                        f'\nCOUNTRY : {country}'
                        f'\nFANS : {followme}  |  FOLLOWED : {myfollow}')
                return text
            except KeyError:
                return None

    except Exception:
        return None

