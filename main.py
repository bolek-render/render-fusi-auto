import os
import threading
import pyrostep
import DATA.common_globals as cg
from pyrogram import Client, filters, idle, enums
from pyrogram.errors import RPCError
from COMMON.config import config
from COMMON.save import save
from FUSI.Monitor import Monitor
from COMMON.now_is import now_is
from FUSI.follow import follow
from FUSI.userinfo import userinfo
from TG_BOT.keyboards import keyboards
from COMMON.keep_alive import keep_alive

cg.PATH = os.getcwd()

bot = Client('render-fusi-auto',
             api_id=os.environ['API_ID'],
             api_hash=os.environ['API_HASH'],
             bot_token=os.environ['BOT_TOKEN'],
             max_concurrent_transmissions=4)

pyrostep.listen(bot)

user_menu = {}


@bot.on_message(filters.command('start'))
async def start_command(client, msg):
    await msg.reply('Alive')


@bot.on_message(filters.command('current'))
async def c_command(client, msg):
    if len(cg.current_records) > 0:
        await msg.reply(cg.current_records)
    else:
        await msg.reply('Empty')


@bot.on_message(filters.command('unlock'))
async def u_command(client, msg):
    await msg.reply('Tap ID to unlock', reply_markup=keyboards('unlock'))


@bot.on_message(filters.command('threads'))
async def t_command(client, msg):
    text = ''
    for thread in threading.enumerate():
        text = text + str(thread).lstrip('<').rstrip('>') + '\n\n'
    await msg.reply(text)


