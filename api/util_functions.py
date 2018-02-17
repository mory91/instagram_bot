from .models import Reset

def do_reset():
    r = Reset()
    r.save()