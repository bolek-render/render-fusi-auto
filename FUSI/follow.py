import requests
import DATA.common_globals as cg


def follow(fid, opt):
    url = cg.follow_url
    querystring = {"lang": "1",
                   "os": "h5",
                   "cid": "ftsH5",
                   "webVersion": "1000",
                   "uid": cg.fs_user_uid,
                   "token": cg.fs_user_token,
                   "roomId": fid,
                   "optType": opt,
                   "pageID": cg.user_page_id}
    headers = {"referer": cg.referer}

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()

    if response['code'] == 1:
        return True
    else:
        return False
