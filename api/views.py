from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from api.models import Target
from .util_functions import do_reset

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
    target_type = request.POST.get("type")
    target = request.POST.get("name")
    target_action = ""
    if request.POST.get("action_l"):
        target_action = target_action + "l"
    if request.POST.get("action_f"):
        target_action = target_action + "f"
    if request.POST.get("action_c"):
        target_action = target_action + "c"
    print(target_action)
    t = Target(target=target, target_type=target_type, target_action=target_action)
    t.save()
    do_reset()
    return redirect(dashboard)

@login_required
def delete_target(request, id):
    Target.objects.filter(id=id).delete()
    return redirect(dashboard)


