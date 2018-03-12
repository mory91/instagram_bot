from .models import Reset, Bot      

def do_reset(bot_id):
    b = Bot.objects.get(id=bot_id)
    r = Reset(bot=b)
    r.save()