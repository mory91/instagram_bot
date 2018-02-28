from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from api.models import Target
import json
from .util_functions import do_reset
from django.http import HttpResponse


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
def dashboard(request):
    targets = Target.objects.all()
    for t in targets:
        actions = t.target_action
        t.target_action = ""
        if "l" in actions:
            t.target_action = t.target_action + " Like "
        if "c" in actions:
            t.target_action = t.target_action + " Comment "
        if "f" in actions:
            t.target_action = t.target_action + " Follow "
    return render(request, "./panel/index.html", {"targets":targets})

@login_required
def add_target(request):
    data   = json.loads(request.body.decode('utf-8'))
    target_type = data["type"]
    target = data["target"]
    target_action = ""

    already = Target.objects.filter(target=target)
    
    if (len(already) > 0):
        return HttpResponse("already")

    if data["a_l"] == True:
        target_action = target_action + "l"
    if data["a_f"] == True:
        target_action = target_action + "f"
    if data["a_c"] == True:
        target_action = target_action + "c"
    t = Target(target=target, target_type=target_type, target_action=target_action)
    t.save()
    do_reset()
    return HttpResponse("success")

@login_required
def add_page_group(request):
    data   = json.loads(request.body.decode('utf-8'))
    target_type = 'P'
    targets = data["targets"]
    target_action = ""
    already_num = 0
    success_num = 0
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
        saving = Target(target=target_username, target_type=target_type, target_action=target_action)
        saving.save()
        success_num = success_num + 1
    do_reset()
    return JsonResponse({"already": already_num, "success": success_num})

@login_required
def delete_target(request, id):
    Target.objects.filter(id=id).delete()
    return redirect(dashboard)


