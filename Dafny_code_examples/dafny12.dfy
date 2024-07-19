method Smallest(a: array<int>) returns (minIndex: nat)
    requires a.Length > 0
    ensures 0 <= minIndex < a.Length
    ensures forall i | 0 <= i < a.Length :: a[minIndex] <= a[i]
{
    minIndex := 0;
    var i := 1;
    while i < a.Length
        invariant 0 <= i <= a.Length
        invariant 0 <= minIndex < a.Length
        invariant forall j | 0 <= j < i :: a[minIndex] <= a[j]
    {
        if a[i] < a[minIndex] {
            minIndex := i;
        }
        i := i + 1;
    }
}
