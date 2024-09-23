from scheduler import Scheduler
import lock_manager as lm
from parser import *
from os import isatty
from sys import stdin


raw_input = input('S=')
requests = separate_operations(raw_input)

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
        elif operation == 'c':                  # commit
            scheduler.commit(txn)
    except lm.DeadlockException as e:
        print(e)
        scheduler.abort(e.most_recent_txn)
        print(f"Transaction {e.most_recent_txn} aborted")

#print('  ' + scheduler.get_schedule())
#print(scheduler.get_long_schedule())

sch = scheduler.get_schedule()

ops = separate_operations(sch)

listed = []

for op in ops:
    operation = op[0]
    txn = op[1]
    if operation == 'c':
        listed.append(txn)

schedule = ''

for op in ops:
    operation = op[0]
    txn = op[1]
    obj = op[2]

    if txn in listed:
        if obj != None:
            schedule += f"{operation}{txn}({obj})"
        else:
            schedule += f"{operation}{txn}"


print(schedule)