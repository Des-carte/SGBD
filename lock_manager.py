import networkx as nx
from enum import Enum

class DeadlockException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        return f"Deadlock found when {self.args[0]}"

# A classe deve lançar uma exceção sempre que ocorrer um deadlock
class LockManager:
    # uma estrutura que dado um objeto(obj - x, y, z, ...), mostre seus bloqueios e a transação(txn) correspondente
    
    def __init__(self):
        waits_for_graph = nx.DiGraph()
        self.locks = {}

    def get_write_lock(self, txn, obj):
        if obj in self.locks:
            if self.locks[obj] != txn:
                self.waits_for_graph.add_edge(txn, self.locks[obj])
                if self.detect_deadlock():
                    raise DeadlockException("trying to get lock from ...")
                return False
        self.locks[obj] = txn
        return True
    
    def get_read_lock(self, txn, obj):
        if obj in self.locks and self.locks[obj] != txn:
            self.waits_for_graph.add_edge(txn, self.locks[obj])
            if self.detect_deadlock():
                raise DeadlockException("trying to get lock from ...")
            return False
        self.locks[obj] = txn
        return True
    
    def update_to_certify_lock(self, txn, obj):
        return
