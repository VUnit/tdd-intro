% Parse arguments
arg_list = argv;
output_path = arg_list{1};

% Write 10 random integers between 0 - 1000 to file
output_file_name = fullfile(output_path, "stimuli.csv");
csvwrite(output_file_name, randi(1000, 1, 10));

quit(0)
