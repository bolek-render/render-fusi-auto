from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import DATA.common_globals as cg


def keyboards(keyboard, param=None):

    # BOT SETTINGS
    if keyboard == 'menu':
        btn1 = InlineKeyboardButton('MONITOR FREQUENCY', callback_data=f'freq_main.{param}')
        btn2 = InlineKeyboardButton('VIDEO TARGET', callback_data=f'target_main.{param}')
        btn3 = InlineKeyboardButton('ERROR TARGET', callback_data=f'error_main.{param}')
        btn4 = InlineKeyboardButton('FUSI TOKEN', callback_data=f'ftoken_main.{param}')
        btn5 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [[btn1], [btn2], [btn3], [btn4], [btn5]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # MONITOR FREQUENCY
    if keyboard == 'freq_main':
        btn1 = InlineKeyboardButton('CHANGE', callback_data=f'freq_set.{param}')
        btn2 = InlineKeyboardButton('BACK', callback_data=f'menu.{param}')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [
            [btn1],
            [btn2, btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'freq_back':
        btn1 = InlineKeyboardButton('BACK', callback_data=f'freq_main.{param}')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [[btn1, btn2]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # VIDEO TARGET
    if keyboard == 'target_main':
        if cg.target is None:
            btn1 = InlineKeyboardButton('SET', callback_data=f'target_set.{param}')
        else:
            btn1 = InlineKeyboardButton('CHANGE', callback_data=f'target_set.{param}')
        btn2 = InlineKeyboardButton('BACK', callback_data=f'menu.{param}')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [
            [btn1],
            [btn2, btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'target_back':
        btn1 = InlineKeyboardButton('BACK', callback_data=f'target_main.{param}')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [[btn1, btn2]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # ERROR TARGET
    if keyboard == 'error_main':
        if cg.target is None:
            btn1 = InlineKeyboardButton('SET', callback_data=f'error_set.{param}')
        else:
            btn1 = InlineKeyboardButton('CHANGE', callback_data=f'error_set.{param}')
        btn2 = InlineKeyboardButton('BACK', callback_data=f'menu.{param}')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [
            [btn1],
            [btn2, btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'error_back':
        btn1 = InlineKeyboardButton('BACK', callback_data=f'error_main.{param}')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [[btn1, btn2]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    # FUSI TOKEN
    if keyboard == 'ftoken_set':
        btn1 = InlineKeyboardButton('SET / CHANGE', callback_data=f'ftoken_set.{param}')
        btn2 = InlineKeyboardButton('BACK', callback_data=f'menu.{param}')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
        buttons = [
            [btn1],
            [btn2, btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb

    if keyboard == 'ftoken_back':
        btn1 = InlineKeyboardButton('BACK', callback_data=f'ftoken_main.{param}')
        btn2 = InlineKeyboardButton('CLOSE', callback_data=f'close.{param}')
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
        btn1 = InlineKeyboardButton('FOLLOW', callback_data=f'follow.{param}')
        btn2 = InlineKeyboardButton('UNFOLLOW', callback_data=f'unfollow.{param}')
        btn3 = InlineKeyboardButton('CLOSE', callback_data=f'exit')
        buttons = [
            [btn1, btn2],
            [btn3]
        ]
        kb = InlineKeyboardMarkup(buttons)
        return kb
