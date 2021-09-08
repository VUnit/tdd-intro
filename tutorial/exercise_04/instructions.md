# Exercise 04
## Purpose

* Learn how to use VUnit logging
* Learn how to use VUnit checks

After this exercise you will be able to replace your VHDL report and assert statements with more powerful options.

More information on this topic can be found in our [logging user guide](http://vunit.github.io/logging/user_guide.html) and our [check user guide](http://vunit.github.io/check/user_guide.html) and in [this](https://www.linkedin.com/pulse/vunit-30-while-waiting-vhdl-2017-lars-asplund/) LinkedIn article.


## Instructions

* Create a copy of `exercise_04/original` named `exercise_04/workspace`.
* Open `exercise_04/workspace/test/tb_log_and_check.vhd`. Read the code for one test case at a time and then run the test case with

    ``` console
    python run.py *"Test n "* -v
    ```

    where n is the test case number (1 - 11). Note that there is no DUT being tested in this exercise. We're just trying out different testbench utilities.
