import networkx as nx
from enum import Enum

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
                    raise Exception
                return False
        self.locks[obj] = txn
        return True
    
    def get_read_lock(self, txn, obj):
        if obj in self.locks and self.locks[obj] != txn:
            self.waits_for_graph.add_edge(txn, self.locks[obj])
            if self.detect_deadlock():
                raise Exception
            return False
        self.locks[obj] = txn
        return True
    
    def get_certify_lock(self, txn, obj);
        return
