import os

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import DATA.common_globals as cg


def keyboards(keyboard, param=None):

    # BOT SETTINGS
    if keyboard == 'menu':
        btn1 = InlineKeyboardButton('MONITOR FREQUENCY', callback_data=f'freq_main')
        btn2 = InlineKeyboardButton('VIDEO TARGET', callback_data=f'target_main')
        btn3 = InlineKeyboardButton('ERROR TARGET', callback_data=f'error_main')
        btn4 = InlineKeyboardButton('FUSI TOKEN', callback_data=f'ftoken_main')
        btn5 = InlineKeyboardButton('VIDEO FILES', callback_data=f'files_main')
        btn6 = InlineKeyboardButton('CLOSE', callback_data=f'close')
        buttons = [[btn1], [btn2], [btn3], [btn4], [btn5], [btn6]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # MONITOR FREQUENCY
    if keyboard == 'freq_main':
        btn1 = InlineKeyboardButton('CHANGE', callback_data=f'freq_set')
        btn2 = InlineKeyboardButton('BACK', callback_data=f'menu')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close')
        buttons = [
            [btn1],
            [btn2, btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'freq_back':
        btn1 = InlineKeyboardButton('BACK', callback_data=f'freq_main')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'close')
        buttons = [[btn1, btn2]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # VIDEO TARGET
    if keyboard == 'target_main':
        if cg.target is None:
            btn1 = InlineKeyboardButton('SET', callback_data=f'target_set')
        else:
            btn1 = InlineKeyboardButton('CHANGE', callback_data=f'target_set')
        btn2 = InlineKeyboardButton('BACK', callback_data=f'menu')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close')
        buttons = [
            [btn1],
            [btn2, btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'target_back':
        btn1 = InlineKeyboardButton('BACK', callback_data=f'target_main')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'close')
        buttons = [[btn1, btn2]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # ERROR TARGET
    if keyboard == 'error_main':
        if cg.target is None:
            btn1 = InlineKeyboardButton('SET', callback_data=f'error_set')
        else:
            btn1 = InlineKeyboardButton('CHANGE', callback_data=f'error_set')
        btn2 = InlineKeyboardButton('BACK', callback_data=f'menu')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close')
        buttons = [
            [btn1],
            [btn2, btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'error_back':
        btn1 = InlineKeyboardButton('BACK', callback_data=f'error_main')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'close')
        buttons = [[btn1, btn2]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # FUSI TOKEN
    if keyboard == 'ftoken_set':
        btn1 = InlineKeyboardButton('SET / CHANGE', callback_data=f'ftoken_set')
        btn2 = InlineKeyboardButton('BACK', callback_data=f'menu')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close')
        buttons = [
            [btn1],
            [btn2, btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'ftoken_back':
        btn1 = InlineKeyboardButton('BACK', callback_data=f'ftoken_main')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'close')
        buttons = [[btn1, btn2]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # UNLOCK
    if keyboard == 'unlock':
        buttons = []
        for uid in cg.current_records:
            btn = InlineKeyboardButton(f'{uid}', callback_data=f'unlock.{uid}')
            buttons.append([btn])
        btn1 = InlineKeyboardButton('CLOSE', callback_data=f'exit')
        buttons.append([btn1])
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # FOLLOW / UNFOLLOW
    if keyboard == 'follow':
        fid = param
        btn1 = InlineKeyboardButton('FOLLOW', callback_data=f'follow.{fid}')
        btn2 = InlineKeyboardButton('UNFOLLOW', callback_data=f'unfollow.{fid}')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'exit')
        buttons = [
            [btn1, btn2],
            [btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # FILES
    if keyboard == 'files':
        buttons = []

        for index, file in enumerate(cg.vid_files):
            btn = InlineKeyboardButton(f'{file}', callback_data=f'del_file.{index}')
            buttons.append([btn])
        btn1 = InlineKeyboardButton('BACK', callback_data=f'menu')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'files_close')
        buttons.append([btn1, btn2])
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'files_sure':
        index = param
        btn1 = InlineKeyboardButton('NO !', callback_data=f'files_main')
        btn2 = InlineKeyboardButton('YES', callback_data=f'files_yes.{index}')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'files_close')
        buttons = [
            [btn1, btn2],
            [btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb
