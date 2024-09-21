# TODO: receber uma sequência de operações da forma ri(x)wj(z) p/ i, j > 0 junto com ci e cj representando o commit
# Usar regex (sugestão)
# - Retornar uma lista de objetos
# - Retornar uma lista de tuplas, em que cada tupla representa as operações de uma transação e a posição i da lista
#   se refere a transação i. (Essa estrutura pode ser parâmetro de uma função)

import re

def separate_operations(scheduler):
    pattern = r'([rwc])(\d+)\((\w+)\)|([c])(\d+)'
    operations = re.findall(pattern, scheduler)
    
    results = []
    for op in operations:
        if op[0]:
            type = op[0]
            transaction = op[1]
            resource = op[2]
            results.append((type, transaction, resource))
        elif op[3]:
            type = op[3]
            transaction = op[4]
            results.append((type, transaction, None))
    return results
