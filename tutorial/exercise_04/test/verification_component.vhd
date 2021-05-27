library vunit_lib;
context vunit_lib.vunit_context;

library ieee;
use ieee.std_logic_1164.all;

entity verification_component is
  generic (
    logger : logger_t);
end entity verification_component;

architecture a of verification_component is

begin

  main : process is
    constant checker : checker_t                    := new_checker(logger);
    constant data    : std_logic_vector(7 downto 0) := "00010001";
  begin  -- process main
    wait for 10 ns;
    debug(logger, "all systems are up and running");
    wait for 10 ns;
    check_equal(checker, data, 17, result("for data"));
    wait;
  end process main;

end architecture a;
