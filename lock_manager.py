import networkx as nx
from enum import Enum

# A classe deve lançar uma exceção sempre que ocorrer um deadlock
class LockManager:
    waits_for_graph = nx.DiGraph()
    # uma estrutura que dado um objeto(obj - x, y, z, ...), mostre seus bloqueios e a transação(txn) correspondente
    
    def __init__(self):
        return

    def get_write_lock(txn, obj):
        return
    
    def get_read_lock(txn, obj):
        return
    
    def get_certify_lock(txn, obj);
        return
