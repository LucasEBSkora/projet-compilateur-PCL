with Ada.Text_IO; use Ada.Text_IO;

procedure unDebut is

  a , b: integer;
  type example is record c: integer end record;

  begin
    a := a + a - a;
    a := a - a - a;
    a := a * a * a;
    a := a / a / a;
    a := a rem a rem a;
    a := a and b and a;
    a := a and then b and then a;
    a := a or b or a;
    a := a or else b or else a;
    a := a.b.c;
  end unDebut;