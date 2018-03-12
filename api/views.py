from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from api.models import Target
from api.models import Bot
import json
from .util_functions import do_reset
from django.http import HttpResponse
import os

def index(request):
    return JsonResponse({"test": "salam"})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect(dashboard)
        else:
            return redirect(login_user)

    else:
        if request.user.is_authenticated:
            return redirect(dashboard)
        else:
            return render(request, "./panel/login.html")

@login_required
def dashboard(request, bot_id):
    targets = Target.objects.filter(bot__pk=bot_id)
    bots = Bot.objects.all()
    bot = Bot.objects.get(id=bot_id)
    for t in targets:
        actions = t.target_action
        t.target_action = ""
        if "l" in actions:
            t.target_action = t.target_action + " Like "
        if "c" in actions:
            t.target_action = t.target_action + " Comment "
        if "f" in actions:
            t.target_action = t.target_action + " Follow "
    return render(request, "./panel/index.html", {"targets":targets, "bots": bots, "activated": bot})

@login_required
def add_target(request, bot_id):
    data   = json.loads(request.body.decode('utf-8'))
    target_type = data["type"]
    target = data["target"]
    target_action = ""
    follows = data['follows']
    already = Target.objects.filter(target=target)
    
    if (len(already) > 0):
        return HttpResponse("already")

    if data["a_l"] == True:
        target_action = target_action + "l"
    if data["a_f"] == True:
        target_action = target_action + "f"
    if data["a_c"] == True:
        target_action = target_action + "c"
    b = Bot.objects.get(id=bot_id)
    t = Target(target=target, target_type=target_type, target_action=target_action, target_follows= follows, bot=b)
    t.save()
    do_reset(bot_id)
    return HttpResponse("success")

@login_required
def add_page_group(request):
    data   = json.loads(request.body.decode('utf-8'))
    target_type = 'P'
    targets = data["targets"]
    target_action = ""
    already_num = 0
    success_num = 0
    follows = data['follows']
    for t in targets:
        target_username = t['user']['username']
        already = Target.objects.filter(target=target_username)
        if (len(already) > 0):
            already_num = already_num + 1
            continue
        if data["a_l"] == True:
            target_action = target_action + "l"
        if data["a_f"] == True:
            target_action = target_action + "f"
        if data["a_c"] == True:
            target_action = target_action + "c"
        b = Bot.objects.get(id=bot_id)
        saving = Target(target=target_username, target_type=target_type, target_action=target_action, target_follows= follows, bot=b)
        saving.save()
        success_num = success_num + 1
    do_reset(bot_id)
    return JsonResponse({"already": already_num, "success": success_num})

@login_required
def delete_target(request, id, bot_id):
    Target.objects.filter(id=id).delete()
    return redirect("/api/" + str(bot_id) + "/dashboard")
@login_required
def change_follows_state(request, bot_id):
    data   = json.loads(request.body.decode('utf-8'))
    id = data['id']
    state = data['state']
    target = Target.objects.get(id=id)
    target.target_follows = state
    target.save()
    do_reset(bot_id)
    return HttpResponse("success")

@login_required
def create_bot(request):
    data   = json.loads(request.body.decode('utf-8'))
    name = data['name']
    bot = Bot(name=name, state = 0)
    bot.save()
    return HttpResponse("success")

@login_required
def set_config(request, bot_id):
    if request.method == "POST":
        bot = Bot.objects.get(id=bot_id)
        username = request.POST.get("username")
        password = request.POST.get("password")
        like_per_day = request.POST.get("like_per_day")
        comment_per_day = request.POST.get("comment_per_day")
        follow_per_day = request.POST.get("follow_per_day")
        unfollow_per_day = request.POST.get("unfollow_per_day")
        second_username = request.POST.get("second_username")
        second_password = request.POST.get("second_password")
        comment_text = request.POST.get("comment_text")
        bot.username = username
        bot.password = password
        bot.like_per_day = int(like_per_day)
        bot.comment_per_day = int(comment_per_day)
        bot.follow_per_day = int(follow_per_day)
        bot.unfollow_per_day = int(unfollow_per_day)
        bot.second_username = second_username
        bot.second_password = second_password
        bot.comments = comment_text
        bot.state = 2
        bot.save()
        return redirect("/api/" + str(bot_id) + "/dashboard")