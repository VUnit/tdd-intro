package string_pkg is
   function to_string (data : integer_vector) return string;
end package;

package body string_pkg is
   function to_string (data : integer_vector) return string is
   begin
     if data'length = 1 then
       return "(" & to_string(data(data'left)) & ")";
     else
       return "()";
     end if;
  end function;
end package body;
