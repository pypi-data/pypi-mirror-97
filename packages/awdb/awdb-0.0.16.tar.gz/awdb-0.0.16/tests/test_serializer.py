import pytest


@pytest.fixture
def serializer():
    from awdb.serializer import Serializer
    return Serializer()


def test_base_serialize(serializer):
    assert serializer.serialize(1) == 1
    assert serializer.serialize("a") == "a"
    assert serializer.serialize(1.2) == 1.2


def test_container_serialize(serializer):
    data = ["a", 1, 1.2, True]
    result = serializer.serialize(data)
    assert result == data

    data = [["a", 1, 1.2, True]]
    result = serializer.serialize(data)
    assert result == data

    data = [["a", 1, 1.2, True, {"a": "d"}]]
    result = serializer.serialize(data)
    assert result == data

    data = [["a", 1, 1.2, True, {True: "d"}]]
    result = serializer.serialize(data)
    assert result != data

    data = [["a", 1, 1.2, True, {True: "d"}]]
    result = serializer.serialize(data)
    assert result == [["a", 1, 1.2, True, {"True": "d"}]]


def test_dict_serialize(serializer):
    """
    Test that values get properly converted in the
    structure including the keys which should be strings.
    """
    data = {"a": "2"}
    result = serializer.serialize(data)
    assert result == data

    data = {1: "1"}
    result = serializer.serialize(data)
    assert result == {"1": "1"}

    data = {2: "2", True: True}
    result = serializer.serialize(data)
    assert result == {"2": "2", "True": True}

    data = {tuple([1, 2]): True}
    result = serializer.serialize(data)
    assert result == {"[1, 2]": True}

    data = {1: {1: {1: tuple([1, 2, 3])}}}
    result = serializer.serialize(data)
    assert result == {"1": {"1": {"1": [1, 2, 3]}}}


def test_custom_type(serializer):
    class CustomCons(object):
        def __init__(self, car, cdr):
            self.car = car
            self.cdr = cdr

    def custom_cons_dispatch(serializer, value):
        result = []
        serializer.dispatch(value.car)
        car = serializer.result
        serializer.dispatch(value.cdr)
        cdr = serializer.result
        result.append(car)
        if isinstance(cdr, list):
            result += cdr
        else:
            result.append(cdr)
        serializer.result = result

    serializer.define_dispatch(CustomCons, custom_cons_dispatch)

    data = CustomCons(1, CustomCons(2, CustomCons(3, None)))
    result = serializer.serialize(data)
    assert result == [1, 2, 3, None]


def test_unknown_type(serializer):
    class CustomType(object):
        def __init__(self, data):
            self.data = data

        def __repr__(self):
            return 'Custom<{}>'.format(self.data)

    data = CustomType(42)
    result = serializer.serialize(data)
    assert result == 'Custom<42>'

    data = {CustomType(43): CustomType(99)}
    result = serializer.serialize(data)
    assert result == {'Custom<43>': 'Custom<99>'}


def test_awdb_type(serializer):
    class CustomType(object):
        def __init__(self, data):
            self.data = data

        def __awdb_repr__(self):
            return 'Custom<{}>'.format(self.data)

    data = CustomType(42)
    result = serializer.serialize(data)
    assert result == 'Custom<42>'

    data = {CustomType(43): CustomType(99)}
    result = serializer.serialize(data)
    assert result == {'Custom<43>': 'Custom<99>'}
