# Exercise 01
## Purpose

* Learn how to write a `run.py` script
* Learn how to compile your project
* Learn how to make your existing testbench VUnit compliant
* Learn how a testbench fails and how it passes

After this exercise you will be able to turn a non-VUnit testbench into a fully automated VUnit testbench.

More information on this topic can be found in our [user guide](http://vunit.github.io/user_guide.html) and in the run library [documentation](https://vunit.github.io/run/user_guide.html).

## Instructions

* Create a copy of `exercise_01/original` named `exercise_01/workspace`.
* Open `exercise_01/workspace/run.py` in your text editor. Get acquainted with the content.
* If you have **more than one** simulator on your path you need to select one of them. `<simulator>` = `ghdl`, `modelsim`, `rivierapro`, `activehdl` or `incisive`.
    ``` console
    set VUNIT_SIMULATOR=<simulator>
    ```
* Run the script from the command line with the compile option:

    ``` console
    python run.py --compile
    ```

    All project files (just `src/counter.vhd`) and VUnit packages are found and compiled in dependency order.

* Re-run the compile command. Nothing is re-compiled because nothing has changed. You can always do a clean compile

    ``` console
    python run.py --compile --clean
    ```

* Modify `run.py` to add a `tb_lib` library and add all source files in `test/` to that library

    ``` python
    tb_lib = prj.add_library("tb_lib")
    tb_lib.add_source_files(join(root, "test", "*.vhd"))
    ```

* Re-compile:

    ``` console
    python run.py --compile
    ```

    Only `tb_counter` needs to be compiled.

* Open `test/tb_counter.vhd` and look at the five lines making this a VUnit testbench

    ``` vhdl
    -- Include VUnit functionality
    library vunit_lib;
    context vunit_lib.vunit_context;

    -- The testbench is controlled through the runner_cfg generic
    runner_cfg : string;

    -- Setup VUnit
    test_runner_setup(runner, runner_cfg);

    -- This line will force the simulation to a stop
    test_runner_cleanup(runner);
    ```

* Run `run.py` and watch it fail

    ``` console
    python run.py
    ```

* Remove/fix/comment these lines, one by one, and run the script in between. Watch the different ways to fail

    ``` vhdl
    -- Different ways to fail
    assert count = 1;
    check_equal(count, 1);
    info("LSB of count = " & to_string(count(width)));
    wait for 1 hr;
    ```

    Failing on a testbench that is stuck requires the `test_runner_watchdog`. It's not required for a VUnit testbench but can save you from wasting a lot of simulation time.

    ``` vhdl
    test_runner_watchdog(runner, 1 ms);
    ```

    Full automation requires that all types of errors are detected and handled gracefully.
* The previous errors caused an immediate stop of the simulation. Using VUnit checks you can control when the simulation stops. Run again to see multiple errors.

* Remove the remaining lines before `test_runner_cleanup` to make the testbench pass.
