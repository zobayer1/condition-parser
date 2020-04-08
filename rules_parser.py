# -*- coding: utf-8 -*-
import json
from json.decoder import JSONDecodeError

""" Grammar Rules
##################################################
    cond := node
    node := ANY_node | ALL_node | VAL_node | leaf
    ANY_node := list(node) | node
    ALL_node := list(node) | node
    VAL_node := leaf
##################################################
"""

test_data = []

ANY, ALL, VAL = 'any', 'all', 'val'


def eval_val(node):
    # evaluate a leaf node, parsing based on application logic
    if type(node) is not str:
        raise SyntaxError(f'Illegal node: {node}')
    return node in test_data    


def eval_all(node):
    # AND logic parser
    logic_val = True
    if type(node) is not list:
        node = [node]
    for this_node in node:
        if type(this_node) is dict:
            if ANY in this_node:
                logic_val = logic_val & eval_any(this_node[ANY])
            elif ALL in this_node:
                logic_val = logic_val & eval_all(this_node[ALL])
            elif VAL in this_node:
                logic_val = logic_val & eval_val(this_node[VAL])
            else:
                raise SyntaxError(f'Illegal node: {node}')
        elif type(this_node) is str:
            logic_val = logic_val & eval_val(this_node)
        else:
            raise SyntaxError(f'Illegal node: {node}')
        if not logic_val:
            break
    return logic_val


def eval_any(node):
    # OR logic parser
    logic_val = False
    if type(node) is not list:
        node = [node]
    for this_node in node:
        if type(this_node) is dict:
            if ANY in this_node:
                logic_val = logic_val | eval_any(this_node[ANY])
            elif ALL in this_node:
                logic_val = logic_val | eval_all(this_node[ALL])
            elif VAL in this_node:
                logic_val = logic_val | eval_val(this_node[VAL])
            else:
                raise SyntaxError(f'Illegal node: {node}')
        elif type(this_node) is str:
            logic_val = logic_val | eval_val(this_node)
        else:
            raise SyntaxError(f'Illegal node: {node}')
        if logic_val:
            break
    return logic_val


def eval_rules(rules_file):
    with open(rules_file) as rules_input:
        print(f'Reading {rules_file}')
        rules_data = json.load(rules_input)
        print('Done')
        try:
            try:
                for index, rule in enumerate(rules_data['rules']):
                    cond = rule['cond']
                    if type(cond) is not dict and type(cond) is not str:
                        raise SyntaxError(f'Illegal node: {cond}')
                    print(f'Evaluating #{index}: {cond}')
                    logic_val = eval_any(cond)
                    
                    if logic_val:
                        print(f'\tPassed: Payload: {rule["payload"]}')
                    else:
                        print('\tFailed')
            except KeyError as err:
                raise SyntaxError(f'Invalid key: {str(err)}')
        except SyntaxError as err:
            print(f'SyntaxError: {str(err)}')


def read_data(data_file):
    with open(data_file) as data_input:
        print(f'Reading {data_file}')
        global test_data
        test_data = json.load(data_input).get('vals')
        print('Done')


if __name__ == '__main__':
    try:
        read_data('data.json')
        eval_rules('rules.json')
    except JSONDecodeError as err:
        print(f'Malformed JSON file')
