from scheduler import Scheduler
import lock_manager as lm
from parser import *
from os import isatty
from sys import stdin


raw_input = input('S = ')
requests = separate_operations(raw_input)
print(requests)

if not isatty(stdin.fileno()):
    print(raw_input)

scheduler = Scheduler()

for request in requests:
    try:
        operation = request[0]
        txn = request[1]
        obj = request[2]

        if operation == 'r':                    # read
            scheduler.read(txn, obj)
        elif operation == 'w':                  # write
            scheduler.write(txn, obj)
        elif operation == 'c':                   # commit
            scheduler.commit(txn)
    except lm.DeadlockException as e:
        print(e)

print(scheduler.get_schedule())