@bot.on_message(filters.command('menu'))
async def menu_command(client, msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    await bot.delete_messages(cid, msg.id)
    bm = await bot.send_message(cid, 'MAIN MENU'
                                     '\n\nSelect option',
                                reply_markup=keyboards('menu', uid))
    user_menu[uid] = bm


@bot.on_message(filters.text)
async def text_msg(client, msg):
    uid = msg.from_user.id
    if uid == cg.MASTER:
        fid = msg.text
        if fid.isdigit() and len(fid) <= 7:
            text = userinfo(fid)
            if text is not None:
                await msg.reply(text, reply_markup=keyboards('follow', fid))


@bot.on_callback_query()
async def callback_query(client, call):
    cid = call.message.chat.id
    mid = call.message.id

    # try:
    #     uid = int(call.data.split('.')[1])
    # except IndexError:
    #     uid = 0

    # CLOSE
    if call.data == 'close':
        await pyrostep.unregister_steps(cid)
        await bot.delete_messages(cid, mid)
        del user_menu[cid]

    # MENU
    if call.data == 'menu':
        await bot.edit_message_text(cid, mid, 'MAIN MENU'
                                              '\n\nSelect option',
                                    reply_markup=keyboards('menu'))

    # FREQUENCY
    if call.data == 'freq_main':
        await pyrostep.unregister_steps(cid)
        await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                              f'\n\nCurrent frequency : {cg.refresh_freq}s',
                                    reply_markup=keyboards('freq_main'))

    if call.data == 'freq_set':
        await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                              f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                              f'\n\nEnter value in seconds (min 0 - 60 max) 💬',
                                    reply_markup=keyboards('freq_back'))
        await pyrostep.register_next_step(cid, freq_set)

    # VIDEO TARGET
    if call.data == 'target_main':
        await pyrostep.unregister_steps(cid)
        if cg.target is None:
            await bot.edit_message_text(cid, mid, f'Set basic target group for videos',
                                        reply_markup=keyboards('target_main'))
        else:
            await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                  f'\n\nCurrent target ID : {cg.target}',
                                        reply_markup=keyboards('target_main'))

    if call.data == 'target_set':
        if cg.target is None:
            await bot.edit_message_text(cid, mid, f'Set basic target group for videos'
                                                  f'\n\nEnter group ID 💬',
                                        reply_markup=keyboards('target_back'))
        else:
            await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                  f'\n\nCurrent target ID : {cg.target}'
                                                  f'\n\nEnter group ID 💬',
                                        reply_markup=keyboards('target_back'))
        await pyrostep.register_next_step(cid, target_set)

    # ERROR TARGET
    if call.data == 'error_main':
        await pyrostep.unregister_steps(cid)
        if cg.target is None:
            await bot.edit_message_text(cid, mid, f'Set basic target group for errors',
                                        reply_markup=keyboards('error_main'))
        else:
            await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                  f'\n\nCurrent errors log ID : {cg.errors}',
                                        reply_markup=keyboards('error_main'))

    if call.data == 'error_set':
        if cg.target is None:
            await bot.edit_message_text(cid, mid, f'Set basic target group for errors'
                                                  f'\n\nEnter errors log group ID 💬',
                                        reply_markup=keyboards('error_back'))
        else:
            await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                  f'\n\nCurrent errors log ID : {cg.errors}'
                                                  f'\n\nEnter errors log group ID 💬',
                                        reply_markup=keyboards('error_back'))
        await pyrostep.register_next_step(cid, error_set)

    # FUSI TOKEN
    if call.data == 'ftoken_main':
        await bot.edit_message_text(cid, mid, f'Set/change FUSI token'
                                              f'\n\nCurrent token : {cg.fs_user_token}',
                                    reply_markup=keyboards('ftoken_set'))

    if call.data == 'ftoken_set':
        await bot.edit_message_text(cid, mid, f'Set/change FUSI token'
                                              f'\n\nCurrent token : {cg.fs_user_token}'
                                              f'\n\nEnter token 💬',
                                    reply_markup=keyboards('ftoken_back'))
        await pyrostep.register_next_step(cid, ftoken_set)

    # VID FILES
    if call.data == 'files_main':
        cg.vid_files = os.listdir(f'{cg.PATH}\VIDS')
        await bot.edit_message_text(cid, mid, 'Available video files',
                                    reply_markup=keyboards('files'))

    if call.data == 'files_close':
        await bot.delete_messages(cid, mid)
        cg.vid_files.clear()

    if call.data.startswith('del_file'):
        index = int(call.data.split('.')[1])
        await bot.edit_message_text(cid, mid, f'Are you sure to delete file'
                                              f'\n\n{cg.vid_files[index]}',
                                    reply_markup=keyboards('files_sure', index))

    if call.data.startswith('files_yes'):
        index = int(call.data.split('.')[1])
        file = cg.vid_files[index]
        os.remove(f'{cg.PATH}/VIDS/{file}')
        cg.vid_files = os.listdir(f'{cg.PATH}\VIDS')
        await bot.edit_message_text(cid, mid, 'Available video files',
                                    reply_markup=keyboards('files'))
        await bot.answer_callback_query(call.id, f'✅ Video deleted', show_alert=True)

    # UNLOCK
    if call.data.startswith('unlock'):
        unlock_id = int(call.data.split('.')[1])
        try:
            cg.current_records.remove(unlock_id)
            await bot.edit_message_text(cid, mid, 'Tap ID to unlock', reply_markup=keyboards('unlock'))
        except KeyError:
            pass

    if call.data == 'exit':
        await bot.delete_messages(cid, mid)

    # FOLLOW / UNFOLLOW

    if call.data.startswith('follow'):
        fid = int(call.data.split('.')[1])
        if follow(fid, 1):
            await bot.answer_callback_query(call.id, f'✅ {fid} Followed', show_alert=True)
        else:
            await bot.answer_callback_query(call.id, f'☑️ {fid} Already followed', show_alert=True)

        await bot.delete_messages(cid, mid)

    if call.data.startswith('unfollow'):
        fid = int(call.data.split('.')[1])
        if follow(fid, 2):
            await bot.answer_callback_query(call.id, f'✅ {fid} Unfollowed', show_alert=True)
        else:
            await bot.answer_callback_query(call.id, f'☑️ {fid} Already unfollowed', show_alert=True)

        await bot.delete_messages(cid, mid)


