library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std_unsigned.all;

entity counter is
  generic(
    width : positive);
  port(
    clk       : in  std_logic;
    rst       : in  std_logic;
    en        : in  std_logic;
    load      : in  std_logic;
    load_data : in  std_logic_vector(width - 1 downto 0);
    count     : out std_logic_vector(width - 1 downto 0) := (others => '0'));
end;

architecture rtl of counter is
begin

  main : process is
  begin
    wait until rising_edge(clk);
    if rst then
      count <= (others => '0');
    elsif load then
      count <= count;                   -- BUG: Should be count <= load_data;
    elsif en then
      count <= count + 1;
    end if;
  end process main;

end;
