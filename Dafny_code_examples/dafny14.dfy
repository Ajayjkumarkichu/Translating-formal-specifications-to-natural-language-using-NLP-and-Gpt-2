function F(x: int): int
  decreases x
{
  if x < 5 then x else F(x - 1)
}

function G(x: int): int
  decreases x
{
  if 1 <= x then G(x - 2) else x
}

function H(x: int): int
  decreases x + 30
{
  if x < -30 then x else H(x - 1)
}

function I(x: nat, y: nat): int
  decreases x + y
{
  if x == 0 || y == 0 then
    8
  else if x % 2 == y % 2 then
    I(x - 1, y)
  else
    I(x, y - 1)
}

function M(x: int, b: bool): int
  decreases if b then 0 else 1
{
  if b then x else M(x + 20, true)
}

function L(x: int): int
  decreases 80 - x
{
  if x < 80 then L(x + 1) + 8 else x
}

function J(x: nat, y: nat): int
  decreases x, y
{
  if x == 0 then
    y
  else if y == 0 then
    J(x - 1, 2)
  else
    J(x, y - 2)
}
