with Ada.Text_IO; use Ada.Text_IO;

procedure unDebut is

  a , b: integer;
  type example is record c: integer end record;
  d : example;
  
  begin
    a := a + a - a;
    a := a - a + a;
    a := a * a / a rem b;
    a := a rem b / a * a;
    a := a * b rem a / a;
    a := a and then b or a;
    a := a or else b and a;
    a := a.b.c;
  end unDebut;