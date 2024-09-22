from scheduler import Scheduler
import lock_manager as lm
from parser import *

raw_input = input('S = ')
requests = separate_operations(raw_input)

scheduler = Scheduler()

for request in requests:
    try:
        operation = request[0]
        txn = request[1]
        obj = request[2]

        if operation == 'r':    # read
            scheduler.read(txn, obj)
        elif operation == 'w':  # write
            scheduler.write(txn, obj)
        else:                   # commit
            scheduler.commit(txn)
    except lm.DeadlockException as e:
        print(e)

print(scheduler.get_schedule())