# STEP HANDLERS
async def freq_set(client, msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    mid = user_menu[uid].id
    await bot.delete_messages(cid, msg.id)

    if msg.text is None:
        try:
            await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                  f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                  f'\n\nEnter value in seconds (min 0 - 60 max) 💬'
                                                  f'\n\n❌ Value must be digit ‼️',
                                        reply_markup=keyboards('freq_back', uid))
        except RPCError:
            pass
        await pyrostep.register_next_step(uid, freq_set)

    else:
        if msg.text.isdigit():
            new = int(msg.text)
            if new < 0:
                try:
                    await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                          f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                          f'\n\nEnter value in seconds (min 0 - 60 max) 💬'
                                                          f'\n\n❌ Value to low ‼️',
                                                reply_markup=keyboards('freq_back', uid))
                except RPCError:
                    pass
                await pyrostep.register_next_step(uid, freq_set)

            elif new > 60:
                try:
                    await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                          f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                          f'\n\nEnter value in seconds (min 0 - 60 max) 💬'
                                                          f'\n\n❌ Value to high ‼️',
                                                reply_markup=keyboards('freq_back', uid))
                except RPCError:
                    pass
                await pyrostep.register_next_step(uid, freq_set)

            elif new == cg.refresh_freq:
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\n☑️ Same value nothing changed',
                                            reply_markup=keyboards('freq_main', uid))

            else:
                cg.refresh_freq = new
                for k, v in cg.config.items():
                    if k == 'refresh_freq':
                        cg.config[k] = new
                    else:
                        cg.config[k] = v
                save(cg.config, f'{cg.PATH}/DATA/config')
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\n✅ Frequency changed',
                                            reply_markup=keyboards('freq_main', uid))

        else:
            try:
                await bot.edit_message_text(cid, mid, f'Set monitor refresh frequency in seconds'
                                                      f'\n\nCurrent frequency : {cg.refresh_freq}s'
                                                      f'\n\nEnter value in seconds (min 0 - 60 max) 💬'
                                                      f'\n\n❌ Value must be digit ‼️',
                                            reply_markup=keyboards('freq_back', uid))
            except RPCError:
                pass
            await pyrostep.register_next_step(uid, freq_set)


async def target_set(client, msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    mid = user_menu[uid].id
    await bot.delete_messages(cid, msg.id)

    if msg.text is None:
        try:
            await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                  f'\n\nCurrent target ID : {cg.target}'
                                                  f'\n\n❌ Value must be negative digit ‼️'
                                                  f'\n\nEnter group ID 💬',
                                        reply_markup=keyboards('target_back', uid))
        except RPCError as e:
            pass
        await pyrostep.register_next_step(uid, target_set)

    else:
        try:
            target = int(msg.text)
            if target > 0:
                try:
                    await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                          f'\n\nCurrent target ID : {cg.target}'
                                                          f'\n\n❌ Value must be negative digit ‼️'
                                                          f'\n\nEnter group ID 💬',
                                                reply_markup=keyboards('target_back', uid))
                except RPCError:
                    pass
                await pyrostep.register_next_step(uid, target_set)

            else:
                try:
                    await bot.send_chat_action(target, enums.ChatAction.TYPING)
                    cg.target = target
                    for k, v in cg.config.items():
                        if k == 'target':
                            cg.config[k] = target
                        else:
                            cg.config[k] = v
                    save(cg.config, f'{cg.PATH}/DATA/config')
                    await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                          f'\n\nCurrent target ID : {cg.target}'
                                                          f'\n\n✅ Target changed',
                                                reply_markup=keyboards('target_main', uid))
                except RPCError as e:
                    try:
                        await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                              f'\n\nCurrent target ID : {cg.target}'
                                                              f'\n\n⛔️ BOT can\'t write in this group'
                                                              f'\n\nEnter group ID 💬',
                                                    reply_markup=keyboards('target_back', uid))
                    except RPCError:
                        pass
                    await pyrostep.register_next_step(uid, target_set)

        except ValueError:
            try:
                await bot.edit_message_text(cid, mid, f'Change basic target group for videos'
                                                      f'\n\nCurrent target ID : {cg.target}'
                                                      f'\n\n❌ Value must be negative digit ‼️'
                                                      f'\n\nEnter group ID 💬',
                                            reply_markup=keyboards('target_back', uid))
            except RPCError:
                pass
            await pyrostep.register_next_step(uid, target_set)


