import pytest


def find_element(collection, element):
    return element in collection


@pytest.fixture()
def test_data1():
    # print('init')
    return ['a', 'b', 'c']


@pytest.fixture()
def test_data2():
    # print('init')
    return ['a', 'b', 'd']


@pytest.fixture(autouse=True)
def run_around_tests():
    print('before test')
    yield
    # Code that will run after your test, for example:
    print('after test')


def test_stuff(test_data1):
    print('test')
    assert find_element(test_data1, 'a')


def test_stuff2(test_data2):
    print('test')
    assert find_element(test_data2, 'd')


def test_stuff3(test_data2):
    print('test')
    assert not find_element(test_data2, 'x')


if __name__ == '__main__':
    print('hello')
