%%% standart prelude %%%
% change path to current working directory
% (matlab does NOT do this automatically!)
cd(getenv('PWD'));
% load parameters
load parameters;

% example
disp(['massA from the parameters file has the value ' num2str(massA)]);
