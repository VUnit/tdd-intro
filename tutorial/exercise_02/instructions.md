# Exercise 02
## Purpose

* Learn how to create a testbench with test cases
* Learn the advantages of independent test cases
* Learn how to use VUnit together with your simulator GUI

After this exercise you will be able to work with test cases and you will know the basic workflow with VUnit.

More information on this topic can be found in our [user guide](http://vunit.github.io/user_guide.html), in the [run library documentation](http://vunit.github.io/run/user_guide.html), and in the [command line interface documentation](http://vunit.github.io/cli.html#).


## Instructions

* Create a copy of `exercise_02/original` named `exercise_02/workspace`.
* Open `exercise_02/workspace/test/tb_counter.vhd` in your text editor. Get acquainted with the tests being performed.
* If you have **more than one** simulator on your path you need to select one of them. `<simulator>` = `ghdl`, `modelsim`, `rivierapro`, `activehdl` or `incisive`.

	``` console
    set VUNIT_SIMULATOR=<simulator>
    ```
* Run the script from the command line with the list option:

    ``` console
    python run.py --list
    ```

* Run just the `tb_counter` testbench by applying a pattern just matching its name

    ``` console
    python run.py *.all
    ```

    Identify what part of the testbench that failed based on the call stack. Do we know if the reset works?

* Open `tb_counter_with_test_cases.vhd` in your text editor. Note how the test case comments of `tb_counter.vhd` are turned into VUnit test cases.

* Run the script from the command line with the list option:

    ``` console
    python run.py --list
    ```

* Run the `tb_counter_with_test_cases` testbench

    ``` console
    python run.py *test_cases*
    ```

    What do we know about the reset functionality. Does it work?

    VUnit skips test cases after a failing test case since the result of the remaining test cases may be affected by the preceding error state.

* Remove the `-- vunit_pragma run_all_in_same_sim` at the bottom of `tb_counter_with_test_cases.vhd` to run all test cases independently in different simulations

    ``` console
    python run.py *test_cases*
    ```

    What do we know about the reset functionality. Does it work?

    Note the elapsed time for the simulation (displayed at the bottom of the test report)

* Run the test cases in three parallel threads. Note that you need three licenses to run in parallel.

    ``` console
    python run.py *test_cases* --num-threads 3
    ```

    What happened to the elapsed time?

* Make sure you've selected a simulator that has a GUI. If not, switch to one that has, for example

    ``` console
    set VUNIT_SIMULATOR=rivierapro
    ```

* Open `run.py` in your text editor. Note that a simulator specific compile option has been added to remove optimizations such that the test is more easily debugged in the GUI

    ``` python
    # Set simulator specific compile options
    prj.set_compile_option("rivierapro.vcom_flags", ["-dbg"])
    ```

* Open the GUI to debug the failing test case

    ``` console
    python run.py *loaded* --gui
    ```

* Run the test case by calling `vunit_run` in the console window. Watch it fail.

    ``` console
    vunit_run
    ```

* Debug like you normally would or simply fix the bug in `src/counter.vhd`

    ``` vhdl
    count <= count;                   -- BUG: Should be count <= load_data;
    ```

* Compile and restart test case by calling `vunit_restart` in the console window. Watch it pass.

    ``` console
    vunit_restart
    ```

    A passing test stops at

    ``` vhdl
    std.env.stop(status);
    ```

* Close the simulator and run a regression test to make sure you didn't break anything

    ``` console
    python run.py *test_cases* --num-threads 3
    ```

* Passing checks are silent by default. You can make them visible on the display by adding a `show` procedure call to your testbench

    ``` vhdl
    test_runner_setup(runner, runner_cfg);
    show(display_handler, pass);
    ```

* Re-run with the verbose option.

    ``` console
    python run.py *test_cases* --verbose
    ```

* Run the script with the help option. Note that many options have a shorthand version.

    ``` console
    python run.py *test_cases* --help
    ```
