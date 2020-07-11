import requests
import sys
import webbrowser
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import ctypes

def quickedit(enabled=1): # This is a patch to the system that sometimes hangs
        kernel32 = ctypes.windll.kernel32
        if enabled:
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
        else:
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100))

quickedit(0)
inputfile = pd.read_excel(r"Copyactualinput.xlsx")
df = pd.read_csv(r"MozData.csv")
df = df.astype(str)

spamperc = input("Enter the spam score percentage you wish to reject for\n")
PAnum = int(input("Enter the PA number below which you wish to reject for\n"))
DAnum = int(input("Enter the DA number below which you wish to reject for\n"))

AnchorTextCheck = inputfile['Exclusions'].to_list()
Web2Check = inputfile['Web2.0'].to_list()
BrandsCheck = inputfile['Brands'].to_list()
OthersCheck = inputfile['Others'].to_list()
Others1Check = inputfile['Others1'].to_list()
Others2Check = inputfile['Others2'].to_list()


# In[297]:


Anchor = []
Web2 = []
Brands = []
Others = []
Others1 = []
Others2 = []

AnchorTextCheck = list(filter(lambda x: x == x, AnchorTextCheck))
Web2Check = list(filter(lambda x: x == x, Web2Check))
BrandsCheck = list(filter(lambda x: x == x, BrandsCheck))
OthersCheck = list(filter(lambda x: x == x, OthersCheck))
Others1Check = list(filter(lambda x: x == x, Others1Check))
Others2Check = list(filter(lambda x: x == x, Others2Check))

for i in AnchorTextCheck:
    Anchor.append(i.lower())

for i in Web2Check:
    Web2.append(i.lower())

for i in BrandsCheck:
    Brands.append(i.lower())

for i in OthersCheck:
    Others.append(i.lower())
    
for i in Others1Check:
    Others1.append(i.lower())
    
for i in Others2Check:
    Others2.append(i.lower())


# In[298]:


InitializingFalse = [False for i in range(len(df))]


# In[299]:


df1 = df['URL']
df2 = df['Anchor text']

basisoffilteration = []
for i in range(len(df)):
    for j in Anchor:
        if((j in df1[i].lower()) or (j in df2[i].lower())):
            basisoffilteration.append(j)
            InitializingFalse[i] = True
            break


# In[301]:


