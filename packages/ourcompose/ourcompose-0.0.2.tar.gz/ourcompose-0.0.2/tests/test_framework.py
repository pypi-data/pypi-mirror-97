from unittest import IsolatedAsyncioTestCase

from ourcompose.framework import Composition, Piece, Dependency

class TestFramework(IsolatedAsyncioTestCase):

    def test_define_piece_will_raise_error_with_no_fn_input(self):

        def my_fn():
            return None

        self.assertRaises(
            Exception,
            Piece,
            id="my-piece",
            fn=my_fn,
        )

    def test_define_piece_will_raise_error_with_fn_input_without_type(self):

        def my_fn(inp):
            return None

        self.assertRaises(
            Exception,
            Piece,
            id="my-piece",
            fn=my_fn,
        )

    def test_define_piece_will_raise_error_with_invalid_fn_input(self):

        class MyInputCls():
            pass

        def my_fn(inp: MyInputCls):
            return None

        self.assertRaises(
            Exception,
            Piece,
            id="my-piece",
            fn=my_fn,
        )

    def test_define_piece_will_succeed(self):

        class MyInputCls():
            pass
        
        class MyOutputCls():
            pass

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            return None

        try:
            Piece(
                id="my-piece",
                fn=my_fn,
            )
        except Exception as e:
            self.fail(e)

    def test_define_piece_with_input_as_super_class_should_succeed(self):

        class MySuperSuperClass():
            pass

        class MySuperClass(MySuperSuperClass):
            pass

        class MyInputCls(MySuperClass):
            pass
        
        class MyOutputCls(MySuperClass):
            pass

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            return None

        try:
            Piece(
                id="my-piece",
                fn=my_fn,
            )
        except Exception as e:
            self.fail(e)

    def test_runtime_piece_with_invalid_input(self):

        class MyInputCls():
            pass

        class MyOutputCls():
            pass

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            pass

        piece = Piece(
            id="my-piece",
            fn=my_fn,
        )

        self.assertRaises(
            Exception,  
            piece.__verify_fn_inputs__,
            fn=piece.fn,
            actual_input={}
        )

    def test_runtime_piece_with_valid_input(self):

        class MyInputCls():
            def __init__(self, data) -> None:
                super().__init__()
                self.data=data

        class MyOutputCls():
            pass

        def my_fn(inp: MyInputCls):
            pass

        piece = Piece(
            id="my-piece",
            fn=my_fn,
        )

        try:
            piece.__verify_fn_inputs__(piece.fn, [MyInputCls(data={})])
        except Exception as e:
            self.fail(e)

    def test_runtime_piece_with_invalid_output(self):

        class MyInputCls():
            pass

        class MyOutputCls():
            pass

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            pass

        piece = Piece(
            id="my-piece",
            fn=my_fn,
        )

        self.assertRaises(
            Exception,  
            piece.__verify_fn_output__,
            fn=piece.fn,
            actual_output={}
        )

    def test_runtime_piece_with_valid_input(self):

        class MyInputCls():
            pass

        class MyOutputCls():
            def __init__(self, data) -> None:
                super().__init__()
                self.data=data

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            pass

        piece = Piece(
            id="my-piece",
            fn=my_fn,
        )

        try:
            piece.__verify_fn_output__(piece.fn, MyOutputCls(data={}))
        except Exception as e:
            self.fail(e)

    def test_define_piece_with_invalid_output_type(self):

        class MyInputCls():
            pass

        class MyOutputCls():
            pass

        def my_fn(inp: MyInputCls):
            pass

        self.assertRaises(
            Exception,
            Piece,
            id="my-piece",
            fn=my_fn,
            input_classes=[MyInputCls],
            output_class=MyOutputCls,
        )

    def test_define_piece_with_valid_output_type(self):

        class MyInputCls():
            pass

        class MyOutputCls():
            pass

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            pass

        try:
            Piece(
                id="my-piece",
                fn=my_fn,
            )
        except Exception as e:
            self.fail(e)

    def test_define_piece_with_multiple_input_types(self):

        class MyInputCls1():
            pass

        class MyInputCls2():
            pass

        class MyOutputCls():
            pass

        def my_fn(inp1: MyInputCls1, inp2: MyInputCls2) -> MyOutputCls:
            pass

        try:
            Piece(
                id="my-piece",
                fn=my_fn,
            )
        except Exception as e:
            self.fail(e)

    def test_perform_piece_with_valid_input_type(self):

        class MyInputCls():
            pass

        class MyOutputCls():
            pass

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            return MyOutputCls()

        try:
            piece = Piece(
                id="my-piece",
                fn=my_fn,
            )
            piece.perform({"inp": MyInputCls()})
        except Exception as e:
            self.fail(e)

    def test_perform_piece_with_valid_output_type(self):

        class MyInputCls():
            pass

        class MyOutputCls():
            pass

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            return MyOutputCls()

        try:
            piece = Piece(
                id="my-piece",
                fn=my_fn,
            )
            piece.perform({"inp": MyInputCls()})
        except Exception as e:
            self.fail(e)

    async def test_perform_piece_with_invalid_input_type(self):

        class MyInputCls():
            pass

        class MyOutputCls():
            pass

        class InvalidInputType:
            pass

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            pass

        try:
            piece = Piece(
                id="my-piece",
                fn=my_fn,
            )
        except Exception as e:
            self.fail(e)

        with self.assertRaises(Exception):
            await piece.perform(input=InvalidInputType())

    async def test_perform_piece_with_invalid_output_type(self):

        class MyInputCls():
            pass

        class MyOutputCls():
            pass

        class InvalidOutputType:
            pass

        def my_fn(inp: MyInputCls) -> MyOutputCls:
            return InvalidOutputType()

        try:
            piece = Piece(
                id="my-piece",
                fn=my_fn,
            )
        except Exception as e:
            self.fail(e)

        with self.assertRaises(Exception):
            await piece.perform(input=MyInputCls())

    async def test_perform_piece_with_valid_input_and_output(self):

        class MyInputCls():

            def __init__(self, add1: int, add2: int) -> None:
                super().__init__()
                self.add1 = add1
                self.add2 = add2

        class MyOutputCls():

            def __init__(self, _sum: int) -> None:
                super().__init__()
                self.sum = _sum

        async def sum_fn(inp: MyInputCls) -> MyOutputCls:
            return MyOutputCls(inp.add1 + inp.add2)

        try:
            piece = Piece(
                id="my-piece",
                fn=sum_fn,
            )
            out = await piece.perform(
                input={
                    "inp": MyInputCls(
                        add1=1,
                        add2=2,
                    )
                }
            )
            self.assertEqual(out.sum, 3)
        except Exception as e:
            self.fail(e)

    async def test_perform_piece_with_inverse_order_of_inputs(self):

        class MyInputCls1():
            def __init__(self, number: int):
                self.number=number

        class MyInputCls2():
            def __init__(self, number: int):
                self.number=number

        class MyOutputCls():
            def __init__(self, _sum) -> None:
                self.sum = _sum

        async def my_fn(inp1: MyInputCls1, inp2: MyInputCls2) -> MyOutputCls:
            return MyOutputCls(inp1.number - inp2.number)

        try:
            piece = Piece(
                id="my-piece",
                fn=my_fn,
            )
            out1 = await piece.perform(
                {
                    "inp1": MyInputCls1(number=1),
                    "inp2": MyInputCls2(number=2),
                }
            )
            self.assertEqual(out1.sum, -1)
            
            out2 = await piece.perform(
                {
                    "inp2": MyInputCls2(number=2),
                    "inp1": MyInputCls1(number=1),
                }
            )
            self.assertEqual(out2.sum, -1)
        except Exception as e:
            self.fail(e)

    async def test_perform_piece_with_too_many_inputs_should_succeed(self):

        async def concat_dicts(inp1: dict, inp2: dict) -> dict:
            return {**inp1, **inp2}

        piece = Piece(
            id="concat-piece",
            fn=concat_dicts,
        )

        try:
            result = await piece.perform(
                input={
                    "inp1": {"a": 1, "b": 2},
                    "inp2": {"c": 1, "d": 2},
                    "inp3": {"a": 2, "b": 3},
                    "inp4": {"c": 2, "d": 3},
                }
            )
            self.assertEqual(result, {"a": 1, "b": 2, "c": 1, "d": 2})
        except Exception as e:
            self.fail(e)

    async def test_perform_pieces_with_simple_dependency_for_composition(self):

        async def perform_piece_1(arg: list) -> dict:
            return {k:k for k in arg}

        async def perform_piece_2(arg: list) -> list:
            return [k+1 for k in arg]

        composition = Composition(
            id="comp-0",
            pieces=[
                Piece(
                    id="piece-1",
                    fn=perform_piece_1,
                ),
                Piece(
                    id="piece-2",
                    fn=perform_piece_2,
                    inputs={
                        'arg': [1,2,3],
                    },
                ),
            ],
            dependencies=[
                Dependency(
                    piece_id="piece-1", 
                    dependent_on_id="piece-2",
                    connected_on="arg",
                )
            ]
        )

        try:
            composition_result = await composition.perform()
            self.assertEqual(len(composition_result), 2)
            self.assertEqual(composition_result['piece-1'], {2:2, 3:3, 4:4})
        except Exception as e:
            self.fail(e)

    async def test_perform_pieces_with_multiple_input_dependencies_for_composition(self):

        async def perform_piece_1(arg: list) -> list:
            return [k for k in arg]

        async def perform_piece_2(arg: list) -> list:
            return [k+1 for k in arg]

        async def perform_piece_3(arg1: list, arg2: list) -> list:
            return [i+j for i,j in zip(arg1, arg2)]

        composition = Composition(
            id="comp-0",
            pieces=[
                Piece(
                    id="piece-1",
                    fn=perform_piece_1,
                    inputs={
                        'arg': [1,2,3],
                    },
                ),
                Piece(
                    id="piece-2",
                    fn=perform_piece_2,
                    inputs={
                        'arg': [1,2,3],
                    },
                ),
                Piece(
                    id="piece-3",
                    fn=perform_piece_3,
                )
            ],
            dependencies=[
                Dependency(
                    piece_id="piece-3", 
                    dependent_on_id="piece-1",
                    connected_on="arg1",
                ),
                Dependency(
                    piece_id="piece-3", 
                    dependent_on_id="piece-2",
                    connected_on="arg2",
                ),
            ]
        )

        try:
            composition_result = await composition.perform()
            self.assertEqual(len(composition_result), 3)
            self.assertEqual(composition_result['piece-3'], [3, 5, 7])
        except Exception as e:
            self.fail(e)

    async def test_perform_pieces_with_one_dependency_argument_into_many_pieces(self):

        async def fn_0(inp: dict) -> dict:
            return inp

        async def fn_1a(inp: dict) -> dict:
            return {**inp, **{'b': 1}}

        async def fn_1b(inp: dict) -> dict:
            return {**inp, **{'c': 1}}

        composition = Composition(
            id="comp-0",
            pieces=[
                Piece(
                    id="p0",
                    fn=fn_0,
                    inputs={
                        "inp": {"a": 1},
                    },
                ),
                Piece(
                    id="p1a",
                    fn=fn_1a,
                ),
                Piece(
                    id="p1b",
                    fn=fn_1b,
                ),
            ],
            dependencies=[
                Dependency(
                    piece_id="p1a", 
                    dependent_on_id="p0", 
                    connected_on="inp",
                ),
                Dependency(
                    piece_id="p1b", 
                    dependent_on_id="p0", 
                    connected_on="inp",
                ),
            ],
        )

        try:
            result = await composition.perform()
            self.assertEqual({'a': 1, 'b': 1}, result['p1a'])
            self.assertEqual({'a': 1, 'c': 1}, result['p1b'])
        except Exception as e:
            self.fail(e)

    async def test_perform_pieces_with_composition_with_throwing_errors(self):

        async def fn_0(inp: dict) -> dict:
            raise Exception("Did raise exception!")

        composition = Composition(
            id="comp-0",
            pieces=[
                Piece(
                    id="p0",
                    fn=fn_0,
                    inputs={
                        "inp": {"a": 1},
                    },
                )
            ],
        )

        try:
            result = await composition.perform()
            self.assertTrue(isinstance(result['p0'], Exception))
        except Exception as e:
            self.fail(e)

    async def test_perform_shallow_composition_chaining(self):

        async def fn_0(inp: dict) -> dict:
            return inp

        async def fn_1(inp: dict) -> dict:
            return inp

        composition_joint = Composition(
            id="comp-joint",
            pieces=[
                Composition(
                    id="comp-0",
                    pieces=[
                        Piece(
                            id="p0",
                            fn=fn_0,
                            inputs={
                                "inp": {"a": 1},
                            },
                        )
                    ],
                ),
                Composition(
                    id="comp-1",
                    pieces=[
                        Piece(
                            id="p1",
                            fn=fn_1,
                            inputs={
                                "inp": {"b": 2},
                            },
                        )
                    ],
                ),
            ],
        )

        try:
            result = await composition_joint.perform()
            self.assertEqual(result['comp-0']['p0']['a'], 1)
            self.assertEqual(result['comp-1']['p1']['b'], 2)
        except Exception as e:
            self.fail(e)

    async def test_perform_deep_composition_chaining(self):

        async def fn_0(inp: dict) -> dict:
            return inp

        async def fn_1(inp: dict) -> dict:
            return inp

        composition_joint = Composition(
            id="comp-joint",
            pieces=[
                Composition(
                    id="comp-0",
                    pieces=[
                        Composition(
                            id="comp-joint",
                            pieces=[
                                Composition(
                                    id="comp-0",
                                    pieces=[
                                        Piece(
                                            id="p0",
                                            fn=fn_0,
                                            inputs={
                                                "inp": {"a": 1},
                                            },
                                        )
                                    ],
                                ),
                                Composition(
                                    id="comp-1",
                                    pieces=[
                                        Piece(
                                            id="p1",
                                            fn=fn_1,
                                            inputs={
                                                "inp": {"b": 2},
                                            },
                                        )
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                Composition(
                    id="comp-1",
                    pieces=[
                        Composition(
                            id="comp-joint",
                            pieces=[
                                Composition(
                                    id="comp-0",
                                    pieces=[
                                        Piece(
                                            id="p0",
                                            fn=fn_0,
                                            inputs={
                                                "inp": {"a": 1},
                                            },
                                        )
                                    ],
                                ),
                                Composition(
                                    id="comp-1",
                                    pieces=[
                                        Piece(
                                            id="p1",
                                            fn=fn_1,
                                            inputs={
                                                "inp": {"b": 2},
                                            },
                                        )
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
            ],
        )

        try:
            result = await composition_joint.perform()
        except Exception as e:
            self.fail(e)

    async def test_simple_concurrent_mathematical_calculations(self):

        async def fn_sum(n1: int, n2: int) -> int:
            return n1 + n2

        async def fn_sub(n1: int, n2: int) -> int:
            return n1 - n2

        async def fn_prod(n1: int, n2: int) -> int:
            return n1 * n2

        async def fn_merge(n_sum: int, n_sub: int, n_prod: int) -> list:
            return [n_sum, n_sub, n_prod]

        n1, n2 = 1, 2
        composition = Composition(
            id="comp-0",
            pieces=[
                Piece(
                    id="fn_sum",
                    fn=fn_sum,
                    inputs={"n1": n1, "n2": n2},
                ),
                Piece(
                    id="fn_sub",
                    fn=fn_sub,
                    inputs={"n1": n1, "n2": n2},
                ),
                Piece(
                    id="fn_prod",
                    fn=fn_prod,
                    inputs={"n1": n1, "n2": n2},
                ),
                Piece(
                    id="fn_merge",
                    fn=fn_merge,
                )
            ],
            dependencies=[
                Dependency(
                    piece_id="fn_merge", 
                    dependent_on_id="fn_sum", 
                    connected_on="n_sum",
                ),
                Dependency(
                    piece_id="fn_merge", 
                    dependent_on_id="fn_sub", 
                    connected_on="n_sub",
                ),
                Dependency(
                    piece_id="fn_merge", 
                    dependent_on_id="fn_prod", 
                    connected_on="n_prod",
                ),
            ],
        )

        try:
            result = await composition.perform()
            self.assertIn(3, result['fn_merge'])
            self.assertIn(-1, result['fn_merge'])
            self.assertIn(2, result['fn_merge'])
        except Exception as e:
            self.fail(e)