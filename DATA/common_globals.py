import os

RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\u001b[33m'
RESET = '\033[0m'

PATH = None

# HIDDEN ENV
MASTER = int(os.environ['MASTER'])
lives_url = os.environ['lives_url']
links_url = os.environ['links_url']
user_url = os.environ['user_url']
follow_url = os.environ['follow_url']
host = os.environ['host']
main_page_id = os.environ['main_page_id']
user_page_id = os.environ['user_page_id']
referer = os.environ['referer']


# COMMON FROM CONFIG FILE
config = {}
fs_user_token = None
fs_user_uid = None
target = None
errors = None
refresh_freq = 0
admins = set()
notify_users = set()


current_records = set()
