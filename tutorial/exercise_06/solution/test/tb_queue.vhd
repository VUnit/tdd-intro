library vunit_lib;
context vunit_lib.vunit_context;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std_unsigned.all;

library osvvm;
use osvvm.RandomPkg.all;

library common_lib;

entity tb_queue is
  generic(
    runner_cfg : string);
end entity;

architecture test of tb_queue is
  constant clk_period : time    := 4 ns;
  constant q          : queue_t := new_queue;

  signal clk                         : std_logic := '0';
  signal input_tvalid, output_tvalid : std_logic := '0';
  signal input_tdata                 : std_logic_vector(15 downto 0);
  signal output_tdata                : std_logic_vector(input_tdata'range);
  signal check_done                  : boolean   := false;
begin

  test_runner : process
    variable rnd       : RandomPType;
    variable n_samples : integer;
  begin
    test_runner_setup(runner, runner_cfg);
    show(check_logger, display_handler, pass);

    while test_suite loop
      if run("Test DUT with random data") then
        n_samples := rnd.RandInt(5, 10);
        push(q, n_samples);

        for i in 1 to n_samples loop
          input_tdata <= rnd.RandSlv(input_tdata'length);

          input_tvalid <= '0';
          wait for rnd.RandTime(0 ns, 3 * clk_period, clk_period);

          input_tvalid <= '1';
          wait until rising_edge(clk);

          push(q, input_tdata);
        end loop;

        wait until check_done;
      end if;
    end loop;

    test_runner_cleanup(runner);
  end process;

  test_runner_watchdog(runner, 1 ms);

  check_output : process is
  begin
    wait on clk until not is_empty(q);

    for i in 1 to pop(q) loop
      wait until rising_edge(clk) and output_tvalid = '1';
      check_equal(output_tdata, pop_std_ulogic_vector(q) + 1, result("for output_tdata"));
    end loop;

    check_done <= true;
  end process;

  incrementer_inst : entity common_lib.incrementer
    generic map (
      delay => 10)
    port map (
      clk => clk,

      input_tdata  => input_tdata,
      input_tvalid => input_tvalid,

      output_tdata  => output_tdata,
      output_tvalid => output_tvalid);

  clk <= not clk after clk_period/2;

end;
