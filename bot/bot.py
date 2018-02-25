#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol



import sys
sys.path.append('../')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram_bot.settings")

import django
django.setup()


from api.models import Reset, Target


def get_tags():
    tags = []
    tag_objs = Target.objects.filter(target_type='T')
    return tag_objs

def get_pages():
    pages = []
    pages_objs = Target.objects.filter(target_type='P')
    return pages_objs

last_id = 0
tags = get_tags()
bot = InstaBot(
    login="Alias.gallery",
    password="#575#830*220",
    like_per_day=1000,
    comments_per_day=5,
    tag_list=tags,
    user_list=['mehrdad89228'],
    user_blacklist={},
    max_like_for_one_tag=50,
    follow_per_day=3000,
    follow_time=1 * 60,
    unfollow_per_day=300,
    unfollow_break_min=15,
    unfollow_break_max=30,
    log_mod=0,
    proxy='',
    comment_list=[['خیلی'], ['خوبه']],
    unwanted_username_list=[])

while(1):
    last = Reset.objects.last()
    if last is not None and last.id > last_id:
        last_id = last.id
        tags = get_tags()
        pages = get_pages()
        bot.tag_list = tags
        bot.user_list = pages

    mode = -1

    if mode == -1:
        bot.new_auto_mod_tag()
        bot.new_auto_mod_page()

    elif mode == 0:
        bot.new_auto_mod()
    elif mode == 1:
        check_status(bot)
        while bot.self_following - bot.self_follower > 200:
            unfollow_protocol(bot)
            time.sleep(10 * 60)
            check_status(bot)
        while bot.self_following - bot.self_follower < 400:
            while len(bot.user_info_list) < 50:
                feed_scanner(bot)
                time.sleep(5 * 60)
                follow_protocol(bot)
                time.sleep(10 * 60)
                check_status(bot)
    elif mode == 2:
        bot.bot_mode = 1
        bot.new_auto_mod()
    elif mode == 3:
        unfollow_protocol(bot)
        time.sleep(10 * 60)
    elif mode == 4:
        feed_scanner(bot)
        time.sleep(60)
        follow_protocol(bot)
        time.sleep(10 * 60)
    elif mode == 5:
        bot.bot_mode = 2
        unfollow_protocol(bot)
    else:
        print("Wrong mode!")
