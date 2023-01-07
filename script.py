import datetime


def get_name(name):
    day = {'/Monday':1, '/Tuesday': 2, '/Thursday':4, '/Friday': 5}
    now_ = datetime.datetime.now()
    if day[name] < now_.isoweekday():
        result = now_ + datetime.timedelta(days=(7 - now_.isoweekday() + day[name]))
    else:
        result = now_ + datetime.timedelta(days=(day[name]-now_.isoweekday()))
    return f'{name} {result.strftime("%d.%m")}'

print(get_name('/Monday'))
print(get_name('/Friday'))

template = """НАзва події {0}

Вартість {1}"""


print(template.format(*('Event', '250')))