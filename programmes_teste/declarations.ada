with Ada.Text_IO; use Ada.Text_IO;

procedure proc is

  type potato;
  type carrot is access potato;
  type stock is record  p : potato; c1, c2: carrot; end record;

  a : potato;
  b, c : carrot := a;
  d : stock;

  procedure proc2 is begin
    d.c1 := a;
  end;

  procedure proc3 (a: in integer; b,c : in out integer) is 
    type internal is access carrot;
    e: integer;
  begin 
    e := a;
  end proc3;

  function two return integer is begin
    return 2;
  end;

  function make(p: in potato; c, l: in carrot) return stock is
    s: stock;
  begin
    s.p := p;
    s.c1 := c;
    s.c2 := l;
    return s;
  end make;

begin
end proc;