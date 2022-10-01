"""
SPIKE Prime spike.control Python Classes

"""
class Timer:
    def __init__(self):
        pass
    def reset(self):
        pass
    def now(self):
        pass

def wait_for_seconds(seconds):
    """
    Waits for a specified number of seconds before continuing the program.
    
    Parameters
    --------------
    seconds : The time to wait in seconds.
    
    Type : float (decimal value)
    
    Values : any value
    
    Default : no default value
    
    Errors
    ----------------
    TypeError : seconds is not a number.
    
    ValueError : seconds is not at least 0.
    """
    pass
def wait_until(get_value_function, operator_function, target_value=True):
    """
    Waits until the condition is True before continuing with the program.
    
    Parameters
    --------------
    get_value_function
    
    Type : callable function
    
    Values : A function that returns the current value to be compared to the target value.
    
    Default : no default value
    
    operator_function
    
    Type : callable function
    
    Values : A function that compares two arguments. The first argument will be the result of get_value_function() and the second argument will be target_value. The function will compare these two values and return the result.
    
    Default : no default value
    
    target_value
    
    Type : any type
    
    Values : Any object that can be compared by operator_function.
    
    Default : no default value
    
    Errors
    ----------------
    TypeError : get_value_function or operator_function is not callable or operator_function does not compare two arguments.
    """
    pass
