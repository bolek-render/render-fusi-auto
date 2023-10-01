import requests
import DATA.common_globals as cg
from COMMON.now_is import now_is


class GetLink:
    def __init__(self, bot, uid):
        self.bot = bot
        self.uid = uid
        self.url = cg.links_url
        self.querystring = {
            "lang": "1",
            "os": "h5",
            "cid": "ftsH5",
            "webVersion": "1000",
            "roomId": uid,
            "pageID": cg.main_page_id
        }
        self.headers = {
            "Host": cg.host,
            "accept": "application/json, text/javascript, */*; q=0.01",
            "user-agent": "Mozilla/5.0 (Linux; Android 7.1.2; ASUS_Z01QD) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
            "origin": "origin",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": cg.referer,
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9"
        }
        self.hls = None
        self.country = None

    def get_link(self):
        try:
            with requests.get(self.url, params=self.querystring, headers=self.headers) as response:
                if response.status_code == 200:
                    r = response.json()
                    if r['msg'] == 'successful':
                        self.hls = r['pullFlowUrlHLS']
                        self.country = r['roomBaseInfo']['addr']

                else:
                    print(f'{now_is()} - {cg.RED}Error while getting link{cg.RESET} : {response.status_code}\n')
                    self.bot.send_message(cg.errors, f'Error while getting link : {response.status_code}')

        except requests.exceptions.SSLError:
            print(f'{now_is()} - {cg.RED}SSLError while getting link{cg.RESET}, {cg.GREEN}trying again{cg.RESET}\n')
            self.bot.send_message(cg.errors, 'SSLError while getting link, trying again')
            cg.current_records.remove(self.uid)

        except requests.exceptions.ConnectionError:
            print(f'{now_is()} - {cg.RED}ConnectionError while getting link{cg.RESET}, {cg.GREEN}trying again{cg.RESET}\n')
            self.bot.send_message(cg.errors, 'ConnectionError while getting link, trying again')
            cg.current_records.remove(self.uid)

        except Exception as e:
            self.bot.send_message(cg.errors, f'Exception while getting link : {e}')
            print(f'{now_is()} - {cg.RED}Exception while getting link{cg.RESET} : {e}\n')
            cg.current_records.remove(self.uid)
