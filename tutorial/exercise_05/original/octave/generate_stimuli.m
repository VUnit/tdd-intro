% Parse arguments
arg_list = argv;
output_path = arg_list{1};

% Create some stimuli
output_file_name = fullfile(output_path, "stimuli.csv");
%stimuli_data = <put some nice stimuli here>
%csvwrite(output_file_name, stimuli_data);

quit(0)
