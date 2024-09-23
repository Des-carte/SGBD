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

def output_filter(scheduler):
    ops = separate_operations(scheduler)
    commited_txn_list = []
    for op in ops:
        operation = op[0]
        txn = op[1]
        if operation == 'c':
            commited_txn_list.append(txn)

    output_schedule = ''
    for op in ops:
        operation = op[0]
        txn = op[1]
        obj = op[2]
        if txn in commited_txn_list:
            if obj != None:
                output_schedule += f"{operation}{txn}({obj})"
            else:
                output_schedule += f"{operation}{txn}"
    
    return output_schedule
