function Fib(n: nat): nat
{
    if n < 2 then n else Fib(n - 1) + Fib(n - 2)
}
 
method FibIter(n: nat) returns (x: nat)
    ensures x == Fib(n)
{
    var a := 0;
    var b := 1;
    var i := 0;
    while i < n
        invariant i <= n
        invariant a == Fib(i)
        invariant b == Fib(i + 1)
    {
        var temp := a;
        a := b;
        b := temp + b;
        i := i + 1;
    }
    x := a;
}