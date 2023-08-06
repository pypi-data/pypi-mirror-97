import pytest

from wait import *

def test_wait_for():
    def func():
        import random
        return random.randint(0, 1)

    wait_for(func, 0) 

def test_wait_for_true():

    def TFunc():
        return True
    
    def FFunc():
        return False

    wait_for_true(TFunc)

    try:
        wait_for_true(FFunc, 1, 5)
    except TimeoutError as e:
        return
    
    assert False

def test_wait_for_false():

    def TFunc():
        return True
    
    def FFunc():
        return False

    wait_for_false(FFunc)

    try:
        wait_for_false(TFunc, 1, 5)
    except TimeoutError as e:
        return
    
    assert False

def test_wait_until_change():

    def CFunc():
        import random
        return random.randint(0, 1)
    
    def NCFunc():

        return 0
    
    wait_until_change(CFunc)

    try:
        wait_until_change(NCFunc, 1, 5)
    except TimeoutError as e:
        return
    
    assert False

def test_wait_until_no_change():

    def NCFunc():

        return 0
    
    wait_until_no_change(NCFunc)