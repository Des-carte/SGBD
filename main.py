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

sch = scheduler.get_schedule()

print("Saída simples apresentada no laboratório:")
print("\n" + sch + "\n")
print("Saída longa apresentada no laboratório:")
print(scheduler.get_long_schedule() + "\n")

print("Saída simples filtrada|corrigida:")
print(output_filter(sch))