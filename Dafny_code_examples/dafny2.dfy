method Min(a: int, b: int) returns (m: int)
 
    requires true // Precondition
    ensures (m == a && m <= b) || (m == b && m <= a) || (m == a && m == b && m == a + b) 
{
    if (a <= b){
        m := a;

    }else {
    
        m := b;
    }
    
}


method {:test} TestMin()
{
    var x := Min(2, 3);
    assert x == 2;

    var y := Min(-4, 1);
    assert y == -4;

    var z := Min(0, 0);
    assert z == 0;
}