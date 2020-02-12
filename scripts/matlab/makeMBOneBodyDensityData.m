%% Makes data files for one body density (MB only).
%
% INPUT:
% psi.mat : FILE,  from script call `OutputSTD.py --psi`.
% parameters.mat : FILE,  from script `icefox/scripts/makeParametersMat.py`
% density1b.mat : FILE
% tape.mat : FILE
% OUTPUT:
% gpop.mat : FILE
% dmat1A_grid.mat, dmat1B_grid.mat : FILE

%%% prelude %%%
% change directory to current working directory
% (MATLAB does not do this automatically)
cd(getenv('PWD'));

% One-body densities in the grid representation.
tic
%% load
load('parameters.mat');
load('tape.mat')
load('density1b.mat','dmat1A','dmat1B')
load('psi.mat','node3','node5')
%% process
dmat1A_grid=zeros(T,n);
%
for i=1:mA
    for j=1:mA
        dmat1A_grid=dmat1A_grid+(1/dx).*...
                repmat(squeeze(dmat1A(i,j,1:T)),[1,n]).*...
                squeeze(conj(node3(1:T,i,:))).*...
                squeeze(node3(1:T,j,:));
    end
end
dmat1B_grid=zeros(T,n);
for i=1:mB
    for j=1:mB
        dmat1B_grid=dmat1B_grid+(1/dx).*...
                repmat(squeeze(dmat1B(i,j,1:T)),[1,n]).*...
                squeeze(conj(node5(1:T,i,:))).*...
                squeeze(node5(1:T,j,:));
    end
end
%% save
save('gpop.mat','dmat1A_grid','dmat1B_grid')
disp('Density matrices to grid done!')
%%
toc
