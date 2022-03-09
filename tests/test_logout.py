import pytest
from source.error import AccessError
from source.register import register
from source.login import login
from source.logout import logout
from source.test_clear import clear

@pytest.fixture
def initial_clear():
	clear()

@pytest.fixture
def register_a():
	register_info = register("testA@gmail.com", "1234567890", "Person", "AA")
	return register_info

def test_invalid_token_format(initial_clear, register_a):
	test_token = "hello"
	with pytest.raises(AccessError):
		logout(test_token)

def test_invalid_token(initial_clear, register_a):
	test_token = "aaa.bbb.ccc"
	with pytest.raises(AccessError):
		logout(test_token)

def test_logout_success(initial_clear, register_a):
	# Nothing is supposed to happen here since logout
	# does not return anything. So expected behaviour is that
	# this test passes without any errors.
	token = register_a['token']
	logout(token)