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
            self.add_dict_helper(self.lock_manager.locks, txn, 'rl' + obj)
            self.schedule += f"r{txn}({obj})"
    
    def write(self, txn, obj):
        if self.lock_manager.get_write_lock(txn, obj):
            self.add_dict_helper(self.lock_manager.locks, txn, 'wl' + obj)
            self.schedule += f"w{txn}({obj})"
    
    def commit(self, txn):
        operation = f"c{txn}"
        txn_locks = self.lock_manager.locks[txn]
        for i, lock in enumerate(txn_locks):
            if lock[0] == 'w':
                if self.lock_manager.update_to_certify_lock(txn, lock[2]):
                    txn_locks[i] = 'cl'
        txn_locks = [x for x in txn_locks if x != 'cl']
        # free in LockManager (retirar vértice txn), retornar a vizinhança do vértice txn
            # para cada operation in waiting_requests da vizinha: executar operation
            
    def get_schedule(self):
        return self.schedule


