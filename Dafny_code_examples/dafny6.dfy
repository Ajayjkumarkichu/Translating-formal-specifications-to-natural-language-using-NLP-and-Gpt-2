function pow2(n: nat): nat
{
    if n == 0 then 1
    else 2 * pow2(n - 1)
}
method {:test} Testpow2()
{
    var x := pow2(2);
    assert x == 4;
 
    var y := pow2(0);
    assert y == 1;
}
