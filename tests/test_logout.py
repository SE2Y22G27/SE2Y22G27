'''
	imported all the required module to test of authorised user logout
	successfully
'''
import pytest
from source.error import AccessError
from source.register import register
from source.logout import logout
from source.test_clear import clear

def test_invalid_token_format():
    '''
        test when entering invalid token format to logout
    '''
    clear()
    register("testA@gmail.com", "1234567890", "Person", "AA")
    test_token = "hello"
    with pytest.raises(AccessError):
        logout(test_token)

def test_invalid_token():
    '''
        test when entering invalid token to logout
	'''
    clear()
    register("testA@gmail.com", "1234567890", "Person", "AA")
    test_token = "aaa.bbb.ccc"
    with pytest.raises(AccessError):
        logout(test_token)

def test_logout_success():
    '''
		test when entering valid token to logout
	'''
	# Nothing is supposed to happen here since logout
	# does not return anything. So expected behaviour is that
	# this test passes without any errors.
    clear()
    register_a = register("testA@gmail.com", "1234567890", "Person", "AA")
    token = register_a['token']
    logout(token)
