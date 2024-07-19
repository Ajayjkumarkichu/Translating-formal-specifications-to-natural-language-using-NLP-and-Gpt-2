predicate sorted(a: array<int>)
    reads a
{

    forall i, j | 0 <= i < j < a.Length :: a[i] <= a[j]
}

method BinarySearch(a: array<int>, value: int) returns (index: int)
    requires sorted(a)
    ensures index == -1 || 0 <= index < a.Length
    ensures index == -1 ==> value !in a[..]

    ensures index >= 0  ==> a[index] == value