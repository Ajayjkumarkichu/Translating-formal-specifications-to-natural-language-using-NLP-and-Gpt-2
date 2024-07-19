function power(a:int , n: nat): (result: int)
{
    if n == 0 then 1
    else a * power(a, n - 1)
}
method Pow(a: int, n: nat) returns (result: int)
    ensures result == power(a, n) 
{
    result := 1;
    var i := 0;
    while i < n
        invariant 0 <= i <= n
        invariant result * power(a, n - i) == power(a, n)
    {
        result := result * a;
        i := i + 1;
    }
}