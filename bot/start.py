import random 
from instapy import InstaPy
import threading
import datetime
import time
import random
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
    tag_objs = list(Target.objects.filter(target_type='T', bot=bot.id))
    tags_to_ret = []
    for t in tag_objs:
        tags_to_ret.append(t.target)
    return tags_to_ret 

def get_pages_follow_followers(bot):
    pages = []
    # TODO: change buttom F to L
    pages_objs = list(Target.objects.filter(target_type='P', bot=bot.id, target_follows='F'))
    pages_to_ret = []
    for p in pages_objs:
        pages_to_ret.append(p.target)
    return pages_to_ret

def get_pages_follow_likers(bot):
    pages = []
    pages_objs = list(Target.objects.filter(target_type='P', bot=bot.id, target_follows='L'))
    pages_to_ret = []
    for p in pages_objs:
        pages_to_ret.append(p.target)
    return pages_to_ret

def worker(bot):
    
    last_id = 0
    tags = get_tags(bot)
    followersToFollow = get_pages_follow_followers(bot)
    likersToFollow = get_pages_follow_likers(bot)
    
    

    if (len(bot.username) <= 0):
        bot.started = False
        return

    instaUser = bot.username
    instaPass = bot.password
    smartTags = tags
    print("MULTI - Started as",instaUser,"at",datetime.datetime.now().strftime("%H:%M:%S"))
    session = InstaPy(username=instaUser, password=instaPass, headless_browser=True) 
    print(instaUser)
    session.login()

    session.set_relationship_bounds(enabled=False)

    while 1:
        last = Reset.objects.filter(bot=bot.id).last()
        
        bot_db = Bot.objects.get(id=bot.id)
        smartTags = tags
        
        # session.set_dont_unfollow_active_users(enabled=True, posts=7)
        # session.set_user_interact(amount=2, randomize=True, percentage=20, media='Photo')
        # session.set_relationship_bounds(enabled=True,
        #         potency_ratio=-1.21,
        #         delimit_by_numbers=True,
        #         max_followers=4590,
        #             max_following=5555,
        #             min_followers=45,
        #             min_following=77)

        # session.like_by_feed(amount=random.randint(5,11), randomize=True, unfollow=True, interact=True)
        # print("MULTI -",instaUser,"finished liking by feed at",datetime.datetime.now().strftime("%H:%M:%S"))


        # Location
        # if not followLocation[selection] == '':#if no location given for that account, just ignore this step
        #     session.like_by_locations(followLocation[selection], amount=10)
        #     print("MULTI -",instaUser[selection],"finished liking by location",datetime.datetime.now().strftime("%H:%M:%S"))


        session.set_do_comment(enabled=True, percentage=25)
        session.set_comments(bot.comments.split('*'))

        # session.unfollow_users(amount=random.randint(1, 5), sleep_delay=(random.randint(44,111)))
        # print("MULTI -",instaUser ,"finished unfollowing at",datetime.datetime.now().strftime("%H:%M:%S"))
        
        if likersToFollow:
            random_likers_to_follow = random.sample(likersToFollow, min(5, len(likersToFollow)))
            session.set_user_interact(amount=2,
				 percentage=70,
                  randomize=True,
                   media='Photo')
            # session.follow_likers (random_likers_to_follow, photos_grab_amount = 2, follow_likers_per_photo = 3, randomize=True, sleep_delay=600, interact=True)
            session.follow_user_followers(random_likers_to_follow, amount=random.randint(44,55), randomize=False, interact=True, sleep_delay=111)
            print("MULTI -",instaUser,"finished following likers at",datetime.datetime.now().strftime("%H:%M:%S")) 

        # Followers of followers
        if followersToFollow:
            random_followers_to_follow = random.sample(followersToFollow, min(5, len(followersToFollow)))
            session.set_user_interact(amount=2,
				 percentage=70,
                  randomize=True,
                   media='Photo')
            session.follow_user_followers(random_followers_to_follow, amount=random.randint(44,55), randomize=False, interact=True, sleep_delay=111)
            print("MULTI -",instaUser,"finished following followers at",datetime.datetime.now().strftime("%H:%M:%S")) 


            
        
        if smartTags:
            session.set_smart_hashtags(smartTags, limit=3, sort='top', log_tags=True)
            session.like_by_tags(amount=random.randint(2,5), use_smart_hashtags=True)
            print("MULTI -",instaUser,"finished smartTags at",datetime.datetime.now().strftime("%H:%M:%S"))
        
        if last is not None and last.id > last_id:
            last_id = last.id
            tags = get_tags(bot)
            followersToFollow = get_pages_follow_followers(bot)
            likersToFollow = get_pages_follow_likers(bot)
            smartTags = tags
            # insta_bot.user_list = pages

    session.end()
    print("MULTI -",instaUser,"finished run at",datetime.datetime.now().strftime("%H:%M:%S"))

