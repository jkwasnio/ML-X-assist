%%% prelude %%%
% change directory to current working directory
% (MATLAB does not do this automatically)
cd(getenv('PWD'));
% load marameters
load parameters;

%%% script %%%
disp(['massA from the parameters file has the value ' num2str(massA)]);
