with Ada.Text_IO; use Ada.Text_IO;

procedure unDebut is

  a , b: integer;
  caracter: Character;
  
  function func return integer is
  begin
    return 27 / 9;
  end func;
  
  begin
    begin 
      a := 21 + 3;
      func();
    end;
    if caracter = 'c' then
      put(caracter);
    end if;
    if a > 20 then
      for b in 20 .. a loop
        put(b);
      end loop;
    elsif a < 10 then
      for b in reverse a .. 10 loop
        put(b+a);
      end loop;
    else
      b := character'val('0');
      while b < a loop
        put(b);
        b := b + 1;
      end loop;
    end if;
  end unDebut;