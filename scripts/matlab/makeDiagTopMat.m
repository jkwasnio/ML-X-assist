% 
%
% INPUT:
% psi.mat : FILE
% tape.mat : FILE
% OUTPUT:
% diag_top.mat : FILE

%%% prelude %%%
% change directory to current working directory
% (MATLAB does not do this automatically)
cd(getenv('PWD'));

% Diagonalize the top node in order to get the natural species functions
% and their corresponding natural populations.
tic
%% load
load('tape.mat','T','MA','MB','NstatesA','NstatesB')
load('psi.mat','node1','node2','node4')
%% process
node0A=zeros(T,MA,NstatesA);
node0B=zeros(T,MB,NstatesB);
for t=1:T
    rhoA=zeros(MA,MA);
    rhoB=zeros(MB,MB);
    for j=1:MA
        for k=1:MA
            for i=1:MA
                rhoA(j,k)=rhoA(j,k) + conj(node1(t,1,MA*(i-1)+j))*node1(t,1,MA*(i-1)+k);
                rhoB(j,k)=rhoB(j,k) + conj(node1(t,1,MB*(j-1)+i))*node1(t,1,MB*(k-1)+i);
            end
        end
    end
    [eig_statA,DA]=eig(rhoA);
    [Nat_spA_pop(:,t) order] = sort(diag(DA),'descend');  %# sort eigenvalues in descending order
    Nat_spA_func(:,:,t) = eig_statA(:,order);
    [eig_statB,DB]=eig(rhoB);
    [Nat_spB_pop(:,t) order] = sort(diag(DB),'descend');  %# sort eigenvalues in descending order
    Nat_spB_func(:,:,t) = eig_statB(:,order);
    for i=1:MA
        for j=1:MA
            node0A(t,j,1:NstatesA)=node0A(t,j,1:NstatesA)+conj(Nat_spA_func(i,j,t)).*node2(t,i,1:NstatesA);
            node0B(t,j,1:NstatesB)=node0B(t,j,1:NstatesB)+conj(Nat_spB_func(i,j,t)).*node4(t,i,1:NstatesB);
        end
    end
end
%% save
save('diag_top.mat',...
     'node0A','Nat_spA_func','Nat_spA_pop',...
     'node0B','Nat_spB_func','Nat_spB_pop');
disp('Top node diagonalized!');
%%
toc
