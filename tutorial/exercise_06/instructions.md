# Exercise 06
## Purpose

After this exercise you will be able to use VUnit queues for communication between concurrent processes.

## Instructions

* Open `exercise_06/test/tb_queue.vhd`. This testbench verifies the same incrementer component used in exercise 05  but rather than using stimuli from file we apply random stimuli. OSVVM provides a lot of randomization functionality and is included in VUnit for that purpose. 

* Run the testbench

  ``` console
  python run.py
  ```

  This may fail if your simulator isn't shipped with OSVVM. If so, do the next step. 

* OSVVM and some native VUnit packages are considered add-ons which are not compiled by default. To use such an add-on, it needs to be activated in the `run.py` script. Add the following line to your script and re-run. It will still fail for other reasons but it should compile properly.

    ``` python
    prj.add_osvvm()
    ```

* The testbench randomizes the number of input samples to apply, the values of those samples as well as the number of clock cycles between valid input samples. Under more complex scenarios like this it gets increasingly inconvenient to have stimuli and verification in the same process, so we are moving the output verification to a separate `check_output` process.

  In order for `check_output` to verify the output data it needs to know the stimuli and we use a VUnit queue to transfer that knowledge from the stimuli process. The queue is declared as a constant at the architecture level to make it accessible to all involved processes.

    ``` vhdl
    constant q : queue_t := new_queue;
    ```

  `q` is not the queue itself but rather a reference to a queue object allocated internally in VUnit. By using constants to represent queues we have more freedom in how the queues can be used, as generics for example.

  The input stimuli are applied with the code below. Note the `push` procedure that pushes every sample into `q`.

  ``` vhdl
    test_runner : process
      variable rnd       : RandomPType;
      variable n_samples : integer;
    begin
      test_runner_setup(runner, runner_cfg);

      while test_suite loop
        if run("Test DUT with random data") then
          n_samples := rnd.RandInt(5, 10);

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
  ```

  To prevent that this process calls `test_runner_cleanup` and terminates the test before all outputs has been verified the process waits for `check_done` to be set true by the checking process. For the checking process to know that it is done it needs to know the value of `n_samples`. To provide that information we simply push that into the queue as well.

  Add such push command right after the assignment of `n_samples`. The format is the same as the already provided push command for `input_tdata`.

  Note that `n_samples` is an integer while `input_tdata` is an std_logic_vector. VUnit allow you to push any native VHDL type, any IEEE type, and some VUnit types into the same queue. This means that all types of information can be communicated through a single channel.

  The check process can now pop the number of expected samples from the queue, loop until that many valid outputs have been received, and verify that each output matches the expectation based on the stimulus also popped from the queue.

  ``` vhdl
  check_output : process is
  begin
    wait on clk until not is_empty(q);

    for i in 1 to pop(q) loop
      wait until rising_edge(clk) and output_tvalid = '1';
      check_equal(output_tdata, pop_std_ulogic_vector(q) + 1, result("for output_tdata"));
    end loop;

    check_done <= true;
  end process;
  ```

  Note that just calling `push` or `pop` can become ambiguous. For those occasions you can use `push_<type>` and `pop_<type>` as exemplified with the `pop_std_ulogic_vector` call above.

* Add a show procedure to make all passing checks visible. Then run the testbench with the verbose option to see what's being checked.
