method Filter<T>(a: array<T>, P: T -> bool) returns (s: seq<T>)
    ensures forall x | x in s :: P(x)
    ensures s == [] ==> forall i | 0 <= i < a.Length :: !P(a[i])
    ensures multiset(s) <= multiset(a[..])
{
    s := [];
    var i := 0;
    while i < a.Length
        invariant 0 <= i <= a.Length
        invariant forall x | x in s :: P(x)
        invariant multiset(s) <= multiset(a[..i])
    {
        if P(a[i]) {
            s := s + [a[i]];
        }
        i := i + 1;
    }
}
