-- Include VUnit functionality
library vunit_lib;
context vunit_lib.vunit_context;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std_unsigned.all;

library lib;

entity tb_counter is
  generic(
    runner_cfg : string;  -- The testbench is controlled through the runner_cfg generic
    width      : positive := 8);
end;

architecture test of tb_counter is
  constant clk_period : time := 4 ns;

  signal clk       : std_logic := '0';
  signal rst       : std_logic;
  signal en        : std_logic;
  signal load      : std_logic;
  signal load_data : std_logic_vector(width - 1 downto 0);
  signal count     : std_logic_vector(width - 1 downto 0);
begin

  test_runner : process
  begin
    -- Setup VUnit
    test_runner_setup(runner, runner_cfg);

    -- Different ways to fail
    assert count = 1;
    check_equal(count, 1);
    info("LSB of count = " & to_string(count(width)));
    wait for 1 hr;

    -- You don't have to stop on the first error but a failing check
    -- will always fail the testbench
    set_stop_count(error, 10);  -- Stop after 10 errors
    disable_stop(error);        -- Don't stop on errors at all

    for i in 1 to 5 loop
      check_equal(count, i);
    end loop;

    -- This line will force the simulation to a stop
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
