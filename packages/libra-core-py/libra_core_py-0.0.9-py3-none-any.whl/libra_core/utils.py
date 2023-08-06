import json
import time
import hashlib
import datetime

def dump_json(data):
    return json.dumps(data, ensure_ascii=False)


def load_json(data):
    try:
        return json.loads(data)
    except:
        return None


def sleep(seconds):
    time.sleep(seconds)


def get_current_millisecond():
    return int(round(time.time() * 1000))


def get_current_second():
    return int(round(time.time()))


def timestamp_to_str(timestamp=None, format='%Y-%m-%d %H:%M:%S'):
    if timestamp:
        if len(str(timestamp)) > 10:
            timestamp = timestamp / (10 ** (len(str(timestamp))-10))
        time_tuple = time.localtime(timestamp)
        result = time.strftime(format, time_tuple)
        return result
    else:
        return time.strptime(format)

def str_to_timestamp(str_time=None, format='%Y-%m-%d %H:%M:%S'):
    if str_time:
        time_tuple = time.strptime(str_time, format)
        result = time.mktime(time_tuple)
        return int(result)
    return int(time.time())

def md5(src):
    m2 = hashlib.md5()
    m2.update(src.encode())
    return m2.hexdigest()

def get_current_datetime():
    return datetime.datetime.now()
