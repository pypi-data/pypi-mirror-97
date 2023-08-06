# Ourcompose
Is a framework for setup and running functions asynchronously in topological order. A simple example follows
```python

from ourcompose.framework import Piece, Dependency, Composition
    
async def fn_sum(n1: int, n2: int) -> int:
    return n1 + n2

async def fn_sub(n1: int, n2: int) -> int:
    return n1 - n2

async def fn_prod(n1: int, n2: int) -> int:
    return n1 * n2

async def fn_tolist(n_sum: int, n_sub: int, n_prod: int) -> list:
    return [n_sum, n_sub, n_prod]

n1, n2 = 1, 2
composition = Composition(
    id="comp-0",
    pieces=[
        Piece(
            id="sum",
            fn=fn_sum,
            inputs={"n1": n1, "n2": n2},
        ),
        Piece(
            id="sub",
            fn=fn_sub,
            inputs={"n1": n1, "n2": n2},
        ),
        Piece(
            id="prod",
            fn=fn_prod,
            inputs={"n1": n1, "n2": n2},
        ),
        Piece(
            id="tolist",
            fn=fn_tolist,
        )
    ],
    dependencies=[
        Dependency(
            piece_id="tolist", 
            dependent_on_id="sum", 
            connected_on="n_sum",
        ),
        Dependency(
            piece_id="tolist", 
            dependent_on_id="sub", 
            connected_on="n_sub",
        ),
        Dependency(
            piece_id="tolist", 
            dependent_on_id="prod", 
            connected_on="n_prod",
        ),
    ],
)

result = await composition.perform()
# >> {'fn_merge': [3, -1, 2], 'fn_prod': 2, 'fn_sub': -1, 'fn_sum': 3}
```