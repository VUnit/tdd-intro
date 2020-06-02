package string_pkg is
   function to_string (data : integer_vector) return string;
end package;

package body string_pkg is
  function to_string (data : integer_vector) return string is
    function list(data : integer_vector) return string is
      alias data_i : integer_vector(1 to data'length) is data;
    begin
      if data_i'length = 0 then
        return "";
      elsif data_i'length = 1 then
        return to_string(data_i(1));
      else
        return to_string(data_i(1)) & ", " & list(data_i(2 to data_i'length));
      end if;
    end;
   begin
     return "(" & list(data) & ")";
  end function;
end package body;
