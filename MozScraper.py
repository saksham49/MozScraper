import requests
import sys
import webbrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

dirname = os.path.dirname(__file__)
chrome = os.path.join(dirname, 'Chrome')
chromeexe = os.path.join(chrome, 'chrome.exe')
chromedriver = os.path.join(chrome, 'chromedriver.exe')
inputfile = pd.read_excel("Copyactualinput.xlsx")


# In[288]:


KeywordsToSearch = inputfile['Keywords'].to_list()
NumberOfResults = inputfile['Number of results'].to_list()
KeywordsToSearch = list(filter(lambda x: x == x, KeywordsToSearch))
NumberOfResults = list(filter(lambda x: x == x, NumberOfResults))


# In[289]:


def felem(driver, selector):
    return driver.find_element_by_css_selector(selector)

#Checking to see requirements (PA/DA)
PA_or_DA = input("Would you like to retrieve the PA domains or the DA domains?\n")
if(PA_or_DA == 'DA'):
    LimitOfLinks = int(input("Enter the maximum value for which DA link should be taken\n"))


#Initializing Chrome
chrome_options = Options()
chrome_options.add_argument('user-data-dir=ChromeData')
chrome_options.add_argument("--start-maximized")
chrome_options.binary_location = chromeexe
chrome_options.add_extension("mozbar.crx")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
executable_path = chromedriver
os.environ["webdriver.chrome.driver"] = executable_path

#Signing in process
driver.get("https://moz.com/login")
try:
    felem(driver, "input[name=email]").send_keys("luvu869@gmail.com")
    try:
        felem(driver, "#remember_me").click()
    except:
        pass
    felem(driver, "input[name=password]").send_keys("9449939429\n")
    time.sleep(2)
except:
    pass

#Iterating through all the keywords we require to search for
globaleven = []
globalodd = []
globaltargeturl = []
globaldofollowlinks = []
globalkeywords = []
globalinboundlinks = []
whichauthority = []
for keywords in range(0, len(KeywordsToSearch)):
    SearchItem = KeywordsToSearch[keywords]
    NumberResults = NumberOfResults[keywords]
    url = "https://google.co.in/search?q=" + SearchItem
    driver.get(url)
    time.sleep(2)
    AnalyticsMoz = []
    count = 0
    linksPAandDA = []
    information = []
    valuesToCheck = []
    PA = []
    DA = []
    
    while(count < NumberResults):
        iframes = driver.find_elements_by_class_name("mozbar-serp-item-wGA7MhRhQ3WS")
        count += len(iframes)

        for iframe in range(len(iframes)):
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame(iframes[iframe])
            time.sleep(1)
            m = driver.find_elements_by_class_name("line")

            for j in range(len(m)):
                information.append(m[j].get_attribute('innerHTML').split()[0].replace(',', ''))

            n = driver.find_elements_by_class_name("links > a")

            for k in n:
                linksPAandDA.append(k.get_attribute('href'))

        PA.extend(linksPAandDA[0::2])
        DA.extend(linksPAandDA[1::2])
        valuesToCheck.extend(information[2::4]) 
        time.sleep(2)
        driver.switch_to.default_content()
        NextButton = []
        
        for button in driver.find_elements_by_css_selector("a.G0iuSb"):
            NextButton.append(button.get_attribute('href'))
        
        try:
            driver.get(NextButton[-1])
            time.sleep(3)
        except:
            break
        
    for value in range(len(valuesToCheck)):
        if(PA_or_DA == 'PA'):
            AnalyticsMoz.append(PA[value])
            
        elif(int(valuesToCheck[value]) > LimitOfLinks):
            AnalyticsMoz.append(PA[value])

        else:
            AnalyticsMoz.append(DA[value])
       
    content_even = []
    content_odd = []
    targeturl = []
    dofollowlinks = []
    InboundLinks = []
    keywordslist = []
    for l in AnalyticsMoz[:int(NumberResults)]:
        driver.get(l)
        time.sleep(3)
        temp = driver.find_element_by_name("forms.links.search.search")
        currentinboundlink = temp.get_attribute("value")
        stats = driver.find_elements_by_css_selector("div.metric-value > a")
        stats[1].click()
        time.sleep(2)
        
        NextMozButton = driver.find_elements_by_xpath("/html/body/main/div/div/div[1]/div/div[2]/div[5]/div[2]/div[4]/div[2]/div[2]/div[2]/button")

        for i in NextMozButton:
            NextMoz = i.text
        if(NextMoz[-1] == 'k'):
            NextMoz = NextMoz.replace('k', '')
            NextMoz = float(NextMoz) * 1000
            
        elif(NextMoz[-1] == 'm'):
            NextMoz = NextMoz.replace('m', '')
            NextMoz = float(NextMoz) * 1000000
        
        try:
            dofollow = driver.find_elements_by_css_selector("div.secondary-value")
            time.sleep(1)
            dofollow[1].click()
            time.sleep(5)
        except:
            pass
        
        countElements = 0
        while(int(countElements/8) < int(NextMoz)):
            elems = []
            elems = driver.find_elements_by_css_selector(".wide [href]")
            time.sleep(1)
            linksonpage = [elem.get_attribute('href') for elem in elems]
            dofollowlinks.extend(linksonpage)
            keywordslist.extend([SearchItem] * len(linksonpage))
            InboundLinks.extend([currentinboundlink] * len(linksonpage))
            datalisteven = driver.find_elements_by_class_name("even.content-row td")
            time.sleep(1)
            for data in datalisteven:
                content_even.append(data.text)
                countElements += 1

            datalistodd = driver.find_elements_by_class_name("odd.content-row td")
            time.sleep(1)
            for data in datalistodd:
                content_odd.append(data.text)
                countElements += 1

            buttonclicker = []
            buttonclicker = driver.find_elements_by_css_selector("td.expand-column")
            time.sleep(1)
            for buttons in buttonclicker:
                buttons.click()

            #need to get every alternate element
            target = []
            tlist = driver.find_elements_by_css_selector("a.external-link")
            time.sleep(1)
            for t in tlist:
                target.append(t.get_attribute('href'))

            targeturl.extend(target[1::2])
            time.sleep(2)
            try:
                Plsclicknext = driver.find_element_by_css_selector("span.moz-pagination-pager.moz-pagination-pager-right")
                time.sleep(1)
                Plsclicknext.click()
                time.sleep(5)
            except:
                break

    globaleven.append(content_even)
    globalodd.append(content_odd)
    globaltargeturl.append(targeturl)
    globaldofollowlinks.append(dofollowlinks)
    globalinboundlinks.append(InboundLinks)
    globalkeywords.append(keywordslist)

