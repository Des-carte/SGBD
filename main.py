from scheduler import Scheduler
import lock_manager as lm

raw_input = input('S = ')

# parser raw_input

requests = raw_input.split(' ') # p/ input separado por espaços

lock_manager = lm.LockManager()

scheduler = Scheduler()

for request in requests:
    try:
        operation = request[0]
        txn = request[1]
        obj = request[3]

        if operation == 'r':    # read
            scheduler.read(txn, obj)
        elif operation == 'w':  # write
            scheduler.write(txn, obj)
        else:                   # commit
            scheduler.commit(txn)
    except lm.DeadlockException as e:
        print(e)

print(scheduler.get_schedule())
