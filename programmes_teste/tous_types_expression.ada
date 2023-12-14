with Ada.Text_IO; use Ada.Text_IO;

procedure unDebut is

  a , b: integer;
  caracter: Character;

  begin
    caracter := '\0';
    a := a + a;
    a := a - a;
    a := a * a;
    a := a / a;
    a := a rem a;
    a := a = b;
    a := a < b;
    a := a > b;
    a := a <= b;
    a := a >= b;
    a := a and b;
    a := a and then b;
    a := a or b;
    a := a or else b;
    a := -b;
    a.b := caracter;
    a := character'val(caracter);
  end unDebut;