driver.quit()
print("The Scraping has finished, now it is Filtering")

# In[290]:


anchortext = []
for j in range(len(globaleven)):
    i = 2
    while(i<len(globaleven[j])):
        anchortext.append(globaleven[j][i])
        try:
            anchortext.append(globalodd[j][i])
        except:
            pass
        i += 8


# In[291]:


spamscore = []
for j in range(len(globaleven)):
    i = 6
    while(i < len(globaleven[j])):
        spamscore.append(globaleven[j][i])
        try:
            spamscore.append(globalodd[j][i])
        except:
            pass
        i += 8


# In[292]:


PA = []
for j in range(len(globaleven)):
    i = 3
    while(i < len(globaleven[j])):
        PA.append(globaleven[j][i])
        try:
            PA.append(globalodd[j][i])
        except:
            pass
        i += 8


# In[293]:


DA = []
for j in range(len(globaleven)):
    i = 4
    while(i < len(globaleven[j])):
        DA.append(globaleven[j][i])
        try:
            DA.append(globalodd[j][i])
        except:
            pass
        i += 8


# In[294]:


linkingdomains = []
for j in range(len(globaleven)):
    i = 5
    while (i < len(globaleven[j])):
        linkingdomains.append(globaleven[j][i])
        try:
            linkingdomains.append(globalodd[j][i])
        except:
            pass
        i += 8


# In[295]:


keywordlinks = []
for i in range(len(globalkeywords)):
    for j in range(len(globalkeywords[i])):
        keywordlinks.append(globalkeywords[i][j])
df = pd.DataFrame(keywordlinks, columns = ['KeyWord Searched For'])

inboundlinks = []
for i in range(len(globalinboundlinks)):
    for j in range(len(globalinboundlinks[i])):
        inboundlinks.append(globalinboundlinks[i][j])
df['Inbound Links'] = inboundlinks
DomainNames = []
dofollowlinks = []
for j in range(len(globaldofollowlinks)):
    for i in range(len(globaldofollowlinks[j])):
        dofollowlinks.append(globaldofollowlinks[j][i])
df['URL'] = dofollowlinks

for url in dofollowlinks:
    DomainNames.append(url.split("//")[-1].split("/")[0].split('?')[0])
df['Domain Names'] = DomainNames
df['Anchor text'] = anchortext
df['Spam Score'] = spamscore
df['PA'] = PA
df['DA'] = DA
df['Linking Domains'] = linkingdomains

targeturl = []
for j in range(len(globaltargeturl)):
    for i in range(len(globaltargeturl[j])):
        targeturl.append(globaltargeturl[j][i])
df['Target URL'] = targeturl

linktype = []
for i in range(len(dofollowlinks)):
    linktype.append("follow")
df['Link Type'] = linktype
linkstate = []
for i in range(len(dofollowlinks)):
    linkstate.append('active')
df['Link State'] = linkstate

df.to_csv('MozData.csv', index = False)
