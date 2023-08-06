import time
import random
import ctypes
import threading

_thread_logid_map = {}

def _generate_logid():
    log_time = int(time.time()*1000)
    rand = random.randint(0, 2**63)
    return (log_time & 34359738367) << 28 | rand & 268435455

def _get_current_thread_id():
    current_thread_id = threading.current_thread()._native_id
    return current_thread_id

def get_logid():
    # get logid
    global _thread_logid_map
    current_thread_id = _get_current_thread_id()
    if current_thread_id not in _thread_logid_map.keys():
        log_id = _generate_logid()
        _thread_logid_map[current_thread_id] = log_id
    return _thread_logid_map[current_thread_id]

def release_logid():
    global _thread_logid_map
    current_thread_id = _get_current_thread_id()
    if current_thread_id not in _thread_logid_map.keys():
        return False
    del _thread_logid_map[current_thread_id]
    return True
