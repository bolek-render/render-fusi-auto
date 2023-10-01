from threading import Thread
import time
import requests
import DATA.common_globals as cg
from FUSI.AutoRecHandler import AutoRecHandler
from COMMON.now_is import now_is


class Monitor(Thread):
    def __init__(self, bot) -> None:
        Thread.__init__(self)
        self.bot = bot
        self.name = 'FUSI MONITOR'
        self.url = cg.lives_url
        self.querystring = {
            "lang": "1",
            "os": "h5",
            "cid": "ftsH5",
            "webVersion": "1000",
            "uid": cg.fs_user_uid,
            "token": cg.fs_user_token,
            "pageNum": "1",
            "pageSize": "99",
            "pass": "true",
            "pageID": cg.main_page_id
        }
        self.headers = {"referer": cg.referer}
        self.stop = False

    def run(self) -> None:
        while not self.stop:
            try:
                response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
                data = response.json()

                if data['code'] == 1:
                    for room in data['rooms']:
                        name = room['nickname']
                        state = room['liveState']  # 0 offline / 1 live
                        uid = room['uid']
                        title = room['introduce']

                        live_data = {'uid': uid,
                                     'name': name,
                                     'title': title}

                        if state == 1:
                            if uid not in cg.current_records:
                                cg.current_records.add(uid)
                                AutoRecHandler(self.bot, uid, live_data).start()

                        # if state == 0:
                        #     if uid in cg.current_records:
                        #         print(f'{now_is()} - {cg.BLUE}{uid}{cg.RESET} '
                        #               f'{cg.YELLOW}state 0 found in cr{cg.RESET}\n')

                    time.sleep(cg.refresh_freq)

                elif data['code'] == -1000:
                    self.bot.send_message(cg.errors, 'MONITOR stopped - Token expired')
                    self.bot.send_message(cg.MASTER, 'MONITOR stopped - Token expired')
                    print(f'{now_is()} - {cg.RED}MONITOR stopped - Token expired{cg.RESET}\n')
                    break

                else:
                    self.bot.send_message(cg.errors, f'MONITOR stopped - Unhandled response : {data}')
                    print(f'{now_is()} - '
                          f'{cg.RED}MONITOR stopped - Unhandled response while checking lives{cg.RESET} : {data}\n')
                    break
            except Exception as e:
                self.bot.send_message(cg.errors, f'Exception while checking lives : {e}')
                print(f'{now_is()} - {cg.RED}Exception while checking lives{cg.RESET} : {e}\n')
