%Daniel Akrong ENAE420 HW#3 3/9/22

clear; close all; clc
 
format short e
 
% Material, geometry and applied load
E=2.0e+11; % Young's modulues inPascals
Area=0.05; % Cross-sectional area in square meters
L=2;       % Length in meters
P=1;       % Applied load in Newton

% For nondimensional solutions
E=1;
Area=1;
L=1;
 
% FE modeling
nedof=4;   % Number of DOF in an element
net=3;     % Total number of elements in the model
ntdof=6;   % Total number of DOF in the model
 
iconm=[1 2 3 4;3 4 5 6;1 2 5 6]; 
% Connectivity matrix relating the element DOF and the global DOF
 
gf=zeros(ntdof,1);      % Initialize the global load vector.
gk=zeros(ntdof,ntdof);  % Intialize the global stiffness matrix.
 
% nrdof=4;                % Number of unknown DOF after reduction
% nreduced=[3 4 5 6];     % Unknown DOF to be determined
% gfr=zeros(nrdof,1);     % Reduced global load vector
% gkr=zeros(nrdof,nrdof); % Reduced global stifness matrix 
 
% (a) and (b)
 
delx=[1 1 1]*L;   % x2-x1 for all elements
dely=[1 1 0]*L;  % y2-y1 for all elements
el=zeros(nedof,1);      % Initialize the element load vector
 
fprintf('Element Stiffness Matrices:\n')
 
for lnum=1:net 
% lnum is the element number currently being assembled
    dx=delx(lnum);
    dy=dely(lnum);
    Bhat=[-dx -dy dx dy];
    ccc=dx*dx+dy*dy;
    elength=sqrt(ccc);
    elnumber=lnum;                    % Element number
    ek=E*Area*Bhat'*Bhat/(elength^3); % Element stiffness matrix
    
    fprintf('Element %d Stiffness Matrix:\n',lnum)
    disp(ek)
 
% Extract the connectivity of the element being assembled.
    iconv(:)=iconm(lnum,:);
    
 
    % Assemble load vector and stiffnessmatrix.
        gf(iconv(:))=gf(iconv(:))+el(:);
        gk(iconv(:),iconv(:))=gk(iconv(:),iconv(:))+ek(:,:);
end
	gf(3)=P;
 
 
fprintf('Global Stiffness Matrix:\n')
disp(gk)
fprintf('Global Load vector without reaction force:\n')
disp(gf)
 
% (c) 
% Apply the geometric boundary condition to reduce the global stiffness
% matrix and the global load vector.
        gfr(:)=gf(nreduced(:))
        gkr(:,:)=gk(nreduced(:),nreduced(:));
        
% Solve for the unknown nodal DOF
reducedDOF=gkr\gfr;
 
fprintf('Nodal DOF solved for P=1N:\n')
disp(reducedDOF)
 
% (d) 
% Determine axial stress in each element.
 
% Nodal DOF vector in expanded form
allDOF=zeros(ntdof,1);
allDOF(nreduced(:))=reducedDOF(:);
  
% Calculate axial stress in each element
elq=zeros(nedof,1); % Initialize the element DOF vector
 
for lnum=1:net
    dx=delx(lnum);
    dy=dely(lnum);
    Bhat=[-dx -dy dx dy];
    ccc=dx*dx+dy*dy;
    elength=sqrt(ccc);
    elengthv(lnum)=elength;
    
        iconv(:)=iconm(lnum,:);
        elq(:)=allDOF(iconv(:)); % Element DOF extracted
    
    estrain(lnum)=Bhat*elq/(elength^2); % Element strain
    estress(lnum)=E*estrain(lnum); % Element stress
end
 
fprintf('Element Stress for P=1N in Pascal:\n')
disp(estress)
 
% (e)
% Reaction forces
reaction=gk*allDOF; % Reaction force plus applied load
 
fprintf('Reaction forces and applied force for P=1N:\n')
disp(reaction)