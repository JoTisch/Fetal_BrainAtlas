function [A,B] = BDP2RC(excelsheet)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Description: Match Redcap "Study-ID" and Siemens BDP "Patient-ID"
%(Pseudonymisation ID) based on the DOB of the mother and the fetal MRI
%date. 
%
%Input: Excelsheet (e.g. BDP2RC("INPUTFILENAME") )
%1. Spreadsheet includes the following information (columns from left to
%right): Study-ID; DOB Mother; Fetal MRI;
%2. Spreadsheet includes the following information (columns from left to
%right): DOB Mother; Fetal MRI; Patient ID; 
%
%Output: Excelsheet
%A: Spreadsheet with the following columns: DOB Mother; Fetal MRI; 
%Study-ID; Patient-ID
%B: Spreadsheet with the following columns: DOB_Mother; Fetal MRI, 
%MissingEntries. "MissingEntries" is a binary classification, while
%"True"=Match and "False"=Missing Entry. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% LOAD EXCELSHEET
[~,sheet_name]=xlsfinfo(excelsheet); 
for k=1:numel(sheet_name)
  [data{k},txt{k},raw{k}]=xlsread('matched.xlsx',sheet_name{k});
end

%% REDCAP
% 1. COLUMN: STUDY ID 
RC_StudyID = data{1,1}(:,1); 
% 2. COLUMN: DOB MOTHER 
Offset_datenum= data{1,1}(:,2)+ datenum(1899, 12, 30); % EXCEL offset 
RC_DOB_Mother = datetime(Offset_datenum, 'ConvertFrom', 'datenum', 'Format', 'dd-MM-yyyy'); 
% 3. COLUMN: FETAL MRI 
Offset_datenum= data{1,1}(:,3)+ datenum(1899, 12, 30); % EXCEL offset 
RC_MRI = datetime(Offset_datenum, 'ConvertFrom', 'datenum', 'Format', 'dd-MM-yyyy'); 

A1= RC_DOB_Mother; 
A2= RC_MRI; 

%% BDP 
% 1. COLUMN: DOB MOTHER
Offset_datenum= data{1,2}(:,1)+ datenum(1899, 12, 30); 
BDP_DOB_Mother = datetime(Offset_datenum, 'ConvertFrom', 'datenum', 'Format', 'dd-MM-yyyy'); 
% 2. COLUMN: FETAL MRI 
Offset_datenum= data{1,2}(:,2)+ datenum(1899, 12, 30); 
BDP_MRI = datetime(Offset_datenum, 'ConvertFrom', 'datenum', 'Format', 'dd-MM-yyyy'); 
% 3. COLUMN: PATIENT ID
BDP_PatientID = string(txt{1,2}(2:end,3)); 

B1 = BDP_DOB_Mother; 
B2 = BDP_MRI; 


%% MATCH BDP --> Redcap 
Matched = strings(length(RC_StudyID),1) ;
for i = 1:length(B1)
    C = [B1(i),B2(i)]; 
    D = [A1,A2];
    for kk = 1:length(D)
    ans(kk) = isequal(C,D(kk,:));
    end 
    idx{i} = find(ans==1,10); 
    Matched(idx{i}) = BDP_PatientID(i,1);
end

% Redcap --> BDP 
Matched2 = strings(length(RC_StudyID),1) ;
for i = 1:length(A1)
    C = [B1,B2]; 
    D = [A1(i),A2(i)];
    for kk = 1:length(C)
    ans(kk) = isequal(D,C(kk,:));
    end 
    idx{i} = find(ans==1,10); 
    Matched2(idx{i}) = "Match";
end
    
tmp = (Matched2 == "Match");
MissingEntries = tmp(1:length(B1),1); 

A = [table(A1),table(A2),table(RC_StudyID),table(Matched)]; 
B = [table(B1),table(B2),table(MissingEntries)]; 

writetable(A,'BDP_Redcap.xlsx'); 
writetable(B,'MissingEntries.xlsx');

end 
