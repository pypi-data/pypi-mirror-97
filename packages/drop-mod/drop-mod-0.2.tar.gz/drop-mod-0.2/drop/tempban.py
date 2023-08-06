from datetime import datetime
import json
import os
from drop.errors import *

import parsedatetime
cal = parsedatetime.Calendar()

# If this whole extension looks familiar, it is: I basically just copy-pasted mute.py and edited it to fit with
# temp-bans instead of mutes.


def get_temp_bans_file():
    try:
        with open("data/temp_bans.json", "r", encoding="utf-8", newline="\n") as file:
            return json.load(file)
    except FileNotFoundError:
        if not os.path.exists("data/"):
            os.makedirs("data/")
        with open("data/temp_bans.json", "w+", encoding="utf-8", newline="\n") as file:
            json.dump({}, file)
            return {}


def check_bans(clear_bans=True):
    unban_list = []
    to_clear = []
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M")
    unbans = get_temp_bans_file()
    if dt_string in unbans:
        # we have people to unban for now
        for toUnban in unbans.get(dt_string):
            guild_id = toUnban[1]
            user_id = toUnban[0]
            unban_list.append({
                "guild_id": guild_id,
                "user_id": user_id
            })
            if clear_bans:
                to_clear.append([guild_id, user_id])
        if clear_bans:
            unbans = json.load(open("data/temp_bans.json", "r", encoding="utf-8", newline="\n"))
            unbans.pop(dt_string)
            for to_remove in to_clear:
                guild = to_remove[0]
                user = to_remove[1]
                unbans[str(guild)].pop(str(user))
                if not unbans.get(str(guild)):
                    unbans.pop(str(guild))
            json.dump(unbans, open("data/temp_bans.json", "w+", encoding="utf-8", newline="\n"))
    return unban_list


def add_bans(guild_id: int, user_id: int, author_id: int, datetime_to_parse: str):
    bans = get_temp_bans_file()
    new_ban_data = (user_id, guild_id)
    dt_obj = cal.parseDT(datetimeString=datetime_to_parse)
    now_dt = datetime.now()
    list_dt_obj = str(dt_obj[0]).split(":")
    list_now_dt = str(now_dt).split(":")

    str_now_dt = f'{list_now_dt[0]}:{list_now_dt[1]}'
    str_dt_obj = f'{list_dt_obj[0]}:{list_dt_obj[1]}'
    if dt_obj[1] == 0:
        raise InvalidTimeParsed(f"Time string {datetime_to_parse} could not be parsed")
    elif dt_obj[0] <= now_dt:
        raise PastTimeError(f"Time {str(dt_obj)} is in the past: there's no logical way to unban them that way")
    elif dt_obj[0] == now_dt or str_dt_obj == str_now_dt:
        raise PresentTimeError(f"Time {str(dt_obj)} is the same as now ({str(now_dt)})")
    # if the script made it this far, this is real we have to store temp-ban data
    if str_dt_obj not in bans:
        bans[str_dt_obj] = []
    bans[str_dt_obj].append(new_ban_data)
    temp_ban_index = len(bans[str_dt_obj]) - 1  # how the hell does that work
    if str(guild_id) not in bans:
        bans[str(guild_id)] = {}
    if str(user_id) in bans[str(guild_id)]:
        bans[str(guild_id)].pop(str(user_id))
    if not str(user_id) in bans[str(guild_id)]:
        bans[str(guild_id)][str(user_id)] = []
    bans[str(guild_id)][str(user_id)] = [str_dt_obj, author_id, temp_ban_index]
    json.dump(bans, open("data/temp_bans.json", "w+", newline='\n', encoding='utf-8'))
    return str_dt_obj
    # Don't worry I can't read this mess either.


def get_ban_status(guild_id: int, user_id: int):
    with open("data/temp_bans.json", "r", newline='\n', encoding='utf-8') as temp_file:
        bans = json.load(temp_file)
    guild_temp_bans = bans.get(str(guild_id))
    if guild_temp_bans is None:
        raise NoTempBansForGuild(f"Guild {guild_id} does not have any current temp-bans.")
    user_bans = guild_temp_bans.get(str(user_id))
    if not user_bans:
        return None
    # user has been muted.
    ban_index = user_bans[2]
    ban_data = bans.get(user_bans[0])[ban_index]
    return {
        "unban_time": user_bans[0],
        "ban_author_id": user_bans[1],
        "ban_index": ban_index,
        "ban_data": ban_data
    }


def unban_user(guild_id: int, user_id: int):
    bans = get_temp_bans_file()
    try:
        guild_bans = bans.get(str(guild_id))
    except KeyError:
        raise NoTempBansForGuild(f"Guild {guild_id} does not have any current temp-bans.")
    user_bans = get_ban_status(guild_id, user_id)
    unban_time = user_bans["unban_time"]
    ban_index = user_bans["ban_index"]
    bans.get(unban_time).pop(ban_index)
    if not bans.get(unban_time):
        bans.pop(unban_time)
    guild_bans.pop(str(user_id))
    if not guild_bans:
        bans.pop(str(guild_id))
    else:
        for key, value in bans[str(guild_id)].items():
            value[2] = value[2] - 1
    json.dump(bans, open("data/temp_bans.json", "w+", newline='\n', encoding='utf-8'))
    return
