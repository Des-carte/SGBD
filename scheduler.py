from lock_manager import *

class Scheduler:
    def __init__(self):
        self.schedule = ''
        self.waiting_requests = {}
        self.lock_manager = LockManager()
        # Associa uma transação aos seus locks
        self.locks = {}
    
    def add_dict_helper(self, dictionary: dict, key, value):
        if key not in dictionary:
            dictionary[key] = [value]
        else:
            dictionary[key].append(value)

    def read(self, txn, obj):
        if self.lock_manager.get_read_lock(txn, obj):
            self.add_dict_helper(self.locks, txn, (LockType.READ, obj))
            self.schedule += f"r{txn}({obj})"
            return True
        else:
            self.add_dict_helper(self.waiting_requests, txn, ('r', obj))
            return False
    
    def write(self, txn, obj):
        if self.lock_manager.get_write_lock(txn, obj):
            self.add_dict_helper(self.locks, txn, (LockType.WRITE, obj))
            self.schedule += f"w{txn}({obj})"
            return True
        else:
            self.add_dict_helper(self.waiting_requests, txn, ('w', obj))
            return False
    
    def commit(self, txn):
        operation = f"c{txn}"
        txn_locks = self.locks[txn]
        for i, (lock, obj) in enumerate(txn_locks):
            if lock == LockType.WRITE:
                if self.lock_manager.update_to_certify_lock(txn, obj):
                    txn_locks[i] = (LockType.CERTIFY, obj)
                else:
                    self.add_dict_helper(self.waiting_requests, txn, ('c', None))
                    return False
        # release certify locks
        txn_locks = [(lock, obj) for (lock, obj) in txn_locks if lock != LockType.CERTIFY]
        txns_waiting = self.lock_manager.free_locks(txn)
        for txn_waiting in txns_waiting:
            for (operation, obj) in self.waiting_requests[txn_waiting]:
                success = False
                if operation == 'w':
                    success = self.write(txn_waiting, obj)
                elif operation == 'r':
                    success = self.read(txn_waiting, obj)
                else:
                    success = self.commit(txn_waiting)
                if success:
                    self.waiting_requests[txn_waiting].remove((txn_waiting, obj))
        return True

    def get_schedule(self):
        return self.schedule


