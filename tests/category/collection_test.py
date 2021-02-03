from dataclasses import asdict, dataclass, field
from typing import Generic, TypeVar

from category import Vector

T = TypeVar("T")


def test_vector_init():
    assert [] == Vector() == []
    assert [] == Vector([]) == []
    assert [] == Vector(()) == []
    # assert [] == Vector({}) == [] # Syntax Error
    vector = Vector([0, 1, 2])
    assert Vector is type(vector)
    assert 0 == vector[0] == 0
    assert [0, 1, 2] == vector == [0, 1, 2]
    assert (0, 1, 2) != vector != (0, 1, 2)
    assert {0, 1, 2} != vector != {0, 1, 2}
    assert [0, 2, 4] == Vector([element * 2 for element in vector]) == [0, 2, 4]


def test_vector_add():
    # immutable + mutalbe
    vector = Vector([0, 1, 2])
    im_vector = vector + [3]
    assert im_vector is not vector
    assert Vector is type(im_vector)
    assert [0, 1, 2, 3] == im_vector == [0, 1, 2, 3]
    assert [0, 1, 2] == vector == [0, 1, 2]
    assert im_vector != vector

    # immutable + immutable
    other_vector = Vector([3, 4, 5])
    ii_vector = vector + other_vector
    assert ii_vector is not vector
    assert ii_vector is not other_vector
    assert Vector is type(ii_vector)
    assert [0, 1, 2, 3, 4, 5] == ii_vector == [0, 1, 2, 3, 4, 5]
    assert [0, 1, 2] == vector == [0, 1, 2]
    assert [3, 4, 5] == other_vector == [3, 4, 5]
    assert ii_vector != vector
    assert ii_vector != other_vector


def test_vector_add_warning_case():
    # mutable + immutable
    vector = Vector([0, 1, 2])
    mi_vector = [3] + vector
    assert mi_vector is not vector
    assert list is type(mi_vector)
    assert Vector is not type(mi_vector)
    assert [3, 0, 1, 2] == mi_vector == [3, 0, 1, 2]
    assert [0, 1, 2] == vector == [0, 1, 2]
    assert mi_vector != [3]
    assert mi_vector != vector


# Syntax Error
# def test_immutable_vector_setitem():
#    vector = Vector([0, 1, 2])
#    try:
#        vector[1] = 9
#        assert False
#    except TypeError:
#        assert True


# Syntax Error
# def test_immutable_vector_delitem():
#    vector = Vector([0, 1, 2])
#    try:
#        del vector[1]
#        assert False
#    except TypeError:
#        assert True


def test_vector_append():
    vector = Vector([0, 1, 2])
    appended_vector = vector.append(3)
    assert appended_vector is not vector
    assert Vector is type(vector)
    assert Vector is type(appended_vector)
    assert [0, 1, 2, 3] == appended_vector == [0, 1, 2, 3]


def test_vector_extend():
    vector = Vector([0, 1, 2])
    extend_vector = [3, 4, 5]
    extended_vector = vector.extend(extend_vector)
    assert extended_vector is not vector
    assert extended_vector is not extend_vector
    assert Vector is type(vector)
    assert Vector is type(extended_vector)
    assert [0, 1, 2, 3, 4, 5] == extended_vector == [0, 1, 2, 3, 4, 5]


def test_vector_insert():
    vector = Vector([0, 1, 2])
    inserted_vector = vector.insert(1, 9)
    assert inserted_vector is not vector
    assert Vector is type(vector)
    assert Vector is type(inserted_vector)
    assert [0, 9, 1, 2] == inserted_vector == [0, 9, 1, 2]
    assert [0, 1, 2] == vector == [0, 1, 2]


def test_vector_remove():
    vector = Vector([0, 1, 2])
    removed_vector = vector.remove(1)
    assert removed_vector is not vector
    assert Vector is type(vector)
    assert Vector is type(removed_vector)
    assert [0, 2] == removed_vector == [0, 2]
    assert [0, 1, 2] == vector == [0, 1, 2]


def test_vector_pop():
    vector = Vector([0, 1, 2])
    poped_vector = vector.pop(1)
    assert poped_vector is not vector
    assert Vector is type(vector)
    assert Vector is type(poped_vector)
    assert [0, 2] == poped_vector == [0, 2]
    assert [0, 1, 2] == vector == [0, 1, 2]


def test_vector_index():
    vector = Vector([0, 1, 2])
    index = vector.index(1, 0, 2)
    assert Vector is type(vector)
    assert 1 == index
    assert [0, 1, 2] == vector == [0, 1, 2]


def test_vector_clear():
    vector = Vector([0, 1, 2])
    try:
        vector.clear()
        assert False
    except TypeError:
        assert True


def test_vector_count():
    vector = Vector([0, 1, 2])
    assert 1 == vector.count(0)
    assert type(vector)
    assert [0, 1, 2] == vector == [0, 1, 2]


def test_vector_sort():
    vector = Vector([0, 1, 2])
    sorted_vector = vector.sort(reverse=True)
    assert sorted_vector is not vector
    assert Vector is type(vector)
    assert Vector is type(sorted_vector)
    assert [2, 1, 0] == sorted_vector == [2, 1, 0]
    assert [0, 1, 2] == vector == [0, 1, 2]


def test_vector_reverse():
    vector = Vector([0, 1, 2])
    reversed_vector = vector.reverse()
    assert reversed_vector is not vector
    assert Vector is type(vector)
    assert Vector is type(reversed_vector)
    assert [2, 1, 0] == reversed_vector == [2, 1, 0]
    assert [0, 1, 2] == vector == [0, 1, 2]


def test_vector_copy():
    vector = Vector([0, 1, 2])
    copied_vector = vector.copy()
    assert copied_vector is not vector
    assert Vector is type(vector)
    assert Vector is type(copied_vector)
    assert copied_vector == vector == copied_vector
    assert [0, 1, 2] == copied_vector == [0, 1, 2]
    assert [0, 1, 2] == vector == [0, 1, 2]


def test_vector_empty():
    vector = Vector([0, 1, 2])
    assert False is vector.is_empty()


def test_vector_non_empty():
    vector = Vector([0, 1, 2])
    assert True is vector.non_empty()


def test_immutable_vector_size():
    vector = Vector([0, 1, 2])
    assert 3 == vector.size()


def test_immutable_vector_map():
    vector = Vector([0, 1, 2])
    mapped_vector = vector.map(function=lambda x: x * 2)
    assert mapped_vector is not vector
    assert [0, 2, 4] == mapped_vector


def test_immutable_vector_redece():
    vector = Vector([0, 1, 2])
    reduced_vector = vector.reduce(function=lambda left, right: left * right)
    assert reduced_vector is not vector
    assert 0 == reduced_vector


def test_immutable_vector_dataclass():
    @dataclass(frozen=True)
    class SeqEntity(Generic[T]):
        value: Vector[T] = field(default_factory=Vector[T])

    entity = SeqEntity(value=Vector())
    dict_entity = asdict(entity)
    entity_from_dict = SeqEntity(**dict_entity)
    assert {"value": []} == dict_entity == {"value": []}
    assert entity_from_dict == entity == entity_from_dict

    number_entity = SeqEntity(value=Vector([0, 1, 2]))
    dict_number_entity = asdict(number_entity)
    number_entity_from_dict = SeqEntity(**dict_number_entity)
    assert {"value": [0, 1, 2]} == dict_number_entity == {"value": [0, 1, 2]}
    assert number_entity_from_dict == number_entity == number_entity_from_dict