dfremovedAnchor = pd.DataFrame(columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score', 'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[302]:


for i in range(len(InitializingFalse)):
    if(InitializingFalse[i] == True):
        rowdata = df.loc[i]
        rowdata = list(rowdata)
        dfremovedAnchor = dfremovedAnchor.append({'KeyWord Searched For' : rowdata[0], 'Inbound Links' : rowdata[1], 
                                                  'URL' : rowdata[2], 'Domain Names' : rowdata[3], 'Anchor text' : rowdata[4], 
                                                  'Spam Score' : rowdata[5], 'PA' : rowdata[6], 'DA' : rowdata[7], 
                                                  'Linking Domains' : rowdata[8], 'Target URL' : rowdata[9], 
                                                  'Link Type' : rowdata[10], 'Link State' : rowdata[11]}, ignore_index = True)
dfremovedAnchor['Basis of Filteration'] = basisoffilteration

bofAnchor = dfremovedAnchor["Basis of Filteration"].value_counts()

print("The anchor text has been filtered out")
dfremovedAnchor.to_csv('FilteredAnchor.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[304]:


Nanlist = []
for i in range(len(InitializingFalse)):
    if(InitializingFalse[i] == True):
        Nanlist.append(float("NaN"))
    else:
        Nanlist.append(1)
df['ToDrop'] = Nanlist


# In[305]:


df.dropna(inplace = True, subset = ['ToDrop'])
df = df.reset_index(drop = True)
df = df.drop(columns = ['ToDrop'])


# In[306]:


WebFalse = [False for i in range(len(df))]


# In[307]:


df1 = df['URL']


# In[308]:


basisoffilteration = []
for i in range(len(df1)):
    for j in Web2:
        if((j in df1[i].lower())):
            basisoffilteration.append(j)
            WebFalse[i] = True
            break


# In[309]:


dfremovedWeb2 = pd.DataFrame(columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Basis of Filteration', 'Anchor text', 'Spam Score', 'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[310]:


for i in range(len(WebFalse)):
    if(WebFalse[i] == True):
        rowdata = df.loc[i]
        rowdata = list(rowdata)
        dfremovedWeb2 = dfremovedWeb2.append({'KeyWord Searched For' : rowdata[0], 'Inbound Links' : rowdata[1], 
                                                  'URL' : rowdata[2], 'Domain Names' : rowdata[3], 'Anchor text' : rowdata[4], 
                                                  'Spam Score' : rowdata[5], 'PA' : rowdata[6], 'DA' : rowdata[7], 
                                                  'Linking Domains' : rowdata[8], 'Target URL' : rowdata[9], 
                                                  'Link Type' : rowdata[10], 'Link State' : rowdata[11]}, ignore_index = True)
dfremovedWeb2['Basis of Filteration'] = basisoffilteration

bofWeb2 = dfremovedWeb2["Basis of Filteration"].value_counts()
# In[311]:

print("The Web 2.0 links have been filtered out")
dfremovedWeb2.to_csv('FilteredWeb2.0.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[312]:


Nanlist = []
for i in range(len(WebFalse)):
    if(WebFalse[i] == True):
        Nanlist.append(float("NaN"))
    else:
        Nanlist.append(1)
df['ToDrop'] = Nanlist


# In[313]:


df.dropna(inplace = True, subset = ['ToDrop'])
df = df.reset_index(drop = True)
df = df.drop(columns = ['ToDrop'])


# In[314]:


BrandFalse = [False for i in range(len(df))]


# In[315]:


df1 = df['URL']


# In[316]:


basisoffilteration = []
for i in range(len(df1)):
    for j in Brands:
        if((j in df1[i].lower())):
            basisoffilteration.append(j)
            BrandFalse[i] = True
            break


# In[317]:


dfremovedBrands = pd.DataFrame(columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score', 'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[318]:


for i in range(len(BrandFalse)):
    if(BrandFalse[i] == True):
        rowdata = df.loc[i]
        rowdata = list(rowdata)
        dfremovedBrands = dfremovedBrands.append({'KeyWord Searched For' : rowdata[0], 'Inbound Links' : rowdata[1], 
                                                  'URL' : rowdata[2], 'Domain Names' : rowdata[3], 'Anchor text' : rowdata[4],
                                                  'Spam Score' : rowdata[5], 'PA' : rowdata[6], 'DA' : rowdata[7], 
                                                  'Linking Domains' : rowdata[8], 'Target URL' : rowdata[9], 
                                                  'Link Type' : rowdata[10], 'Link State' : rowdata[11]}, ignore_index = True)

dfremovedBrands['Basis of Filteration'] = basisoffilteration

bofBrands = dfremovedBrands["Basis of Filteration"].value_counts()
# In[319]:

print("The Brand links have been filtered out")
dfremovedBrands.to_csv('FilteredBrands.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[320]:


Nanlist = []
for i in range(len(BrandFalse)):
    if(BrandFalse[i] == True):
        Nanlist.append(float("NaN"))
    else:
        Nanlist.append(1)
df['ToDrop'] = Nanlist


# In[321]:


df.dropna(inplace = True, subset = ['ToDrop'])
df = df.reset_index(drop = True)
df = df.drop(columns = ['ToDrop'])


# In[322]:


OthersFalse = [False for i in range(len(df))]


# In[323]:


df1 = df['URL']


# In[324]:


basisoffilteration = []
for i in range(len(df1)):
    for j in Others:
        if((j in df1[i].lower())):
            basisoffilteration.append(j)
            OthersFalse[i] = True
            break


# In[325]:


dfremovedOthers = pd.DataFrame(columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score', 'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[326]:


for i in range(len(OthersFalse)):
    if(OthersFalse[i] == True):
        rowdata = df.loc[i]
        rowdata = list(rowdata)
        dfremovedOthers = dfremovedOthers.append({'KeyWord Searched For' : rowdata[0], 'Inbound Links' : rowdata[1], 
                                                  'URL' : rowdata[2], 'Domain Names' : rowdata[3], 'Anchor text' : rowdata[4], 
                                                  'Spam Score' : rowdata[5], 'PA' : rowdata[6], 'DA' : rowdata[7], 
                                                  'Linking Domains' : rowdata[8], 'Target URL' : rowdata[9], 
                                                  'Link Type' : rowdata[10], 'Link State' : rowdata[11]}, ignore_index = True)
dfremovedOthers['Basis of Filteration'] = basisoffilteration

bofOthers = dfremovedOthers["Basis of Filteration"].value_counts()
# In[327]:

print("The Other links have been filtered out")
dfremovedOthers.to_csv('FilteredOthers.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[328]:


Nanlist = []
for i in range(len(OthersFalse)):
    if(OthersFalse[i] == True):
        Nanlist.append(float("NaN"))
    else:
        Nanlist.append(1)
df['ToDrop'] = Nanlist


# In[329]:


df.dropna(inplace = True, subset = ['ToDrop'])
df = df.reset_index(drop = True)
df = df.drop(columns = ['ToDrop'])

Others1False = [False for i in range(len(df))]


# In[323]:


df1 = df['Domain Names']


# In[324]:


basisoffilteration = []
for i in range(len(df1)):
    for j in Others1:
        if((j in df1[i].lower())):
            basisoffilteration.append(j)
            Others1False[i] = True
            break


# In[325]:


dfremovedOthers1 = pd.DataFrame(columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score', 'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[326]:


for i in range(len(Others1False)):
    if(Others1False[i] == True):
        rowdata = df.loc[i]
        rowdata = list(rowdata)
        dfremovedOthers1 = dfremovedOthers1.append({'KeyWord Searched For' : rowdata[0], 'Inbound Links' : rowdata[1], 
                                                  'URL' : rowdata[2], 'Domain Names' : rowdata[3], 'Anchor text' : rowdata[4], 
                                                  'Spam Score' : rowdata[5], 'PA' : rowdata[6], 'DA' : rowdata[7], 
                                                  'Linking Domains' : rowdata[8], 'Target URL' : rowdata[9], 
                                                  'Link Type' : rowdata[10], 'Link State' : rowdata[11]}, ignore_index = True)
dfremovedOthers1['Basis of Filteration'] = basisoffilteration

bofOthers1 = dfremovedOthers1["Basis of Filteration"].value_counts()
# In[327]:

print("The Other1 links have been filtered out")
dfremovedOthers1.to_csv('FilteredOthers1.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[328]:


Nanlist = []
for i in range(len(Others1False)):
    if(Others1False[i] == True):
        Nanlist.append(float("NaN"))
    else:
        Nanlist.append(1)
df['ToDrop'] = Nanlist


# In[329]:


df.dropna(inplace = True, subset = ['ToDrop'])
df = df.reset_index(drop = True)
df = df.drop(columns = ['ToDrop'])

# In[330]:
Others2False = [False for i in range(len(df))]


# In[323]:


df2 = df['Anchor text']


# In[324]:


basisoffilteration = []
for i in range(len(df1)):
    for j in Others2:
        if((j in df2[i].lower())):
            basisoffilteration.append(j)
            Others2False[i] = True
            break


# In[325]:


dfremovedOthers2 = pd.DataFrame(columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score', 'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[326]:


for i in range(len(Others2False)):
    if(Others2False[i] == True):
        rowdata = df.loc[i]
        rowdata = list(rowdata)
        dfremovedOthers2 = dfremovedOthers2.append({'KeyWord Searched For' : rowdata[0], 'Inbound Links' : rowdata[1], 
                                                  'URL' : rowdata[2], 'Domain Names' : rowdata[3], 'Anchor text' : rowdata[4], 
                                                  'Spam Score' : rowdata[5], 'PA' : rowdata[6], 'DA' : rowdata[7], 
                                                  'Linking Domains' : rowdata[8], 'Target URL' : rowdata[9], 
                                                  'Link Type' : rowdata[10], 'Link State' : rowdata[11]}, ignore_index = True)
dfremovedOthers2['Basis of Filteration'] = basisoffilteration

bofOthers2 = dfremovedOthers2["Basis of Filteration"].value_counts()
# In[327]:

print("The Other2 links have been filtered out")
dfremovedOthers2.to_csv('FilteredOthers2.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Basis of Filteration', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[328]:


Nanlist = []
for i in range(len(Others2False)):
    if(Others2False[i] == True):
        Nanlist.append(float("NaN"))
    else:
        Nanlist.append(1)
df['ToDrop'] = Nanlist


# In[329]:


df.dropna(inplace = True, subset = ['ToDrop'])
df = df.reset_index(drop = True)
df = df.drop(columns = ['ToDrop'])


dfremovedSpam = pd.DataFrame(columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Spam Score', 'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[331]:


#for i in range(len(df['Spam Score'])):
    #if(df['Spam Score'][i] == '--'):
        #df['Spam Score'][i] = '0%'
df.loc[df['Spam Score'] == '--', 'Spam Score'] = '0%'
df['Spam Score'] = (df['Spam Score'].str.strip('%').astype(float))


# In[332]:


spamlist = [False for i in range(len(df))]


# In[333]:


for i in range(len(df)):
    if(float(df['Spam Score'][i]) > float(spamperc)):
        spamlist[i] = True


# In[334]:
df['Spam Score'] = df['Spam Score'].astype(str)

for i in range(len(df)):
    if(spamlist[i] == True):
        rowdata = df.loc[i]
        rowdata = list(rowdata)
        dfremovedSpam = dfremovedSpam.append({'KeyWord Searched For' : rowdata[0], 'Inbound Links' : rowdata[1], 
                                                  'URL' : rowdata[2], 'Domain Names' : rowdata[3], 'Anchor text' : rowdata[4], 
                                                  'Spam Score' : rowdata[5], 'PA' : rowdata[6], 'DA' : rowdata[7], 
                                                  'Linking Domains' : rowdata[8], 'Target URL' : rowdata[9], 
                                                  'Link Type' : rowdata[10], 'Link State' : rowdata[11]}, ignore_index = True)


# In[335]:

print("The spam score has been filtered out")
dfremovedSpam.to_csv('FilteredSpam.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


Nanlist = []
for i in range(len(df)):
    if(spamlist[i] == True):
        Nanlist.append(float("NaN"))
    else:
        Nanlist.append(1)
df['ToDrop'] = Nanlist
df.dropna(inplace = True, subset = ['ToDrop'])
df = df.reset_index(drop = True)
df = df.drop(columns = ['ToDrop'])


# In[337]:


dfremovedPA = pd.DataFrame(columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Spam Score', 'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[338]:


PAlist = [False for i in range(len(df))]


# In[339]:


for i in range(len(df)):
    if(int(df['PA'][i]) < PAnum):
        PAlist[i] = True


# In[340]:


for i in range(len(df)):
    if(PAlist[i] == True):
        rowdata = df.loc[i]
        rowdata = list(rowdata)
        dfremovedPA = dfremovedPA.append({'KeyWord Searched For' : rowdata[0], 'Inbound Links' : rowdata[1], 
                                                  'URL' : rowdata[2], 'Domain Names' : rowdata[3], 'Anchor text' : rowdata[4], 
                                                  'Spam Score' : rowdata[5], 'PA' : rowdata[6], 'DA' : rowdata[7], 
                                                  'Linking Domains' : rowdata[8], 'Target URL' : rowdata[9], 
                                                  'Link Type' : rowdata[10], 'Link State' : rowdata[11]}, ignore_index = True)


# In[341]:

print("The PA results have been filtered out")
dfremovedPA.to_csv('FilteredPA.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[342]:


Nanlist = []
for i in range(len(df)):
    if(PAlist[i] == True):
        Nanlist.append(float("NaN"))
    else:
        Nanlist.append(1)
df['ToDrop'] = Nanlist
df.dropna(inplace = True, subset = ['ToDrop'])
df = df.reset_index(drop = True)
df = df.drop(columns = ['ToDrop'])


# In[343]:


dfremovedDA = pd.DataFrame(columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Spam Score', 'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[344]:


DAlist = [False for i in range(len(df))]


# In[345]:


for i in range(len(df)):
    if(int(df['DA'][i]) < DAnum):
        DAlist[i] = True


# In[346]:


for i in range(len(df)):
    if(DAlist[i] == True):
        rowdata = df.loc[i]
        rowdata = list(rowdata)
        dfremovedDA = dfremovedDA.append({'KeyWord Searched For' : rowdata[0], 'Inbound Links' : rowdata[1], 
                                                  'URL' : rowdata[2], 'Domain Names' : rowdata[3], 'Anchor text' : rowdata[4], 
                                                  'Spam Score' : rowdata[5], 'PA' : rowdata[6], 'DA' : rowdata[7], 
                                                  'Linking Domains' : rowdata[8], 'Target URL' : rowdata[9], 
                                                  'Link Type' : rowdata[10], 'Link State' : rowdata[11]}, ignore_index = True)


# In[347]:

print("The DA results have been filtered out")
dfremovedDA.to_csv('FilteredDA.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])


# In[348]:


Nanlist = []
for i in range(len(df)):
    if(DAlist[i] == True):
        Nanlist.append(float("NaN"))
    else:
        Nanlist.append(1)
df['ToDrop'] = Nanlist
df.dropna(inplace = True, subset = ['ToDrop'])
df = df.reset_index(drop = True)
df = df.drop(columns = ['ToDrop'])


dictAnchor = bofAnchor.to_dict()
dictBrands = bofBrands.to_dict()
dictWeb2 = bofWeb2.to_dict()
dictOthers = bofOthers.to_dict()
dictOthers1 = bofOthers1.to_dict()
dictOthers2 = bofOthers2.to_dict()

temp = []
for i in dictAnchor.keys():
    temp.append(['Filtered Anchor', i, dictAnchor[i]])
for i in dictBrands.keys():
    temp.append(['Filtered Brands', i, dictBrands[i]])
for i in dictWeb2.keys():
    temp.append(['Filtered Web 2.0', i, dictWeb2[i]])
for i in dictOthers.keys():
    temp.append(['Filtered Others', i, dictOthers[i]])
for i in dictOthers1.keys():
    temp.append(['Filtered Others 1', i, dictOthers1[i]])
for i in dictOthers2.keys():
    temp.append(['Filtered Others 2', i, dictOthers2[i]])

NumberofFiltered = pd.DataFrame(temp, columns = ['Name of file', 'Basis of Filteration', "Number of times Filtered out"])
NumberofFiltered.to_csv('NumberofFiltered.csv', index = False)

print("The process is done executing")
df.to_csv('FinalDataAfterFiltering.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State'])
