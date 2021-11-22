library vunit_lib;
context vunit_lib.vunit_context;

library ieee;
use ieee.std_logic_1164.all;

entity tb_log_and_check is
  generic(
    runner_cfg : string);
end;

architecture test of tb_log_and_check is
  constant verification_component_logger : logger_t := get_logger("verification_component");
  constant clk_period : time := 10 ns;

  signal clk : std_logic := '0';
  signal data_bus : std_logic_vector(7 downto 0) := x"00";
begin

  main : process
    variable license_info : log_level_t;
    variable main_logger, foo_logger, bar_logger : logger_t;
    variable file_handler : log_handler_t;
    constant data : std_logic_vector(7 downto 0) := "00010001";
  begin
    test_runner_setup(runner, runner_cfg);

    while test_suite loop
      if run("Test 1 - Basic logging on the display") then
        -- These are visible on the display by default
        info("Informative message for very useful public information");
        warning("A warning");

        -- Error and failure will stop the simulation by default so the failure
        -- below will not be shown
        error("An error but we could still keep running for a while");
        failure("Fatal error, there is most likely no point in going further");

      elsif run("Test 2 - Multiline messages") then
        info("A message can be over" & LF & "multiple lines");

      elsif run("Test 3 - Printing") then
        print("You can print messages that are independent of logging but you will not see them as clearly");

      elsif run("Test 4 - Stop level") then
        -- By default we stop on errors and failures but here I'm
        -- changing the default to only stop on failure.
        set_stop_level(failure);

        info("Informative message for very useful public information");
        warning("A warning");
        error("An error but we could still keep running for a while");
        failure("Fatal error, there is most likely no point in going further");

      elsif run("Test 5 - Show and hide") then
        -- These are not visible on the display by default
        pass("Message from a passing check");
        debug("Debug message for seldom useful or internal information");
        trace("Trace messages only used for tracing program flow");

        -- You can change the default visibility
        show(display_handler, debug);
        hide(display_handler, warning);

        debug("This is now visible");
        warning("This is no longer visible");

      elsif run("Test 6 - Custom log levels") then
        license_info := new_log_level("license", fg => red, bg => yellow, style => bright);
        show(display_handler, license_info);

        log("Mozilla Public License, v. 2.0.", license_info);

      elsif run("Test 7 - Checking") then
        set_stop_level(failure);

        -- A check is a conditional log entry. Many different checks are supported
        -- but this tutorial focuses on the two most common types

        -- check is the equivalent of a VHDL assert
        check(data = "00010000");
        check(data = "00010000", "Unexpected data");

        -- You can change the level but a failing check will always cause a
        -- failed test
        check(data = "00010000", "Unexpected data", level => warning);

        -- By default checks use a logger named check_logger for reporting error messages.
        -- You can get a log on passing checks by showing the pass level for that logger
        show(check_logger, display_handler, pass);
        check(data = "00010001", "Unexpected data");

        -- "Unexpected data" is not a good message for a passing check. Can be
        -- solved using the result function
        check(data = "00010001", result("for data"));
        check(data = "00010000", result("for data"));

        -- Even better messages are received with check_equal which compares
        -- values of the same or similar types.
        check_equal(data, 17, result("for data"));
        check_equal(data, 16, result("for data"));

      elsif run("Test 8 - Custom loggers") then
        info("This is a message to the default logger");
        info(default_logger, "This is also a message to the default logger");

        main_logger := get_logger(main'path_name);
        info(main_logger, "VUnit supports hierarchies of loggers." & LF & "This is useful when you want different parts" & LF & "to have different logging properties." & LF & "A component can for example have a logger generic" & LF & "allowing the user to control its logging behaviour." & LF & "Here I created a hierarchy of two loggers" & LF & "based on the main process path name.");

        foo_logger := get_logger("tb_log_and_check:foo");
        info(foo_logger, "You can also create a hierarchy with a colon separated name such as" & LF & "tb_log_and_check:foo. In this case tb_log_and_check already exists so only the foo" & LF & "logger is created as a child of tb_log_and_check");

        bar_logger := get_logger("bar", parent => get_logger("tb_log_and_check"));
        info(bar_logger, "You can also create a logger and specify its parent. In this case bar is created" & LF & "as a child to tb_log_and_check");

        show(main_logger, display_handler, debug);
        debug(main_logger, "The main logger shows debug messages");
        debug(foo_logger, "The foo logger hides debug messages which is the default behavior");

        hide(get_logger("tb_log_and_check"), display_handler, warning);
        warning(get_logger("tb_log_and_check"), "tb_log_and_check hides warnings");
        warning(main_logger, "main_logger is a child to tb_logger and inherited the setting to hide warnings");

        hide(get_logger("tb_log_and_check"), display_handler, debug, include_children => false);
        debug(main_logger, "Settings must not be inherited");

      elsif run("Test 9 - Giving a logger to a verification component and then control its logging behavior") then
        show(verification_component_logger, display_handler, (pass, debug));
        wait for 100 ns;

      -- Tip: Open verification_component.vhd to see how a custom checker
      -- that will report to your custom logger can be created.

      elsif run("Test 10 - Adding a file handler") then
        -- tb_path(runner_cfg) returns the directory of this testbench. join
        -- creates a full path by joining that directory name with /log.txt
        file_handler := new_log_handler(file_name => join(tb_path(runner_cfg), "log.txt"),
                                        format => csv,
                                        use_color => false);
        set_log_handlers(default_logger, (display_handler, file_handler));
        show(file_handler, (info, debug));

        info("Avoid tons of debug messages on the display but show them in the log file if needed. Have a look!");

        for i in 1 to 100 loop
          debug("Debug message " & to_string(i));
        end loop;

      elsif run("Test 11 - Location preprocessing") then
        info("Unless you run Riviera-PRO with VHDL-2019 there is no information" & LF & "on the location of logs. You can fix that by uncommenting the" & LF & "following line in run.py" & LF & "#PRJ.enable_location_preprocessing()");

      elsif run("Test 12 - Concurrent checks") then
        info("Most checks can also be run concurrently at every clock edge");
        -- The check used in this example is check_not_unknown located at the bottom
        -- of the file.
        show(check_logger, display_handler, pass);
        set_stop_level(failure);

        data_bus <= x"42", "10100X11" after 5 * clk_period, x"17" after 6 * clk_period;
        wait for 10 * clk_period;

      end if;
    end loop;

    test_runner_cleanup(runner);
  end process;

  test_runner_watchdog(runner, 1 ms);

  clk <= not clk after clk_period / 2;

  check_not_unknown(
    clock => clk,
    -- en is a signal allowing us to control when the check is active.
    -- If always active you can use the predefined check_enabled signal
    en => check_enabled,
    expr => data_bus,
    msg => result("for data_bus")
  );

  verification_component_1 : entity work.verification_component
    generic map (
      logger => verification_component_logger);

end;
