import os
import DATA.common_globals as cg
from COMMON.load import load


def config():

    if not os.path.isdir(f'{cg.PATH}/VIDS'):
        os.mkdir(f'{cg.PATH}/VIDS')

    cfg_path = f'{cg.PATH}/DATA/config'

    if os.path.isfile(cfg_path):
        cfg = load(cfg_path)
        cg.config = cfg
        cg.fs_user_token = cfg['fs_user_token']
        cg.fs_user_uid = cfg['fs_user_uid']
        cg.target = cfg['target']
        cg.errors = cfg['errors']
        cg.refresh_freq = cfg['refresh_freq']
        cg.admins = cfg['admins']
        cg.notify_users = cfg['notify_users']
        cg.notify_users.add(cg.MASTER)
        cg.admins.add(cg.MASTER)
