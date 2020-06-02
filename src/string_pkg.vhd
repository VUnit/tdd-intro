package string_pkg is
   function to_string (data : integer_vector) return string;
end package;

package body string_pkg is
  function to_string (data : integer_vector) return string is
    function list(data : integer_vector) return string is
    begin
      if data'length = 1 then
        return to_string(data(data'left));
      else
        return to_string(data(data'left)) & ", " & list(data(data'left + 1 to data'right));
      end if;
    end;
   begin
     if data'length > 1 then
       return "(" & list(data) & ")";
     elsif data'length = 1 then
       return "(" & to_string(data(data'left)) & ")";
     else
       return "()";
     end if;
  end function;
end package body;
