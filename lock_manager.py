import networkx as nx
from enum import Enum

class LockType(Enum):
    READ = 1
    WRITE = 2
    CERTIFY = 3

class DeadlockException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        return f"Deadlock found when {self.args[0]}"

class LockManager:
    def __init__(self):
        waits_for_graph = nx.DiGraph()
        self.locks = {}

    def get_write_lock(self, txn, obj):
        if obj in self.locks:
            for transaction, lock_type in self.locks[obj].items():
                if transaction != txn:
                    self.waits_for_graph.add_edge(txn, transaction)
                    if self.detect_deadlock():
                        raise DeadlockException(f"trying to get write lock on {obj}")
                    return False
        if obj not in self.locks:
            self.locks[obj] = {}
        self.locks[obj][txn] = LockType.WRITE
        return True
    
    def get_read_lock(self, txn, obj):
        if obj in self.locks:
            for transaction, lock_type in self.locks[obj].items():
                if transaction != txn and lock_type != LockType.READ:
                    self.waits_for_graph.add_edge(txn, transaction)
                    if self.detect_deadlock():
                        raise DeadlockException(f"trying to get read lock on {obj}")
                    return False
        if obj not in self.locks:
            self.locks[obj] = {}
        self.locks[obj][txn] = LockType.READ
        return True
    
    def get_certify_lock(self, txn, obj):
        if obj in self.locks:
            for transaction, lock_type in self.locks[obj].items():
                if transaction != txn:
                    self.waits_for_graph.add_edge(txn, transaction)
                    if self.detect_deadlock():
                        raise DeadlockException(f"trying to get certify lock on {obj}")
                    return False
        if obj not in self.locks:
            self.locks[obj] = {}
        self.locks[obj][txn] = LockType.CERTIFY
        return True

    def update_to_certify_lock(self, txn, obj):
        if obj in self.locks and txn in self.locks[obj]:
            self.locks[obj][txn] = LockType.CERTIFY

    def detect_deadlock(self):
        try:
            cycle = nx.find_cycle(self.waits_for_graph, orientation='original')
            return True
        except nx.NetworkXNoCycle:
            return False
        
