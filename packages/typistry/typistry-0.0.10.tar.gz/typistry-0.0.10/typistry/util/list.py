from typing import Optional, TypeVar, List, Union, Tuple, Type

A = TypeVar("A")
B = TypeVar("B")

def flatten(l: List[Optional[A]]) -> List[A]:
    return [string for string in l if string]

def sequence(l: List[Union[A, B]], type_a: Type[A], type_b: Type[B]) -> Tuple[List[A], List[B]]:
    l1: List[A] = []
    l2: List[B] = []
    for l0 in l:
        if isinstance(l0, type_a):
            l1.append(l0)
        else:
            assert(isinstance(l0, type_b))
            l2.append(l0)
    return l1, l2

