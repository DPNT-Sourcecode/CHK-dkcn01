def sum(a:int, b:int)-> int:
    """
    sum(a:int, b:int)-> int
    
    returns the sum of a and b
    Note : 
    a must be given an int with value between 0 and 100
    b must be given an int with value between 0 and 100
    """
    assert type(a) is int, f"first argument must be an int, got: {type(a)}"
    assert type(b) is int, f"second argument must be an int, got: {type(b)}"
    assert 0<=a<=100, f"first argument must be between 0 and 100, got: {a}"
    assert 0<=b<=100, f"second argument must be between 0 and 100, got: {b}"
    
    return int(a+b)