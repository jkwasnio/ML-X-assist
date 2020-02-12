%
% 
% INPUT:
% tape.mat
% diag_top.mat
% OUTPUT:
% density1b.mat : FILE
% tape.mat : FILE (APPEDING!)


%%% prelude %%%
% change directory to current working directory
% (MATLAB does not do this automatically)
cd(getenv('PWD'));

% One body densities in the working orbital representation
tic
%% load
load('tape.mat',...
     'MA','NA','symA','mA','NsA',...
     'MB','NB','symB','mB','NsB',...
     'T')
load('diag_top.mat',...
     'node0A','Nat_spA_pop',...
     'node0B','Nat_spB_pop');
%% process
if symA==1
	Ns1A=create_bos_ns(NA-1,mA);
	Nstates1A = nchoosek(NA+mA-2,mA-1);
end
if symA==-1
	Ns1A=create_fer_ns(NA-1,mA);
	Nstates1A = nchoosek(mA,NA-1);
end
map2A=create_mapmat(Ns1A,NsA,symA);
%
dmat1A_sf=zeros(mA,mA,T,MA);
for l=1:MA
    dmat1A_sf(:,:,:,l)=create_dmat(NsA,squeeze(node0A(:,l,:)),map2A);
end
%
dmat1A_trans_sf=zeros(mA,mA,T,MA,MA);
for l=1:MA
    for l1=1:MA
    dmat1A_trans_sf(:,:,:,l,l1)=create_dmat_trans(NsA,squeeze(node0A(:,l,:)),squeeze(node0A(:,l1,:)),map2A);
    end
end
%
if symB==1
	Ns1B=create_bos_ns(NB-1,mB);
	Nstates1B = nchoosek(NB+mB-2,mB-1);
end
if symB==-1
	Ns1B=create_fer_ns(NB-1,mB);
	Nstates1B = nchoosek(mB,NB-1);
end
map2B=create_mapmat(Ns1B,NsB,symB);
%
dmat1B_sf=zeros(mB,mB,T,MB);
for l=1:MB
    dmat1B_sf(:,:,:,l)=create_dmat(NsB,squeeze(node0B(:,l,:)),map2B);
end
%
dmat1B_trans_sf=zeros(mB,mB,T,MB,MB);
for l=1:MB
    for l1=1:MB
    dmat1B_trans_sf(:,:,:,l,l1)=create_dmat_trans(NsB,squeeze(node0B(:,l,:)),squeeze(node0B(:,l1,:)),map2B);
    end
end
%
dmat1A=zeros(mA,mA,T);
for i=1:mA
    for j=1:mA
        clear C;
        C(1,1,1:T)=sum(squeeze(dmat1A_sf(i,j,1:T,:)).*Nat_spA_pop(:,1:T)',2);
        dmat1A(i,j,:)=dmat1A(i,j,:)+C(1,1,1:T);
    end
end
%
dmat1B=zeros(mB,mB,T);
for i=1:mB
    for j=1:mB
        clear C;
        C(1,1,1:T)=sum(squeeze(dmat1B_sf(i,j,1:T,:)).*Nat_spB_pop(:,1:T)',2);
        dmat1B(i,j,:)=dmat1B(i,j,:)+C(1,1,1:T);
    end
end
%% save
save('density1b.mat',...
     'dmat1A_sf','dmat1A_trans_sf','dmat1A',...
     'dmat1B_sf','dmat1B_trans_sf','dmat1B')
save('tape.mat',...
    'Ns1A','map2A','Ns1B','map2B',...
    '-append')
disp('One-body Density matrices produced!');
%%
toc
