def print_log(message):
    print(message.toString(), flush=True)

def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)