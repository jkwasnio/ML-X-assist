% Makes tape.
%
% INPUT:
% psi.mat : FILE
% parameters.mat : FILE
% OUTPUT:
% tape.mat : FILE

%%% prelude %%%
% change directory to current working directory
% (MATLAB does not do this automatically)
cd(getenv('PWD'));

tic
%% load 
load('psi.mat');
load('parameters.mat');
%% parameters
MA = tape(4);
MB = tape(5);
NA = tape(8);
symA = tape(9);
mA = tape(10);
NB = tape(20);
symB = tape(21);
mB = tape(22);
n = tape(15);
T = size(time, 2);
length = (xmax-xmin);
dx = length/(n-1);
x = -length/2:dx:length/2;
%% process
% generate all fermionic number states with N particles and m orbitals (A)
if symA==-1
    NsA=create_fer_ns(NA,mA);
    NstatesA = nchoosek(mA,NA);
    map1A=create_occ_mat(NsA);
end
if symA==1
    NsA=create_bos_ns(NA,mA);
    NstatesA = nchoosek(NA+mA-1,mA-1);
    map1A=create_occ_mat(NsA);
end
% generate all fermionic number states with N particles and m orbitals (B)
if symB==-1
    NsB=create_fer_ns(NB,mB);
    NstatesB = nchoosek(mB,NB);
    map1B=create_occ_mat(NsB);
end
if symB==1
    NsB=create_bos_ns(NB,mB);
    NstatesB = nchoosek(NB+mB-1,mB-1);
    map1B=create_occ_mat(NsB);
end
%% save
save('tape.mat',...
     'MA','NA','symA','mA','NsA','NstatesA','map1A',...
     'MB','NB','symB','mB','NsB','NstatesB','map1B',...
     'T','x','dx','n')
disp('Tape read!')
%%
toc  
