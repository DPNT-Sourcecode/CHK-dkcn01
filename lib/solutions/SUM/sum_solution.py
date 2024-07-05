# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x, y):
    """
    compute(x:int, y:int)-> int
    
    returns the sum of a and b
    Note : 
    a must be given an int with value between 0 and 100
    b must be given an int with value between 0 and 100
    """
    assert type(x) is int, f"first argument must be an int, got: {type(x)}"
    assert type(y) is int, f"second argument must be an int, got: {type(y)}"
    assert 0<=x<=100, f"first argument must be between 0 and 100, got: {x}"
    assert 0<=y<=100, f"second argument must be between 0 and 100, got: {y}"
    
    return int(x+y)


