from lock_manager import *

class Scheduler:
    def __init__(self):
        self.schedule = ''
        self.waiting_requests = {}
        self.lock_manager = LockManager()
    
    def add_dict_helper(self, dictionary: dict, key, value):
        if key not in dictionary:
            dictionary[key] = [value]
        else:
            dictionary[key].append(value)

    def read(self, txn, obj):
        if self.lock_manager.get_read_lock(txn, obj):
            self.schedule += f"r{txn}({obj})"
            return True
        else:
            self.add_dict_helper(self.waiting_requests, txn, ('r', obj))
            return False
    
    def write(self, txn, obj):
        if self.lock_manager.get_write_lock(txn, obj):
            self.schedule += f"w{txn}({obj})"
            return True
        else:
            self.add_dict_helper(self.waiting_requests, txn, ('w', obj))
            return False
    
    def commit(self, txn):
        txn_locks = self.lock_manager.locks[txn]
        for (obj, lock) in txn_locks:
            if lock == LockType.WRITE:
                if not self.lock_manager.update_to_certify_lock(txn, obj):
                    self.add_dict_helper(self.waiting_requests, txn, ('c', None))
                    return False
        self.schedule += f"c{txn}"
        # release locks
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
                    self.waiting_requests[txn_waiting].remove((operation, obj))
        return True

    def get_schedule(self):
        return self.schedule
