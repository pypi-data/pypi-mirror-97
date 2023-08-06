from types import FunctionType, MethodType
from typing import NoReturn
import time
import logging

logger = logging.getLogger(__name__)

def wait_until_change(func:FunctionType, interval:int=5, timeout:int=600) -> NoReturn:
    """wait until the return by function changed

    Args:
        func (functionType): function to call
        interval (int, optional): interval to check, default 5 sec
        timeout (int, optional): check timeout, if timeout and the return is no changed, raise TimeoutError. default 600s
    """
    # only function can be called
    assert type(func) == FunctionType or type(func) == MethodType
    s_time = time.time()
    last_result = func()
    while True:
        logger.info("wait %ss to retry" % interval)
        time.sleep(interval)
        result = func()
        waittime = time.time() - s_time
        if result != last_result:
            logger.warning("wait %.1fs" % waittime)
            break
        else:
            last_result = result
            if waittime > timeout:
                raise TimeoutError("%ss timeout" % timeout)
    
    return result


def wait_until_no_change(func:FunctionType, interval:int=5, timeout:int=600) -> NoReturn:
    """wait until the return by function no change any more

    Args:
        func (functionType): function to call
        interval (int, optional): interval to check, default 5 sec
        timeout (int, optional): check timeout, if timeout and the return keeps changing, raise TimeoutError. default 600s
    """
    # only function can be called
    assert type(func) == FunctionType or type(func) == MethodType
    s_time = time.time()
    last_result = func()
    while True:
        logger.info("wait %ss to retry" % interval)
        time.sleep(interval)
        result = func()
        waittime = time.time() - s_time
        if result == last_result:
            logger.warning("wait %.1fs" % waittime)
            break
        else:
            last_result = result
            if waittime > timeout:
                raise TimeoutError("%ss timeout" % timeout)
    
    return result

def wait_for_true(func:FunctionType, interval:int=1, timeout:int=30) -> NoReturn:
    """wait until the function returns True

    Args:
        func (FunctionType): function to call
        interval (int, optional): interval to check, default 1 sec
        timeout (int, optional): check timeout, if timeout and no True has been returned, raise TimeoutError. default 30s
    """
    assert type(func) == FunctionType or type(func) == MethodType
    s_time = time.time()
    while timeout > (time.time() - s_time):

        if func():
            logger.warning("wait %.1fs" % (time.time() - s_time))
            return
        else:
            logger.info("wait %ss to retry" % interval)
            time.sleep(interval)
    
    raise TimeoutError('%ss timeout' % timeout)

def wait_for_false(func:FunctionType, interval:int=1, timeout:int=30) -> NoReturn:
    """wait until the function returns False

    Args:
        func (FunctionType): function to call
        interval (int, optional): interval to check, default 1 sec
        timeout (int, optional): check timeout, if timeout and no False has been returned, raise TimeoutError. default 30s
    """
    assert type(func) == FunctionType or type(func) == MethodType
    s_time = time.time()
    while timeout > (time.time() - s_time):

        if not func():
            logger.warning("wait %.1fs" % (time.time() - s_time))
            return
        else:
            logger.info("wait %ss to retry" % interval)
            time.sleep(interval)
    
    raise TimeoutError('%ss timeout' % timeout)