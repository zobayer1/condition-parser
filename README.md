Rule Based Condition Parser
===========================

A simple boolean condition parser engine.


Requirement
-----------

Python 3.7 or later


Input
-----

* A rule file. Example: [rules.json](rules.json)
* A data file. Example: [data.json](data.json)


Execution
---------

    python rules_parser.py


Grammar
-------

#### Parser engine follows the following grammar

    cond := node
    node := ANY_node | ALL_node | VAL_node | leaf
    ANY_node := list(node) | node
    ALL_node := list(node) | node
    VAL_node := leaf

#### Following are the example of nodes within the context of this denostration

### Leaf Node (leaf):

 A leaf node is a `string` object.

### Value Node (VAL_node)

A value node is a JSON object:

    {"val": leaf}

### ANY [OR] Node (ANY_node)

An ANY node is a JSON object:

    {"any": [...]}
    {"any": node}
    {"any": leaf}

### ALL [AND] Node (ALL_node)

An ALL node is a JSON object:

    {"all": [...]}
    {"all": node}
    {"all": leaf}

### Condition (cond)

A condition is a JSON object:

    {"cond": node}

### An Example Condition

    "cond": {
        "all": [
            "s1.q1.o1",
            {
                "any": [
                    "s2.q1.o1",
                    "s3.q1.o1"
                ]
            }
        ]
    }

This condition is equivalent to `"s1.q1.o1" AND ("s2.q1.o1" OR "s3.q1.o1")`

### Restrictions

1. Root node cannot be a list, as grammar dictates. Reason behind this is, without an ANY or ALL operator, we do not know how to evaluate the list.
2. By extension of #1, a list cannot be nested directly under another list. Only an ANY or an ALL node can contain a list of nodes.


Example Execution
-----------------

### Rule

The Rules file holds a list of all conditions in `rules` key. Each condition `cond` is associated with a `payload` that is selected if the condition succeeds.

    {
        "rules": [
            {
                "cond": {
                    "all": [
                        {
                            "any": [
                                "s2.q1.o1",
                                "s3.q1.o1"
                            ]
                        },
                        "s1.q1.o1"
                    ]
                },
                "payload": "payload 1"
            },
            {
                "cond": {
                    "any": {
                        "all": "s3.q1.o1"
                    }
                },
                "payload": "payload 2"
            },
            {
                "cond": {
                    "val": "s2.q1.o1"
                },
                "payload": "payload 3"
            }
        ]
    }

### Data

In this demosntration, the data file will hold a list of values in `vals` key, which will be used for binary evaluation (exists or not).

    {
        "vals": ["s1.q1.o1", "s2.q1.o1"]
    }

### Run

Running in a terminal, we may get this output

    $ python rules_parser.py
    Reading data.json
    Done
    Reading rules.json
    Done
    Evaluating #0: {'all': ['s1.q1.o1', {'any': ['s2.q1.o1', 's3.q1.o1']}]}
            Passed: Payload: payload 1
    Evaluating #1: {'any': 's3.q1.o1'}
            Failed
    Evaluating #2: {'val': 's2.q1.o1'}
            Passed: Payload: payload 3

### Errors

Program will report various types of syntax errors if it doesn't like how you formed the conditions, i.e. if you didn't follow the grammar.


Modifications
-------------

1. Definition of leaf nodes can be easily changed.
2. JSON file reading can easily be replaced by any other IO method.
3. Payload can be replaced with a more complex JSON node, or even multiple keys.
4. Leaf evaluation can be modified as required by usage.


Trivia
------

1. Condition can contain indefinite amount of nesting.
2. Boolean pruning is present, does not traverse unnecessary nodes.


Author
------

1. [Zobayer Hasan](mailto:zobayer@tigeritbd.com)


License
-------

[MIT License](LICENSE)
