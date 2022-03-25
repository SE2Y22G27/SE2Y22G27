import pytest
from source.login import login
from source.register import register
from source.test_clear import clear
from source.error import InputError

@pytest.fixture
def reset():
    """ Function for clearing the data before the test """
    clear()

@pytest.fixture
def register_a(reset):
    '''
    (Empty Docstring)
    '''
    reset
    register_info = register("testA@gmail.com", "1234567890", "Person", "AA")
    return register_info

@pytest.fixture
def register_b(reset):
    '''
    (Empty Docstring)
    '''
    reset
    register_info = register("testB@gmail.com", "1234567890", "Person", "BB")
    return register_info

@pytest.fixture
def register_c(reset):
    '''
    (Empty Docstring)
    '''
    reset
    register_info = register("testC@gmail.com", "1234567890", "Person", "CC")
    return register_info

def test_no_register(reset):
    '''
    (Empty Docstring)
    '''
    reset
    with pytest.raises(InputError):
        login("test@gmail.com", "password")

def test_login_email_fail(reset, register_a):
    '''
    (Empty Docstring)
    '''
    reset
    with pytest.raises(InputError):
        login("hello@gmail.com", "password")

def test_login_password_fail(reset, register_a):
    '''
    (Empty Docstring)
    '''
    reset
    with pytest.raises(InputError):
        login("testA@gmail.com", "password")

def test_register_login_success(reset):
    '''
    (Empty Docstring)
    '''
    reset
    register_id = register("test@gmail.com", "password", "Person", "Person")
    login_id = login("test@gmail.com", "password")
    assert register_id['auth_user_id'] == login_id['auth_user_id']
    assert register_id['token'] != login_id['token']

def test_multiple_register_login(reset, register_a, register_b, register_c):
    '''
    (Empty Docstring)
    '''
    reset
    login0 = login("testA@gmail.com", "1234567890")
    login1 = login("testB@gmail.com", "1234567890")
    login2 = login("testC@gmail.com", "1234567890")

    assert login0['auth_user_id'] == register_a['auth_user_id']
    assert login1['auth_user_id'] == register_b['auth_user_id']
    assert login2['auth_user_id'] == register_c['auth_user_id']

    assert login0['token'] != register_a['token']
    assert login1['token'] != register_b['token']
    assert login2['token'] != register_c['token']
