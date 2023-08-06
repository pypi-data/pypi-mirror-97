# bdd2dfa

[![Build Status](https://cloud.drone.io/api/badges/mvcisback/bdd2dfa/status.svg)](https://cloud.drone.io/mvcisback/bdd2dfa)
[![codecov](https://codecov.io/gh/mvcisback/bdd2dfa/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/bdd2dfa)
[![PyPI version](https://badge.fury.io/py/bdd2dfa.svg)](https://badge.fury.io/py/bdd2dfa)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple python wrapper around Binary Decision Diagrams (BDDs) to interpret them
as Deterministic Finite Automata (DFAs).

The package takes as input a BDD from the [`dd` package](https://github.com/tulip-control/dd)
and returns a DFA from the [`dfa` package](https://github.com/mvcisback/dfa).

Formally, the resulting `DFA` objects are quasi-reduced BDDs (QDDs)
where all leaves self loop and the label of states is a tuple: `(int, str | bool)`, where the first entry determines the number of inputs until this node is active and the second entry is the decision variable of the node or the BDD's truth assignment.


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)

<!-- markdown-toc end -->

# Installation

If you just need to use `bdd2dfa`, you can just run:

`$ pip install bdd2dfa`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

```python
# Create BDD

from dd import BDD

manager = BDD()
manager.declare('x', 'y', 'z')
x, y, z = map(manager.var, 'xyz')
bexpr = x & y & z


# Convert to DFA

from bdd2dfa import to_dfa

qdd = to_dfa(bexpr)

assert len(qdd.states()) == 7

# End at leaf node.
assert qdd.label([1, 1, 1]) == (0, True)
assert qdd.label([0, 1, 1]) == (0, False)

# End at Non-leaf node.
assert qdd.label([1, 1]) == (0, 'z')
assert qdd.label([0, 1]) == (1, False)

# leaf nodes are self loops.
assert qdd.label([1, 1, 1, 1]) == (0, True)
assert qdd.label([1, 1, 1, 1, 1]) == (0, True)
```

Each state of the resulting `DFA` object has three attribute:

1. `node`: A reference to the internal BDD node given by `dd`.
1. `parity`: `dd` supports Edge Negated `BDD`s, where some edges point
   to a Boolean function that is the negation of the Boolean function
   the node would point to in a standard `BDD`. Parity value determines
   whether or not the node 
1. `debt`: Number of inputs needed before this node can
   transition. Required since `BDD` edges can skip over irrelevant
   decisions.

For example,
```python
assert qdd.start.parity is True
assert qdd.start.debt == 0
assert qdd.start.node.var == 'x'
```

## BDD vs QDD

`to_dfa` also supports exporting a `BDD` rather than a `QDD`. This is done
by toggling the `qdd` flag.

```python
bdd = to_dfa(bexpr, qdd=False)
```

The `DFA` uses a similar state as the `QDD` case, but does not have a
`debt` attribute. Useful when one just wants to walk the `BDD`. 

**note** The labeling alphabet also only returns the decision variable/truth assignment.

If the `dfa` package was installed with the `draw` option, we can
visualize the difference between `qdd` and `bdd` by exporting to a
graphviz `dot` file.

```python
from dfa.draw import write_dot

write_dot(qdd, "qdd.dot")
write_dot(bdd, "bdd.dot")
```

Compiling using the `dot` command yields the following for `qdd.dot`

![qdd image](assets/qdd.svg)

and the following for `bdd.dot`:

![bdd image](assets/bdd.svg)