async def error_set(client, msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    mid = user_menu[uid].id
    await bot.delete_messages(cid, msg.id)

    if msg.text is None:
        try:
            await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                  f'\n\nCurrent errors log ID : {cg.target}'
                                                  f'\n\n❌ Value must be negative digit ‼️'
                                                  f'\n\nEnter errors log group ID 💬',
                                        reply_markup=keyboards('error_back', uid))
        except RPCError as e:
            pass
        await pyrostep.register_next_step(uid, error_set)

    else:
        try:
            errors = int(msg.text)
            if errors > 0:
                try:
                    await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                          f'\n\nCurrent errors log ID : {cg.errors}'
                                                          f'\n\n❌ Value must be negative digit ‼️'
                                                          f'\n\nEnter errors log group ID 💬',
                                                reply_markup=keyboards('error_back', uid))
                except RPCError:
                    pass
                await pyrostep.register_next_step(uid, error_set)

            else:
                try:
                    await bot.send_chat_action(errors, enums.ChatAction.TYPING)
                    cg.errors = errors
                    for k, v in cg.config.items():
                        if k == 'errors':
                            cg.config[k] = errors
                        else:
                            cg.config[k] = v
                    save(cg.config, f'{cg.PATH}/DATA/config')
                    await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                          f'\n\nCurrent errors log ID : {cg.errors}'
                                                          f'\n\n✅ Errors log group changed',
                                                reply_markup=keyboards('error_main', uid))
                except RPCError as e:
                    try:
                        await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                              f'\n\nCurrent errors log ID : {cg.errors}'
                                                              f'\n\n⛔️ BOT can\'t write in this group'
                                                              f'\n\nEnter errors log group ID 💬',
                                                    reply_markup=keyboards('error_back', uid))
                    except RPCError:
                        pass
                    await pyrostep.register_next_step(uid, error_set)

        except ValueError:
            try:
                await bot.edit_message_text(cid, mid, f'Change basic target group for errors'
                                                      f'\n\nCurrent errors log ID : {cg.errors}'
                                                      f'\n\n❌ Value must be negative digit ‼️'
                                                      f'\n\nEnter errors log group ID 💬',
                                            reply_markup=keyboards('error_back', uid))
            except RPCError:
                pass
            await pyrostep.register_next_step(uid, error_set)


async def ftoken_set(client, msg):
    cid = msg.chat.id
    uid = msg.from_user.id
    mid = user_menu[uid].id
    await bot.delete_messages(cid, msg.id)

    if msg.text is None:
        try:
            await bot.edit_message_text(cid, mid, f'Set/change FUSI token'
                                                  f'\n\nCurrent token : {cg.fs_user_token}'
                                                  f'\n\n❌ FUSI token must be text ‼️'
                                                  f'\n\nEnter token 💬',
                                        reply_markup=keyboards('ftoken_back', uid))
        except RPCError as e:
            pass
        await pyrostep.register_next_step(uid, ftoken_set)

    else:
        cg.fs_user_token = msg.text
        for k, v in cg.config.items():
            if k == 'fs_user_token':
                cg.config[k] = msg.text
            else:
                cg.config[k] = v
        save(cg.config, f'{cg.PATH}/DATA/config')
        await bot.edit_message_text(cid, mid, f'Set/change FUSI token'
                                              f'\n\nCurrent token : {cg.fs_user_token}'
                                              f'\n\n✅ FUSI token changed',
                                    reply_markup=keyboards('ftoken_set', uid))

        if cg.fs_user_uid is not None:
            Monitor(bot).start()


if __name__ == '__main__':
    try:
        bot.stop()
    except ConnectionError:
        pass

    bot.start()

    config()

    if cg.fs_user_token is not None and cg.fs_user_uid is not None:
        monitor = Monitor(bot)
        monitor.start()
    else:
        bot.send_message(cg.MASTER, 'Fusi token / userID unset')

    # keep_alive()

    print(f'{now_is()} - {cg.GREEN}BOT STARTED{cg.RESET}\n')
    idle()
    bot.stop()
