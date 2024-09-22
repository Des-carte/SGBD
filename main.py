from scheduler import Scheduler
import lock_manager as lm
from os import isatty
from sys import stdin

raw_input = input('S = ')

if not isatty(stdin.fileno()):
    print(raw_input)

# parser raw_input

requests = raw_input.split(' ') # p/ input separado por espaços

lock_manager = lm.LockManager()

scheduler = Scheduler()

for request in requests:
    try:
        operation = request[0]
        txn = request[1]

        if operation == 'r':    # read
            obj = request[3]
            scheduler.read(txn, obj)
        elif operation == 'w':  # write
            obj = request[3]
            scheduler.write(txn, obj)
        else:                   # commit
            scheduler.commit(txn)
    except lm.DeadlockException as e:
        print(e)

print(scheduler.get_schedule())
