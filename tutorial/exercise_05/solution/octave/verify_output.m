% Parse arguments
arg_list = argv;
stimuli_file = arg_list{1};
dut_response_file = arg_list{2};

% Read stimuli and response
stimuli = csvread(stimuli_file);
dut_response = csvread(dut_response_file);

% Compare
if isequal(dut_response, stimuli + 1)
  quit(0)
else
  printf("ERROR!\nGot:      %s\nExpected: %s\n", mat2str(dut_response), mat2str(stimuli + 1))
  quit(1)
end;
