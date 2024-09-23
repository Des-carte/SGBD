from lock_manager import *

class Scheduler:
    def __init__(self):
        self.schedule = ''
        self.long_schedule = ''
        # Dado uma transação, mostra a lista de operações esperando por ela
        self.waiting_requests = {}
        self.pending = {}
        self.lock_manager = LockManager()
    
    def add_dict_helper(self, dictionary: dict, key, value):
        if key not in dictionary:
            dictionary[key] = [value]
        else:
            dictionary[key].append(value)

    def read(self, txn, obj):
        conflit_txn = self.lock_manager.get_read_lock(txn, obj)
        if conflit_txn is None:
            self.schedule += f"r{txn}({obj})"
            self.long_schedule += f"rl{txn}({obj})r{txn}({obj})"
            return True
        else:
            self.add_dict_helper(self.waiting_requests, conflit_txn, ('r', txn, obj))
            self.pending[txn] = True
            return False
    
    def write(self, txn, obj):
        conflit_txn = self.lock_manager.get_write_lock(txn, obj)
        if conflit_txn is None:
            self.schedule += f"w{txn}({obj})"
            self.long_schedule += f"wl{txn}({obj})w{txn}({obj})"
            return True
        else:
            self.add_dict_helper(self.waiting_requests, conflit_txn, ('w', txn, obj))
            self.pending[txn] = True
            return False
    
    def commit(self, txn):
        if txn not in self.lock_manager.locks:
            return False
        #if txn in self.pending and self.pending[txn] == True:
        #    return False
        txn_locks = self.lock_manager.locks[txn]

        for (obj, lock) in txn_locks:
            if lock == LockType.WRITE:
                conflit_txn = self.lock_manager.try_update_to_certify_lock(txn, obj)
                if conflit_txn is not None:
                    self.add_dict_helper(self.waiting_requests, conflit_txn, ('c', txn, None))
                    return False

                if not self.lock_manager.update_to_certify_lock(txn, obj):
                    return False
        self.schedule += f"c{txn}"
        self.long_schedule += f"c{txn}"
        # release locks
        for (obj, _) in txn_locks:
            self.long_schedule += f"u{txn}({obj})"
        self.lock_manager.free_locks(txn)
        self.pending[txn] = False

        txns_waiting = self.waiting_requests[txn] if txn in self.waiting_requests else []
        
        for (operation, txn_waiting, obj) in txns_waiting:
            success = False
            if operation == 'w':
                success = self.write(txn_waiting, obj)
            elif operation == 'r':
                success = self.read(txn_waiting, obj)
            else:
                success = self.commit(txn_waiting)
            if success:
                txns_waiting.remove((operation, txn_waiting, obj))
        return True
    
    def abort(self, txn):
        self.lock_manager.waits_for_graph.remove_node(txn)
        self.lock_manager.free_locks(txn)

        txns_waiting = self.waiting_requests[txn] if txn in self.waiting_requests else []

        for (operation, txn_waiting, obj) in txns_waiting:
            success = False
            if operation == 'w':
                success = self.write(txn_waiting, obj)
            elif operation == 'r':
                success = self.read(txn_waiting, obj)
            else:
                success = self.commit(txn_waiting)
            if success:
                txns_waiting.remove((operation, txn_waiting, obj))
 

    def get_schedule(self):
        return self.schedule

    def get_long_schedule(self):
        return self.long_schedule


