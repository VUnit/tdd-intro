library vunit_lib;
context vunit_lib.vunit_context;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std_unsigned.all;

library lib;

entity tb_counter_with_test_cases is
  generic(
    runner_cfg : string;
    width      : positive := 8);
end entity;

architecture test of tb_counter_with_test_cases is
  constant clk_period : time := 4 ns;

  signal clk       : std_logic := '0';
  signal rst       : std_logic := '0';
  signal en        : std_logic := '0';
  signal load      : std_logic := '0';
  signal load_data : std_logic_vector(width - 1 downto 0);
  signal count     : std_logic_vector(width - 1 downto 0);
begin

  test_runner : process
  begin
    test_runner_setup(runner, runner_cfg);
    show(display_handler, pass);

    while test_suite loop
      -- Setup code shared between all test cases
      en <= '1';

      if run("Test counting") then
        wait until rising_edge(clk);

        for i in 0 to 10 loop
          check_equal(count, i);
          wait until rising_edge(clk);
        end loop;

      elsif run("Test that data can be loaded") then
        load      <= '1';
        load_data <= to_slv(177, load_data);
        wait until rising_edge(clk);
        load      <= '0';

        for i in 177 to 187 loop
          wait until rising_edge(clk);
          check_equal(count, i);
        end loop;

      elsif run("Test reset") then
        rst <= '1';
        wait until rising_edge(clk);
        rst <= '0';
        wait until rising_edge(clk);
        check_equal(count, 0);
      end if;
    end loop;

    test_runner_cleanup(runner);
  end process;

  test_runner_watchdog(runner, 1 ms);

  counter_inst : entity lib.counter
    generic map (
      width => width)
    port map (
      clk       => clk,
      rst       => rst,
      en        => en,
      load      => load,
      load_data => load_data,
      count     => count);

  clk <= not clk after clk_period/2;

end;
