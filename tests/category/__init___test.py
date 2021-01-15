from dataclasses import asdict, dataclass, field
from typing import Generic, TypeVar

from category import Vector

_T = TypeVar("_T")


def test_vector_init():
    assert [] == Vector() == []
    assert [] == Vector([]) == []
    assert [] == Vector(()) == []
    # assert [] == Vector({}) == [] # Syntax Error
    sequence = Vector([0, 1, 2])
    assert isinstance(sequence, Vector)
    assert 0 == sequence[0] == 0
    assert [0, 1, 2] == sequence == [0, 1, 2]
    assert (0, 1, 2) != sequence != (0, 1, 2)
    assert {0, 1, 2} != sequence != {0, 1, 2}
    assert [0, 2, 4] == Vector([element * 2 for element in sequence]) == [0, 2, 4]


def test_vector_add():
    # immutable + mutalbe
    sequence = Vector([0, 1, 2])
    im_sequence = sequence + [3]
    assert im_sequence is not sequence
    assert isinstance(im_sequence, Vector)
    assert [0, 1, 2, 3] == im_sequence == [0, 1, 2, 3]
    assert [0, 1, 2] == sequence == [0, 1, 2]
    assert im_sequence != sequence

    # immutable + immutable
    other_sequence = Vector([3, 4, 5])
    ii_sequence = sequence + other_sequence
    assert ii_sequence is not sequence
    assert ii_sequence is not other_sequence
    assert isinstance(ii_sequence, Vector)
    assert [0, 1, 2, 3, 4, 5] == ii_sequence == [0, 1, 2, 3, 4, 5]
    assert [0, 1, 2] == sequence == [0, 1, 2]
    assert [3, 4, 5] == other_sequence == [3, 4, 5]
    assert ii_sequence != sequence
    assert ii_sequence != other_sequence


def test_vector_add_warning_case():
    # mutable + immutable
    sequence = Vector([0, 1, 2])
    mi_sequence = [3] + sequence
    assert mi_sequence is not sequence
    assert not isinstance(mi_sequence, Vector)
    assert isinstance(mi_sequence, list)
    assert [3, 0, 1, 2] == mi_sequence == [3, 0, 1, 2]
    assert [0, 1, 2] == sequence == [0, 1, 2]
    assert mi_sequence != [3]
    assert mi_sequence != sequence


# Syntax Error
# def test_immutable_sequence_setitem():
#    sequence = Vector([0, 1, 2])
#    try:
#        sequence[1] = 9
#        assert False
#    except TypeError:
#        assert True


# Syntax Error
# def test_immutable_sequence_delitem():
#    sequence = Vector([0, 1, 2])
#    try:
#        del sequence[1]
#        assert False
#    except TypeError:
#        assert True


def test_vector_append():
    sequence = Vector([0, 1, 2])
    appended_sequence = sequence.append(3)
    assert appended_sequence is not sequence
    assert isinstance(appended_sequence, Vector)
    assert isinstance(sequence, Vector)
    assert [0, 1, 2, 3] == appended_sequence == [0, 1, 2, 3]


def test_vector_extend():
    sequence = Vector([0, 1, 2])
    extend_sequence = [3, 4, 5]
    extended_sequence = sequence.extend(extend_sequence)
    assert extended_sequence is not sequence
    assert extended_sequence is not extend_sequence
    assert isinstance(extended_sequence, Vector)
    assert isinstance(sequence, Vector)
    assert [0, 1, 2, 3, 4, 5] == extended_sequence == [0, 1, 2, 3, 4, 5]


def test_vector_insert():
    sequence = Vector([0, 1, 2])
    inserted_sequence = sequence.insert(1, 9)
    assert inserted_sequence is not sequence
    assert isinstance(inserted_sequence, Vector)
    assert isinstance(sequence, Vector)
    assert [0, 9, 1, 2] == inserted_sequence == [0, 9, 1, 2]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_vector_remove():
    sequence = Vector([0, 1, 2])
    removed_sequence = sequence.remove(1)
    assert removed_sequence is not sequence
    assert isinstance(removed_sequence, Vector)
    assert isinstance(sequence, Vector)
    assert [0, 2] == removed_sequence == [0, 2]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_vector_pop():
    sequence = Vector([0, 1, 2])
    poped_sequence = sequence.pop(1)
    assert poped_sequence is not sequence
    assert isinstance(poped_sequence, Vector)
    assert isinstance(sequence, Vector)
    assert [0, 2] == poped_sequence == [0, 2]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_vector_index():
    sequence = Vector([0, 1, 2])
    index = sequence.index(1, 0, 2)
    assert isinstance(sequence, Vector)
    assert 1 == index
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_vector_clear():
    sequence = Vector([0, 1, 2])
    try:
        sequence.clear()
        assert False
    except TypeError:
        assert True


def test_vector_count():
    sequence = Vector([0, 1, 2])
    assert 1 == sequence.count(0)
    assert type(sequence)
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_vector_sort():
    sequence = Vector([0, 1, 2])
    sorted_sequence = sequence.sort(reverse=True)
    assert sorted_sequence is not sequence
    assert isinstance(sorted_sequence, Vector)
    assert isinstance(sequence, Vector)
    assert [2, 1, 0] == sorted_sequence == [2, 1, 0]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_vector_reverse():
    sequence = Vector([0, 1, 2])
    reversed_sequence = sequence.reverse()
    assert reversed_sequence is not sequence
    assert isinstance(reversed_sequence, Vector)
    assert isinstance(sequence, Vector)
    assert [2, 1, 0] == reversed_sequence == [2, 1, 0]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_vector_copy():
    sequence = Vector([0, 1, 2])
    copied_sequence = sequence.copy()
    assert copied_sequence is not sequence
    assert isinstance(copied_sequence, Vector)
    assert isinstance(sequence, Vector)
    assert copied_sequence == sequence == copied_sequence
    assert [0, 1, 2] == copied_sequence == [0, 1, 2]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_vector_empty():
    sequence = Vector([0, 1, 2])
    assert False is sequence.is_empty()


def test_vector_non_empty():
    sequence = Vector([0, 1, 2])
    assert True is sequence.non_empty()


def test_immutable_sequence_size():
    sequence = Vector([0, 1, 2])
    assert 3 == sequence.size()


def test_immutable_sequence_map():
    sequence = Vector([0, 1, 2])
    mapped_sequence = sequence.map(function=lambda x: x * 2)
    assert mapped_sequence is not sequence
    assert [0, 2, 4] == mapped_sequence


def test_immutable_sequence_redece():
    sequence = Vector([0, 1, 2])
    reduced_sequence = sequence.reduce(function=lambda left, right: left * right)
    assert reduced_sequence is not sequence
    assert 0 == reduced_sequence


def test_immutable_sequence_dataclass():
    @dataclass(frozen=True)
    class SeqEntity(Generic[_T]):
        value: Vector[_T] = field(default_factory=Vector[_T])

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
