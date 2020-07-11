from collections import Counter
from string import punctuation
from bs4 import BeautifulSoup
import pandas as pd
import requests
import ctypes

def quickedit(enabled=1): # This is a patch to the system that sometimes hangs
        kernel32 = ctypes.windll.kernel32
        if enabled:
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
        else:
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100))

quickedit(0)

def someotherfunction(s):
    return ', '.join(set() | set(s))

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\n"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

print("The process is executing")

df = pd.read_csv(r"FinalDataAfterFiltering.csv")
df = df.astype(str)

count = 0
ratios = []
NumberWords = []
NumberLinks = []

for blogs in df['URL']:
    try:
        r = requests.get(blogs)
        soup = BeautifulSoup(r.content, 'html.parser')
        # Words within paragrphs
        text_p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))
        c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

        # Words within divs
        text_div = (''.join(s.findAll(text=True))for s in soup.findAll('div'))
        c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))

        total = c_div + c_p
        dict(total)
        NumberOfWords = sum(total.values())
        NumberWords.append(NumberOfWords)
        NumberOfLinks = 0

        for link in soup.find_all('a'):
            #print(link.get('href'))
            NumberOfLinks += 1
        NumberLinks.append(NumberOfLinks)
        count += 1
        printProgressBar(count, len(df))
        try:
            ratios.append(NumberOfWords/NumberOfLinks)
        except:
            ratios.append('0')

    except:
        count += 1
        printProgressBar(count, len(df))
        NumberWords.append('0')
        NumberLinks.append('0')
        ratios.append('0')

    


# In[350]:


df['Number of Words on webpage'] = NumberWords
df['Number of external links'] = NumberLinks
df['Ratio of words to links'] = ratios

df['Number of Words on webpage'] = df['Number of Words on webpage'].astype(str)
df['Number of external links'] = df['Number of external links'].astype(str)
df['Ratio of words to links'] = df['Ratio of words to links'].astype(str)


RatiosWordstoLinks = df.groupby(['URL'], as_index = False).agg(lambda col: someotherfunction(col))

print("The websites have been scraped for number of words and links")
RatiosWordstoLinks.to_csv('RatiosWordstoLinks.csv', index = False, columns = ['KeyWord Searched For', 'Inbound Links', 'URL', 'Domain Names', 'Anchor text', 'Spam Score',
                                                                      'PA', 'DA', 'Linking Domains', 'Target URL', 'Link Type', 'Link State', 'Number of Words on webpage',
                                                                              'Number of external links', 'Ratio of words to links'])
