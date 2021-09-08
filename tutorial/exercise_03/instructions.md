# Exercise 03
## Purpose

* Learn how to include externally compiled libraries
* Learn how to run testbenches and test cases with different generics using VUnit configurations.

More information on this topic can be found in [here](http://vunit.github.io/py/ui.html#configurations).

## Instructions

* Create a copy of `exercise_03/original` named `exercise_03/workspace`.
* Open `exercise_03/workspace/test/tb_counter.vhd` and/or `exercise_03/workspace/test/tb_counter_with_test_cases.vhd`. Note that these testbenches has a `width` generic with a default value of 8.

    ``` vhdl
      generic(
        runner_cfg : string;
        width      : positive := 8);
    ```

    The width generic is used when instantiating the tested counter

    ``` vhdl
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
    ```
* If you have **more than one** simulator on your path you need to select one of them. `<simulator>` = `ghdl`, `modelsim`, `rivierapro`, `activehdl` or `incisive`.

    ``` console
    set VUNIT_SIMULATOR=<simulator>
	```

* Open `exercise_03/workspace/run.py` and notice how the [external library](http://vunit.github.io/py/vunit.html#vunit.ui.VUnit.add_external_library) `lib` is added

  ``` python
  lib = prj.add_external_library("lib", join(root, "..", "exercise_01", "vunit_out", "<your simulator>", "libraries", "lib"))
  ```

  Sometimes it's useful to add libraries that have been compiled external to VUnit, for example vendor libraries and third-party IPs. In this case we're just taking what's already compiled in exercise 01.

* Run all tests with the verbose flag (make sure that you have run exercise01 first, so lib library from exercise01 is compiled)

    ``` console
    python run.py -v
    ```

    Note that the printed counter width for all tests is the default value.

    ``` console
    0 fs - default              -    INFO - This test is running with counter width = 8 bits.
    ```

    A testbench setup using the default generic values is called the __default configuration__.

* Open `run.py` and uncomment the second line below to override the default generic value

    ``` python
    # Set generic for all testbenches and test cases
    #prj.set_generic("width", 16);
    ```

    This will override the generic value used for the default configuration. Re-run with the verbose flag and note the printed counter width for all tests

* Update the previous section to

    ``` python
    # Set generic for all testbenches and test cases
    prj.set_generic("width", 16);

    # Get the tb_counter_with_test_cases testbench from the tb_lib library in which it has been compiled
    tb_counter_with_test_cases = tb_lib.test_bench("tb_counter_with_test_cases")

    # Add a named configuration for tb_counter_with_test_cases with the width generic set to 12
    tb_counter_with_test_cases.add_config(name="width=12", generics=dict(width=12))

    ```

    A Python dictionary (dict) is a list of key/value pairs where the key is the generic name and the value is its value.
    Many generics are simply comma separated:

    ``` python
    generics=dict(integer_g=12, boolean_g=True, string_g="hello", bit_vector_g = "10101010")
    ```

    __Note:__ What types of top-level generics that can be used is simulator specific.

    The default configuration (width=16) will not be run if a named configuration has been added.

* Run with the list option and note the change in the test case naming.

    ``` console
    python run.py -l
    ```

* Re-run with the verbose flag and note the printed counter width for all tests.

* Update the previous section to

    ``` python
    # Set generic for all testbenches and test cases
    prj.set_generic("width", 16);

    # Get the tb_counter_with_test_cases testbench from the tb_lib library in which it has been compiled
    tb_counter_with_test_cases = tb_lib.test_bench("tb_counter_with_test_cases")

    # Add a named configuration with the width generic set to 12
    tb_counter_with_test_cases.add_config(name="width=12", generics=dict(width=12))

    # Get the "Test counting" test case from the tb_counter_with_test_cases testbench
    test_counting = tb_counter_with_test_cases.test("Test counting")

    # Add named configurations for the "Test counting" test case with the width generic set to 32, 64, and 128
    for value in [32, 64, 128]:
        test_counting.add_config(name="width=%s" % value, generics=dict(width=value))
    ```

* Run with the list option and note the test case naming.

* Run the __Test counting__ with the verbose option and note the printed counter width and number of running tests

* What generics will be used if you comment out the configuration for the tb_counter_with_test_cases testbench?

    ``` python
    # Add a named configuration with the width generic set to 12
    # tb_counter_with_test_cases.add_config(name="width=12", generics=dict(width=12))
    ```

    Give it a try!
