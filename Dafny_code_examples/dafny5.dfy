method Max(a: int, b: int) returns (m: int)
  requires true  
  ensures m == MaxDef(a, b)  
  ensures m >= a && m >= b  
{
    m := MaxDef(a, b);
}

method Min(a: int, b: int) returns (m: int)
  requires true  
  ensures m == MinDef(a, b)  
  ensures m <= a && m <= b  
{
    m := MinDef(a, b);
}
function MaxDef(a: int, b: int): int
{
    if a > b then a else b
}

function MinDef(a: int, b: int): int
{
    if a < b then a else b
}