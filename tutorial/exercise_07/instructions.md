# Exercise 07
## Purpose

* Learn how to use VUnit verification components
* Learn some basic concepts for VUnit message passing

After this exercise you will be able to use VUnit to control common standard interfaces. You will also understand how VUnit can manage multiple DUT interfaces in parallel.

More information on this topic can be found in the [verification component user guide](http://vunit.github.io/verification_components/user_guide.html) and in this [LinkedIn article](https://www.linkedin.com/pulse/vunit-bfms-simple-emailing-lars-asplund).

## Instructions

* Create a copy of `exercise_07/original` named `exercise_07/workspace`.
* The incrementer presented in exercise 05 and 06 is based on AXI interfaces. AXI stream for input and output data and AXI Lite for a control interface which we didn't use in previous exercises. This exercise will raise the abstraction of previous testbenches by using VUnit bus functional models (BFM) rather than controlling the interfaces at the lowest bit level. Open `exercise_07/workspace/test/tb_bfm.vhd`. At the bottom of the testbench you'll find three BFMs:
  * `axi_stream_master` which connects to the input AXI stream on the incrementer.
  * `axi_stream_slave` which connects to the output AXI stream on the incrementer.
  * `axi_lite_master` which connects to the incrementer AXI Lite control bus.

  All these BFMs have a single generic, a handle, which provides the configuration of the BFM as well as gives the BFM instance a unique identifier in case we have several instances of the same BFM. All handles are created at the top of the testbench.

  ``` vhdl
    constant stream_data_length : positive            := 16;
    constant ctrl_data_length   : positive            := 32;

    constant axi_stream_slave   : axi_stream_slave_t  := new_axi_stream_slave(data_length => stream_data_length,
                                                                              actor => new_actor("AXI Stream Slave"));
    constant axi_stream_master  : axi_stream_master_t := new_axi_stream_master(data_length => stream_data_length,
                                                                              actor => new_actor("AXI Stream Master"));
    constant ctrl_bus           : bus_master_t        := new_bus(data_length => ctrl_data_length,
                                                                 address_length => 8,
                                                                 actor => new_actor("AXI Lite Master"));
  ```

  To communicate with our BFMs we use the message passing paradigm under the hood. You can think of message passing as sending emails and the actor created above with `new_actor` is the email address for the BFM.

  The only test case in the testbench is similar to what we had in exercise 06

  ``` vhdl
        if run("Test DUT with random data") then
          n_samples := rnd.RandInt(5, 10);

          push(q, increment);
          push(q, n_samples);

          info("Number of samples to push: " & to_string(n_samples));
          for i in 1 to n_samples loop
            input_data := rnd.RandSlv(input_data'length);
            push(q, input_data);
            push_stream(net, as_stream(axi_stream_master), input_data);
          end loop;
          info("Done pushing!");

          wait until check_done;
        end if;
  ```

  The important differences are that we're pushing the increment used by the incrementer (+1) into the queue used by the `check_output` to verify the output stream. The increment can be changed using the control bus and we'll do that later.

  We have also introduced a new procedure

  ``` vhdl
  push_stream(net, as_stream(axi_stream_master), input_data);
  ```

  This call will take the randomized `input_data` and send that to the `axi_stream_master` BFM telling it to push the `input_data` into the connected input stream. The sending of information to the BFM is done using message passing and you can think of the `net` parameter as the network over which these emails are sent.

  The reason for using `as_stream(axi_stream_master)` rather than just `axi_stream_master` is that `push_stream` is a generic procedure that can be used by other BFMs handling a streaming interface, A BFM driving a UART for example. The `as_stream` function will return the generic parts of `axi_stream_master` such that the generic `push_stream` procedure can be reused.

  Before and after the for loop are two `info` statements. Run the testbench with the verbose flag and notice the time stamps.

  ``` console
  python run.py -v
  ```

  Note that it takes no simulation time to send the `push_stream` commands to the BFM. All messages will be queued in the BFM inbox and the BFM will process the messages one by one and apply the data back-to-back on the incrementer input.

* The `check_output` process has also been updated

  ``` vhdl
  check_output : process is
    variable data : std_logic_vector(stream_data_length - 1 downto 0);
    variable increment : integer;
  begin
    wait on clk until not is_empty(q);
    increment := pop(q);

    for i in 1 to pop(q) loop
      pop_stream(net, as_stream(axi_stream_slave), data);
      check_equal(data, pop_std_ulogic_vector(q) + increment, result("for output_tdata"));
      wait for rnd.RandTime(0 ns, 3 * clk_period, clk_period);
    end loop;

    check_done <= true;
  end process;
  ```

  A `pop_stream` call has been added to tell the AXI stream slave to get us a new `data` from the output of the incrementer. `pop_stream` will send a message to the BFM with this instruction and once new data is available on the stream the BFM will send a reply message which `pop_stream` reads to set `data` and then return.

  You can get a view of the communication taking place. VUnit has a `com_logger` used for tracing of message events and you can make that information visible by adding the following `show` statement:

  ``` vhdl
  test_runner_setup(runner, runner_cfg);
  rnd.InitSeed(rnd'instance_name);

  show(com_logger, display_handler, trace);
  ```

  Re-run the test and you will see events like this

  ``` console
  [1:- - -> AXI Stream Master (stream push)] => AXI Stream Master inbox
  ```

  which means that a message (everything between [ and ]) with ID = 1, destination "AXI Stream Master" and of type "stream push" was written in (=>) AXI Stream Master's inbox. You will see that all pushed messages happened without simulation time passing.

  Then you will see events like these

  ``` console
  AXI Stream Master inbox => [1:- - -> AXI Stream Master (stream push)]
  ```

  which represents the same messages being read from the inbox when the BFM starts processing them.

  You will also see that the `check_output` process requesting data from the AXI stream slave and that that message is processed by that BFM

  ``` console
  [11:- - -> AXI Stream Slave (stream pop)] => AXI Stream Slave inbox
  AXI Stream Slave inbox => [11:- - -> AXI Stream Slave (stream pop)]
  ```

  Once the BFM has a new data it will reply back to the `pop_stream` procedure in `check_output`

  ``` console
  [12:11 AXI Stream Slave -> - (-)] => AXI Stream Slave outbox
  ```

  Message 12 is a reply to message 11 (12:11) but since message 11 was from an anonymous sender (we haven't created an actor for `check_output`) the AXI stream slave will place the message in its own outbox from which the `pop_stream` procedure will read the reply.

  ``` console
  AXI Stream Slave outbox => [12:11 AXI Stream Slave -> - (-)]
  ```

  There is no privacy in message passing!

  Remove the `show` statement to get a cleaner log.

* Go back to the `test_runner` process. All `push_stream` commands were performed without waiting for them to complete. However, it is possible to wait for the BFM to complete all `push_stream` commands issued so far before proceeding. Insert this line after the loop just before the last info statement and re-run the test.

  ``` vhdl
  wait_until_idle(net, as_sync(axi_stream_master));
  ```

  You should now see a time difference between the two logs.

  `wait_until_idle` will send a message to the BFM which the BFM will reply to once it's idle. When the reply is received `wait_until_idle` will return. A BFM can define what being idle means but a typical implementation is to reply to the message immediately when all preceding messages have been consumed. `wait_until_idle` is also a standard procedure that most verification components can provide to support synchronization of activities. Just like we used `as_stream` with standard stream operations we use `as_sync` with standard synchronization operations.

* So far, we've been pushing input data back-to-back but that's not always what we want. In exercise 06 we had a random delay between every data in the stream and to do that with BFMs we can send a command putting it to sleep for a while. Add the following line after the `push_stream` call:

  ``` vhdl
  wait_for_time(net, as_sync(axi_stream_master), rnd.RandTime(0 ns, 3 * clk_period, clk_period));
  ```

  `wait_for_time` is another standard synchronization command and if you re-run the test you should see an increased delay between the time stamps.

* The purpose of sending asynchronous messages that takes no simulation time is that you can control multiple interfaces in parallel from the same process. Having a single process coordinating all activities makes it easier to understand what the test is doing.

  To test that we're going to randomize the increment and write that to the incrementer while data is being pushed on its input. First randomize the increment by updating the beginning of the test case

  ``` vhdl
    if run("Test DUT with random data") then
      increment := rnd.RandInt(0, 255);
      n_samples := rnd.RandInt(5, 10);
  ```

  Then write the new value by adding a `write_bus` call

  ``` vhdl
        push(q, increment);
        push(q, n_samples);

        write_bus(net, ctrl_bus, increment_reg_addr, to_slv(increment, ctrl_data_length));
  ```

  `write_bus` takes the `ctrl_bus` handle of our AXI Lite master BFM and commands it to perform a write to address `increment_reg_addr` (a constant set to 0). The value to write is the increment converted to a std_logic_vector.

  Re-run your test.

  You should get an error because the new increment didn't get written before the first input data was processed by the incrementer. In this case we don't really want the concurrency so you should update your code:

  ``` vhdl
  write_bus(net, ctrl_bus, increment_reg_addr, to_slv(increment, data_length(ctrl_bus)));
  wait_until_idle(net, as_sync(ctrl_bus));
  ```

  Re-run and it should pass.

* Instead of doing a concurrent write operation we can try a concurrent read operation. Update your code to the following:

  ``` vhdl
  write_bus(net, ctrl_bus, increment_reg_addr, to_slv(increment, data_length(ctrl_bus)));
  wait_until_idle(net, as_sync(ctrl_bus));

  read_bus(net, ctrl_bus, increment_reg_addr, ctrl_data);
  info("Increment is " & to_string(to_integer(ctrl_data)));
  ```

  Run the test and you will see the randomized value of the increment.

  The problem is that a read operation is inherently blocking. `read_bus` will send a message to the BFM instructing it to perform a read of address `increment_reg_addr` and then wait for a reply message containing the value read. Once the reply is received the value is placed in `ctrl_data` and the procedure returns.

* To really test that it's possible to read a register while streaming data we need to send the read message to the BFM, then proceed to start streaming data and then, at some later point in time, have a look at the reply message from the BFM. To do that we need to use a read operation that doesn't wait for the data but allow you to check that reply later. Replace the two last lines with

  ``` vhdl
  read_bus(net, ctrl_bus, increment_reg_addr, reference);
  ```

  Rather than returning the data this procedure will just send the read command to the BFM and then return a reference which allow you to fetch the reply later. Let's fetch the data after the loop

  ``` vhdl
  info("Done pushing!");

  await_read_bus_reply(net, reference, ctrl_data);
  info("Increment is " & to_string(to_integer(ctrl_data)));
  ```

  Re-run the test and you should see the same value. The difference is that the read operation was performed concurrently with the data streaming.
