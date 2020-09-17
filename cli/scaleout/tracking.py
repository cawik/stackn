import sys
import threading
from git import Repo
import time
import uuid

import scaleout.auth as sauth

global experiment_id
experiment_id = []

def start_function_log(f):
    # print('------------------------')
    print(f.__name__)
    print('------------------------')

def end_function_log():
    # print('------------------------')
    print('-----------END----------')
    # print('------------------------')

def log_experiment_id():
    print('Experiment id: {}'.format(experiment_id))

def log_project():
    stackn_config, load_status = sauth.get_stackn_config()
    print('Project: {}'.format(stackn_config['active_project']))

def log_param(name, value):
    print('{}:{}'.format(name, value))

def log_time(start_time, end_time):
    print('Start: {}'.format(start_time))
    print('End: {}'.format(end_time))
    print('Duration of call: {}'.format(end_time-start_time))

def log_git_repos():
    repo = None
    try:
        repo = Repo(search_parent_directories=True)
    except Exception as err:
        print("WARN: Did not find Git repository.")

    if repo:
        try:
            sha = repo.head.object.hexsha
            print('{}:{}'.format('Commit hash', sha))
        except:
            print("WARN: No commits found.")
        print('{}:{}'.format('Is dirty', repo.is_dirty()))

        for fname in repo.untracked_files:
            print('Untracked: {}'.format(fname))

def stackn_trace(f):

    sentinel = object()
    gutsdata = threading.local()
    gutsdata.captured_locals = None
    gutsdata.tracing = False
    def trace_locals(frame, event, arg):
        if event.startswith('c_'):  # C code traces, no new hook
            return 
        if event == 'call':  # start tracing only the first call
            if gutsdata.tracing:
                return None
            gutsdata.tracing = True
            return trace_locals
        if event == 'line':  # continue tracing
            return trace_locals

        # event is either exception or return, capture locals, end tracing
        gutsdata.captured_locals = frame.f_locals.copy()
        return None

    def wrapper(*args, **kw):
        global experiment_id
        # Log basics
        start_function_log(f)
        
        log_project()
        log_git_repos()

        # preserve existing tracer, start our trace
        old_trace = sys.gettrace()
        sys.settrace(trace_locals)

        retval = sentinel
        try:
            start_time = time.time()
            print('FUNCTION')
            retval = f(*args, **kw)
            print('END FUNCTION')
            if not experiment_id:
                # print('Init Experiment')
                experiment_id = uuid.uuid4().hex
            log_experiment_id()
            
            end_time = time.time()
            log_time(start_time, end_time)

        finally:
            # reinstate existing tracer, report, clean up
            sys.settrace(old_trace)
            print(f.__name__+str(args))
            # print(args)
            for key, val in gutsdata.captured_locals.items():
                if '_param' in key:
                    print('{}: {!r}'.format(key, val))
            if retval is not sentinel:
                print('Returned: {!r}'.format(retval))
            gutsdata.captured_locals = None
            gutsdata.tracing = False
        end_function_log()
        return retval

    return wrapper

# @stackn_trace
# def sub_func(a):
#     a = 2*a
#     bb_param = 122
#     # print('in sub_func')
#     return 32

# @stackn_trace
# def train(a, b):
#     a_param = a*b
#     b_param = 67
#     c_param = 'Hello World!'
#     d_var = a_param+b_param
#     b_param = d_var
#     sub_func(a_param)
#     return 'res'


# train(1,3)
