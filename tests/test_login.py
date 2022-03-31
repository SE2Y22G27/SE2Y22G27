'''
    import pytest to test if the auth login behave normally
'''
import pytest
from source.login import login
from source.register import register
from source.test_clear import clear
from source.error import InputError

def test_no_register():
    '''
        test error when the email hasn't been registered
    '''
    clear()
    with pytest.raises(InputError):
        login("test@gmail.com", "password")

def test_login_email_fail():
    '''
        testing the email is invalid
    '''
    clear()
    register("testA@gmail.com", "1234567890", "Person", "AA")
    with pytest.raises(InputError):
        login("hello@gmail.com", "password")

def test_login_password_fail():
    '''
        testing the password is invalid
    '''
    clear()
    register("testA@gmail.com", "1234567890", "Person", "AA")
    with pytest.raises(InputError):
        login("testA@gmail.com", "password")

def test_register_login_success():
    '''
        testing all the input are valid and the funciton
        performs normally
    '''
    clear()
    register_id = register("test@gmail.com", "password", "Person", "Person")
    login_id = login("test@gmail.com", "password")
    assert register_id['auth_user_id'] == login_id['auth_user_id']
    assert register_id['token'] != login_id['token']


def test_multiple_register_login(register_a, register_b, register_c):
    '''
        testing multiple register and login
    '''
    clear()
    register_a = register("testA@gmail.com", "1234567890", "Person", "AA")
    register_b = register("testB@gmail.com", "1234567890", "Person", "BB")
    register_c = register("testC@gmail.com", "1234567890", "Person", "CC")

    login0 = login("testA@gmail.com", "1234567890")
    login1 = login("testB@gmail.com", "1234567890")
    login2 = login("testC@gmail.com", "1234567890")

    assert login0['auth_user_id'] == register_a['auth_user_id']
    assert login1['auth_user_id'] == register_b['auth_user_id']
    assert login2['auth_user_id'] == register_c['auth_user_id']

    assert login0['token'] != register_a['token']
    assert login1['token'] != register_b['token']
    assert login2['token'] != register_c['token']
