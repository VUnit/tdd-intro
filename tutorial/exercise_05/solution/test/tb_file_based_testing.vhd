library vunit_lib;
context vunit_lib.vunit_context;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std_unsigned.all;

library common_lib;

entity tb_file_based_testing is
  generic(
    runner_cfg : string);
end entity;

architecture test of tb_file_based_testing is
  constant clk_period : time := 4 ns;

  signal clk                         : std_logic := '0';
  signal input_tvalid, output_tvalid : std_logic := '0';
  signal input_tdata                 : std_logic_vector(15 downto 0);
  signal output_tdata                : std_logic_vector(input_tdata'range);
begin

  test_runner : process
    variable input_data, expected_data, dut_response : integer_array_t;
  begin
    test_runner_setup(runner, runner_cfg);

    while test_suite loop
      if run("Test DUT with data from file") then
        input_data := load_csv(file_name => join(tb_path(runner_cfg), "input_data.csv"),
                               bit_width => input_tdata'length,
                               is_signed => false);

        expected_data := load_raw(file_name => join(tb_path(runner_cfg), "expected_data.dat"),
                                  bit_width => output_tdata'length,
                                  is_signed => false);

        input_tvalid <= '1';
        for i in 0 to length(input_data) - 1 loop
          input_tdata <= to_slv(get(input_data, i), input_tdata);
          wait until falling_edge(clk);
          check_equal(output_tdata, get(expected_data, i), result("for output_tdata"));
          check_equal(output_tvalid, '1', result("for output_tvalid"));
        end loop;

      elsif run("Test generating and verifying data in hooks") then
        input_data := load_csv(file_name => join(output_path(runner_cfg), "python_data.csv"),
                               bit_width => input_tdata'length,
                               is_signed => false);

        dut_response := new_1d(bit_width => output_tdata'length, is_signed => false);

        input_tvalid <= '1';
        for i in 0 to length(input_data) - 1 loop
          input_tdata <= to_slv(get(input_data, i), input_tdata);
          wait until falling_edge(clk);
          if output_tvalid then
            append(dut_response, to_integer(output_tdata));
          end if;
        end loop;

        save_csv(dut_response, join(output_path(runner_cfg), "dut_response.csv"));

      end if;
    end loop;

    test_runner_cleanup(runner);
  end process;

  test_runner_watchdog(runner, 1 ms);

  incrementer_inst : entity common_lib.incrementer
    port map (
      clk => clk,

      input_tdata  => input_tdata,
      input_tvalid => input_tvalid,

      output_tdata  => output_tdata,
      output_tvalid => output_tvalid);

  clk <= not clk after clk_period/2;

end;
