#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol

import threading

import sys
sys.path.append('../')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram_bot.settings")

import django
django.setup()


from api.models import Reset, Target, Bot

bots_t = []

def get_tags(bot):
    tags = []
    tag_objs = Target.objects.filter(target_type='T', bot=bot.id)
    return tag_objs 

def get_pages(bot):
    pages = []
    pages_objs = Target.objects.filter(target_type='P', bot=bot.id)
    return pages_objs

def run_bot(bot):
    last_id = 0
    tags = get_tags(bot)
    if (len(bot.username) <= 0):
        bot.started = False
        return
    
    insta_bot = InstaBot(
        login=bot.username,
        password=bot.password,
        like_per_day=bot.like_per_day,
        comments_per_day=bot.comment_per_day,
        tag_list=[],
        user_list=[],
        max_like_for_one_tag=50,
        follow_per_day=bot.follow_per_day,
        follow_time=1 * 60,
        unfollow_per_day=bot.unfollow_per_day,
        unfollow_break_min=15,
        unfollow_break_max=30,
        log_mod=0,
        proxy='',
        comment_list=[bot.comments.split("*")],
        unwanted_username_list=[],
        second_login=bot.second_username,
        second_password=bot.second_password)

    while(1):
        last = Reset.objects.filter(bot=bot.id).last()
        bot_db = Bot.objects.get(id=bot.id)
        if bot_db.state == 2:
            insta_bot.cleanup()
            time.sleep(10)
            insta_bot = InstaBot(
                login=bot.username,
                password=bot.password,
                like_per_day=bot.like_per_day,
                comments_per_day=bot.comment_per_day,
                tag_list=[],
                user_list=[],
                max_like_for_one_tag=50,
                follow_per_day=bot.follow_per_day,
                follow_time=1 * 60,
                unfollow_per_day=bot.unfollow_per_day,
                unfollow_break_min=15,
                unfollow_break_max=30,
                log_mod=0,
                proxy='',
                comment_list=[bot.comments.split("*")],
                unwanted_username_list=[],
                second_login=bot.second_username,
                second_password=bot.second_password)
            bot_db.state = 1
            bot_db.save()
        if last is not None and last.id > last_id:
            last_id = last.id
            tags = get_tags(bot)
            pages = get_pages(bot)
            insta_bot.tag_list = tags
            insta_bot.user_list = pages
           
        insta_bot.new_auto_mod_tag()
        insta_bot.new_auto_mod_page()



bs = Bot.objects.all()
bs_list = list(bs)
if bs != None and len(bs) > 0:
    for b in bs_list:
        if b.state == 1:
            b.state = -1
            b.save()

while(1):
    bs = Bot.objects.all()
    bs_list = list(bs)
    if bs != None and len(bs) > 0:
        for b in bs_list:
            if b.state == -1:
                b.state = 1
                t = threading.Thread(target=run_bot, args=(b,))
                t.start()
                time.sleep(3)
                bots_t.append({"id": b.id,  "process": t})
                b.save()



