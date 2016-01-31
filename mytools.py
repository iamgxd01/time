import datetime


def get_now_time_object():

    dt = datetime.datetime.now()
    hour = dt.strftime("%H:%M").split(':')[0]
    minute = dt.strftime("%H:%M").split(':')[1]
    return datetime.time(int(hour), int(minute), 00)


def get_now_date_object():
    dt = datetime.datetime.now()
    year = dt.strftime('%Y-%m-%d').split('-')[0]
    month = dt.strftime('%Y-%m-%d').split('-')[1]
    day = dt.strftime('%Y-%m-%d').split('-')[2]
    return datetime.date(int(year), int(month), int(day))


def int_to_time_object(time_int):
    hour = time_int / 60
    minute = time_int % 60

    return datetime.time(int(hour), int(minute))
# print(get_now_time_object()-datetime.timedelta(seconds =60))
# print(get_now_time_object().hour)
# print(int_to_time_object(23))


def time_add_time(time1, time2):
    hour = time1.hour + time2.hour
    minute = time1.minute + time2.minute
    if minute >= 60:
        hour += 1
        minute -= 60
    if hour >= 24:
        hour -= 24
    return datetime.time(hour, minute)
# print(time_add_time(datetime.time(int(12), int(23)), datetime.time(int(13), int(20))))