library vunit_lib;
context vunit_lib.vunit_context;
context vunit_lib.vc_context;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std_unsigned.all;

library osvvm;
use osvvm.RandomPkg.all;

library common_lib;
use common_lib.incrementer_pkg.all;

entity tb_bfm is
  generic(
    runner_cfg : string);
end entity;

architecture test of tb_bfm is
  shared variable rnd : RandomPType;

  constant clk_period : time    := 4 ns;
  constant q          : queue_t := new_queue;

  constant stream_data_length : positive := 16;
  constant ctrl_data_length   : positive := 32;

  constant axi_stream_slave : axi_stream_slave_t := new_axi_stream_slave(data_length => stream_data_length,
                                                                         actor       => new_actor("AXI Stream Slave"));
  constant axi_stream_master : axi_stream_master_t := new_axi_stream_master(data_length => stream_data_length,
                                                                            actor       => new_actor("AXI Stream Master"));
  constant ctrl_bus : bus_master_t := new_bus(data_length    => ctrl_data_length,
                                              address_length => 8,
                                              actor          => new_actor("AXI Lite Master"));

  signal clk                       : std_logic := '0';
  signal input_tdata, output_tdata : std_logic_vector(stream_data_length - 1 downto 0);
  signal check_done                : boolean   := false;
begin

  test_runner : process
    variable n_samples  : integer;
    variable increment  : integer := 1;
    variable input_data : std_logic_vector(input_tdata'range);
    variable ctrl_data  : std_logic_vector(ctrl_data_length - 1 downto 0);
    variable reference  : bus_reference_t;
  begin
    test_runner_setup(runner, runner_cfg);
    rnd.InitSeed(rnd'instance_name);

    while test_suite loop
      if run("Test DUT with random data") then
        increment := rnd.RandInt(0, 255);
        n_samples := rnd.RandInt(5, 10);

        push(q, increment);
        push(q, n_samples);

        write_bus(net, ctrl_bus, increment_reg_addr, to_slv(increment, data_length(ctrl_bus)));
        wait_until_idle(net, as_sync(ctrl_bus));

        read_bus(net, ctrl_bus, increment_reg_addr, reference);

        info("Number of samples to push: " & to_string(n_samples));
        for i in 1 to n_samples loop
          input_data := rnd.RandSlv(input_data'length);
          push(q, input_data);
          push_stream(net, as_stream(axi_stream_master), input_data);
          wait_for_time(net, as_sync(axi_stream_master), rnd.RandTime(0 ns, 3 * clk_period, clk_period));
        end loop;
        wait_until_idle(net, as_sync(axi_stream_master));
        info("Done pushing!");

        await_read_bus_reply(net, reference, ctrl_data);
        info("Increment is " & to_string(to_integer(ctrl_data)));

        wait until check_done;
      end if;
    end loop;

    test_runner_cleanup(runner);
  end process;

  test_runner_watchdog(runner, 1 ms);

  check_output : process is
    variable data      : std_logic_vector(stream_data_length - 1 downto 0);
    variable increment : integer;
    variable n_samples  : integer;
  begin
    wait on clk until not is_empty(q);
    increment := pop(q);
    n_samples := pop(q);

    for i in 1 to n_samples loop
      pop_stream(net, as_stream(axi_stream_slave), data);
      check_equal(data, pop_std_ulogic_vector(q) + increment, result("for output_tdata"));
      wait for rnd.RandTime(0 ns, 3 * clk_period, clk_period);
    end loop;

    check_done <= true;
  end process;

  dut_and_vc : block is
    signal input_tvalid  : std_logic;
    signal input_tready  : std_logic;
    signal output_tvalid : std_logic;
    signal output_tready : std_logic;
    signal ctrl_arready  : std_logic;
    signal ctrl_arvalid  : std_logic;
    signal ctrl_araddr   : std_logic_vector(7 downto 0);
    signal ctrl_rready   : std_logic;
    signal ctrl_rvalid   : std_logic;
    signal ctrl_rdata    : std_logic_vector(31 downto 0);
    signal ctrl_rresp    : std_logic_vector(1 downto 0);
    signal ctrl_awready  : std_logic;
    signal ctrl_awvalid  : std_logic;
    signal ctrl_awaddr   : std_logic_vector(7 downto 0);
    signal ctrl_wready   : std_logic;
    signal ctrl_wvalid   : std_logic;
    signal ctrl_wdata    : std_logic_vector(31 downto 0);
    signal ctrl_wstrb    : std_logic_vector(3 downto 0);
    signal ctrl_bvalid   : std_logic;
    signal ctrl_bready   : std_logic;
    signal ctrl_bresp    : std_logic_vector(1 downto 0);
  begin
    incrementer_inst : entity common_lib.incrementer
      generic map (
        delay => 3)
      port map (
        clk => clk,

        input_tdata  => input_tdata,
        input_tvalid => input_tvalid,
        input_tready => input_tready,

        output_tdata  => output_tdata,
        output_tvalid => output_tvalid,
        output_tready => output_tready,

        ctrl_arready => ctrl_arready,
        ctrl_arvalid => ctrl_arvalid,
        ctrl_araddr  => ctrl_araddr,
        ctrl_rready  => ctrl_rready,
        ctrl_rvalid  => ctrl_rvalid,
        ctrl_rdata   => ctrl_rdata,
        ctrl_rresp   => ctrl_rresp,
        ctrl_awready => ctrl_awready,
        ctrl_awvalid => ctrl_awvalid,
        ctrl_awaddr  => ctrl_awaddr,
        ctrl_wready  => ctrl_wready,
        ctrl_wvalid  => ctrl_wvalid,
        ctrl_wdata   => ctrl_wdata,
        ctrl_wstrb   => ctrl_wstrb,
        ctrl_bvalid  => ctrl_bvalid,
        ctrl_bready  => ctrl_bready,
        ctrl_bresp   => ctrl_bresp);

    axi_stream_master_inst : entity vunit_lib.axi_stream_master
      generic map (
        master => axi_stream_master)
      port map (
        aclk   => clk,
        tvalid => input_tvalid,
        tready => input_tready,
        tdata  => input_tdata);

    axi_stream_slave_inst : entity vunit_lib.axi_stream_slave
      generic map (
        slave => axi_stream_slave)
      port map (
        aclk   => clk,
        tvalid => output_tvalid,
        tready => output_tready,
        tdata  => output_tdata);

    axi_lite_master_inst : entity vunit_lib.axi_lite_master
      generic map (
        bus_handle => ctrl_bus)
      port map (
        aclk    => clk,
        arready => ctrl_arready,
        arvalid => ctrl_arvalid,
        araddr  => ctrl_araddr,
        rready  => ctrl_rready,
        rvalid  => ctrl_rvalid,
        rdata   => ctrl_rdata,
        rresp   => ctrl_rresp,
        awready => ctrl_awready,
        awvalid => ctrl_awvalid,
        awaddr  => ctrl_awaddr,
        wready  => ctrl_wready,
        wvalid  => ctrl_wvalid,
        wdata   => ctrl_wdata,
        wstrb   => ctrl_wstrb,
        bvalid  => ctrl_bvalid,
        bready  => ctrl_bready,
        bresp   => ctrl_bresp);

    clk <= not clk after clk_period/2;

  end block dut_and_vc;

end;