if __name__ == '__main__':        
    print("MULTI -","Starting at",datetime.datetime.now().strftime("%H:%M:%S"))
    jobs = []   
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
                    p = threading.Thread(target=worker, args=(b,))
                    p.start()
                    time.sleep(10)
                    bots_t.append({"id": b.id,  "process": p})
                    b.save()
                    











#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import os
# import time



# import threading

# import sys
# sys.path.append('../')

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram_bot.settings")

# import django
# django.setup()


# from api.models import Reset, Target, Bot

# bots_t = []

# def get_tags(bot):
#     tags = []
#     tag_objs = Target.objects.filter(target_type='T', bot=bot.id)
#     return tag_objs 

# def get_pages(bot):
#     pages = []
#     pages_objs = Target.objects.filter(target_type='P', bot=bot.id)
#     return pages_objs

# def run_bot(bot):
#     last_id = 0
#     tags = get_tags(bot)
#     if (len(bot.username) <= 0):
#         bot.started = False
#         return
    
#     insta_bot = InstaBot(
#         login=bot.username,
#         password=bot.password,
#         like_per_day=bot.like_per_day,
#         comments_per_day=bot.comment_per_day,
#         tag_list=[],
#         user_list=[],
#         max_like_for_one_tag=50,
#         follow_per_day=bot.follow_per_day,
#         follow_time=1 * 60,
#         unfollow_per_day=bot.unfollow_per_day,
#         unfollow_break_min=15,
#         unfollow_break_max=30,
#         log_mod=0,
#         proxy='',
#         comment_list=[bot.comments.split("*")],
#         unwanted_username_list=[],
#         second_login=bot.second_username,
#         second_password=bot.second_password)

#     while(1):
#         last = Reset.objects.filter(bot=bot.id).last()
#         bot_db = Bot.objects.get(id=bot.id)
#         if bot_db.state == 2:
#             insta_bot.cleanup()
#             time.sleep(10)
#             insta_bot = InstaBot(
#                 login=bot.username,
#                 password=bot.password,
#                 like_per_day=bot.like_per_day,
#                 comments_per_day=bot.comment_per_day,
#                 tag_list=[],
#                 user_list=[],
#                 max_like_for_one_tag=50,
#                 follow_per_day=bot.follow_per_day,
#                 follow_time=1 * 60,
#                 unfollow_per_day=bot.unfollow_per_day,
#                 unfollow_break_min=15,
#                 unfollow_break_max=30,
#                 log_mod=0,
#                 proxy='',
#                 comment_list=[bot.comments.split("*")],
#                 unwanted_username_list=[],
#                 second_login=bot.second_username,
#                 second_password=bot.second_password)
#             bot_db.state = 1
#             bot_db.save()
#         if last is not None and last.id > last_id:
#             last_id = last.id
#             tags = get_tags(bot)
#             pages = get_pages(bot)
#             insta_bot.tag_list = tags
#             insta_bot.user_list = pages
        
#         threadLock.acquire()
#         insta_bot.new_auto_mod_tag()
#         insta_bot.new_auto_mod_page()
#         threadLock.release()


# threadLock = threading.Lock()
# bs = Bot.objects.all()
# bs_list = list(bs)
# if bs != None and len(bs) > 0:
#     for b in bs_list:
#         if b.state == 1:
#             b.state = -1
#             b.save()

# while(1):
#     bs = Bot.objects.all()
#     bs_list = list(bs)
#     if bs != None and len(bs) > 0:
#         for b in bs_list:
#             if b.state == -1:
#                 b.state = 1
#                 t = threading.Thread(target=run_bot, args=(b,))
#                 t.start()
#                 time.sleep(3)
#                 bots_t.append({"id": b.id,  "process": t})
#                 b.save()


