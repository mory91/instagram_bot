#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol

from multiprocessing import Process, Lock

import sys
sys.path.append('../')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram_bot.settings")

import django
django.setup()


from api.models import Reset, Target, Bot

bots_p = []

def get_tags(bot):
    tags = []
    tag_objs = Target.objects.filter(target_type='T', bot=bot.id)
    return tag_objs 

def get_pages(bot):
    pages = []
    pages_objs = Target.objects.filter(target_type='P', bot=bot.id)
    return pages_objs

def run_bot(bot, lck):
    last_id = 0
    lck.acquire()
    tags = get_tags(bot)
    if (len(bot.username) <= 0):
        bot.started = False
        return
    lck.release()
    
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
        lck.acquire()
        last = Reset.objects.filter(bot=bot.id).last()
        bot_db = Bot.objects.get(id=bot.id)
        lck.release()
        if bot_db.state == 2:
            insta_bot.cleanup()
            time.sleep(3)
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
            lck.acquire()
            bot_db.state = 1
            bot_db.save()
            lck.release()
        if last is not None and last.id > last_id:
            last_id = last.id
            tags = get_tags(bot)
            pages = get_pages(bot)
            insta_bot.tag_list = tags
            insta_bot.user_list = pages
           
        insta_bot.new_auto_mod_tag()
        insta_bot.new_auto_mod_page()

lock = Lock()

while(1):
    lock.acquire()
    bs = Bot.objects.all()
    if bs != None and len(bs) > 0:
        for b in bs:
            if b.state == -1:
                b.state = 1
                p = Process(target=run_bot, args=(b, lock,))
                p.start()
                time.sleep(3)
                bots_p.append({"id": b.id,  "process": p})
                b.save()
    lock.release()



