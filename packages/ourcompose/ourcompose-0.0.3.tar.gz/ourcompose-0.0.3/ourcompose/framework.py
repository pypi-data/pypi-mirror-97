import abc
import asyncio
import inspect
import time
from typing import Callable, Dict, Any, List
from toposort import toposort

class Perform(object):

    def __init__(self) -> None:
        super().__init__()
        self.execution_time = None

    @abc.abstractclassmethod
    async def fn(self, input: Dict[str, Any]) -> Any:
        raise NotImplementedError()

    @staticmethod
    def __verify_fn_inputs__(fn: Callable, actual_input: Dict[str, Any]):
        """
            Verify input type of fn such that the actual input has same type.
        """

        for k, param in dict(inspect.signature(fn).parameters).items():
            if not k in actual_input:
                raise Exception(f"Argument '{k}' is missing when computing function {fn}")
            
            actual_input_type = type(actual_input[k])
            expected_input_type = param._annotation
            if not actual_input_type == expected_input_type:
                raise TypeError(f"For function {fn}: Expected input type {expected_input_type} but got {actual_input_type}.")

    @staticmethod
    def __verify_fn_output__(fn: Callable, acutal_output: Any):
        """
            Verify return type of fn such that the output has same type.
        """
        expected_output_type = inspect.signature(fn).return_annotation
        actual_output_type = type(acutal_output)
        try:
            if not expected_output_type == Any:
                if not expected_output_type.__name__ == actual_output_type.__name__:
                    raise TypeError(
                        f"For function {fn}: Expected output type was {expected_output_type} but got {actual_output_type}."
                    )
        except Exception as e:
            raise Exception(f"Could not type check output for function {fn}: {e}")

    async def __timeit__(self, async_method):
        tic = time.time()
        result = await async_method
        self.execution_time = time.time() - tic
        return result

    @staticmethod
    def _fit_input_kwargs_from_fn(fn: Callable, input: Dict[str, Any]):
        fn_keys = dict(inspect.signature(fn).parameters)
        return {k:v for k, v in input.items() if k in fn_keys}
            
    async def perform(self, input: Dict[str, Any] = {}) -> Any:
        Piece.__verify_fn_inputs__(self.fn, actual_input=input)
        output = await self.__timeit__(
            async_method=self.fn(**self._fit_input_kwargs_from_fn(self.fn, input))
        )
        Piece.__verify_fn_output__(self.fn, acutal_output=output)
        return output

class Piece(Perform):

    def __init__(self, id: str, fn: Callable, inputs: dict = {}) -> None:
        super().__init__()
        Piece.__validate_fn_input__(fn=fn)
        Piece.__validate_fn_output__(fn=fn)

        self.id = id
        self.fn = fn
        self.inputs = inputs

    @staticmethod
    def __validate_fn_input__(fn: Callable):
        """
            Validates such that expected input type of fn is same as been given on init.
        """
        parameters = dict(inspect.signature(fn).parameters)
        if not parameters:
            raise Exception(f"Function {fn} is missing inputs. A Piece-function must have at least one input.")

        for _, param in parameters.items():
            if param._annotation == inspect._empty:
                raise TypeError(f"Input arguments cannot be untyped. In function {fn}, got '{param._annotation}'")

    @staticmethod
    def __validate_fn_output__(fn: Callable):
        """
            Validates such that expected output type of fn is same as been given on init.
        """
        expected_output_type = inspect.signature(fn).return_annotation
        if expected_output_type == inspect._empty:
            raise TypeError(f"Output type cannot be untyped. In function {fn}, got '{expected_output_type}'")

    async def perform(self, input: Dict[str, Any] = {}) -> Any:
        return await super().perform({**input, **self.inputs})

class Competition(Perform):

    """
        A Competition is a race between two performers of whom is completed
        first. Whenever one is done, results are returned and the others are
        cancelled.
    """

    def __init__(self, id: str, performers: List[Perform]) -> None:
        super().__init__()
        self.id = id
        self.performers = performers

    async def fn(self, input: dict) -> Any:
        loop = asyncio.get_running_loop()
        
        async_tasks = [
            loop.create_task(performer.perform(**{'input': input}))
            for performer in self.performers
        ]
        try:
            while async_tasks:
                done, pending = await asyncio.wait(async_tasks, return_when=asyncio.FIRST_COMPLETED)

                for finished in done:
                    
                    try:
                        result = finished.result()
                        for task in pending:
                            task.cancel()

                        return result

                    except:
                        async_tasks = pending
                        continue

        except asyncio.CancelledError as ce:
            raise ce
        except Exception as e:
            raise e

    async def perform(self, input: Dict[str, Any]) -> Any:
        return await super().perform(input={'input': input})

class Dependency(object):

    """
        A Dependency is connecting two pieces on one agreed argument.
        E.g., piece_id="1" is dependent on dependen_on_id="0" and connected on
        argument connected_on="arg", meaning that the result from "0" will be propagated
        to "1" by "arg".
    """

    def __init__(self, piece_id: str, dependent_on_id: str, connected_on: str) -> None:
        self.piece_id = piece_id
        self.dependent_on_id = dependent_on_id
        self.connected_on = connected_on

class Composition(Perform):

    """
        A Composition is a composition of pieces, sub classing Perform and running according to the piece's dependencies.
    """

    def __init__(self, id: str, pieces: List[Piece], dependencies: List[Dependency] = []) -> None:
        super().__init__()
        self.id = id
        self.pieces = {piece.id: piece for piece in pieces}
        self.dependencies = Composition._key_dependencies(
            pieces=pieces, 
            dependencies=dependencies,
        )
        self.piece_running_order = list(
            toposort(
                Composition._toposort_dependencies(
                    pieces=pieces,
                    dependencies=dependencies,
                ),
            ),
        )

    @staticmethod
    def _toposort_dependencies(pieces: List[Piece], dependencies: List[Dependency]):

        depend = {piece.id: set() for piece in pieces}
        for dependency in dependencies:
            depend[dependency.piece_id].add(dependency.dependent_on_id)

        return depend

    @staticmethod
    def _key_dependencies(pieces: List[Piece], dependencies: List[Dependency]):

        depend = {piece.id: [] for piece in pieces}
        for dependency in dependencies:
            depend[dependency.piece_id].append((dependency.dependent_on_id, dependency.connected_on))
        return depend

    async def fn(self, input: dict = {}) -> Any:
        
        outs = {}
        loop = asyncio.get_running_loop()
        for piece_paras in self.piece_running_order:
            
            async_tasks = []
            for piece_key in piece_paras:

                try:
                    input_args = {**{}, **input}
                    if piece_key in self.dependencies:
                        for target_piece_key, piece_arg in self.dependencies[piece_key]:
                            input_args.update({piece_arg: outs[target_piece_key]})

                    async_tasks.append(loop.create_task(self.pieces[piece_key].perform(input_args)))
                except Exception as e:
                    raise Exception(f"Could not construct task from piece function '{piece_key}' because of error: {e}")

            piece_results = await asyncio.gather(*async_tasks, return_exceptions=True)
            for piece_result, piece_key in zip(piece_results, piece_paras):
                outs[piece_key] = piece_result

        return outs

    async def perform(self, input: Dict[str, Any] = {}) -> Any:
        return await super().perform(input={'input': input})