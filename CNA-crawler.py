import requests
from bs4 import BeautifulSoup
import time
import re
import sys

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
url = "https://www.cna.com.tw/news/aipl/"#202107150041.aspx"
batchSize = 400

def dateGenerator(date):#20210715
	day = int(date[6:])+1
	month = int(date[4:6])
	year = int(date[0:4])
	#print(month in [1, 3, 5, 7, 8, 10, 12])
	if (day > 28 and month == 2) or (day > 30 and month in [4, 6, 9, 11]) or (day > 31 and month in [1, 3, 5, 7, 8, 10, 12]) :
		day = 1
		month += 1
		if month == 13:
			month = 1
			year += 1
	
	#print(f'{year:04d}{month:02d}{day:02d}')
	return f'{year:04d}{month:02d}{day:02d}'

#dateGenerator('20210715')


def parmgenerator(parm):#202107150041.aspx
	index = int(parm[8:12])+1
	return f'{parm[0:8]}{index:04d}.aspx'


def crawling(newsUrl):
	try:
		response = requests.request("GET", newsUrl, headers=HEADERS)
		raw_text = response.text.encode('utf8')
		#print(raw_text)

		soup = BeautifulSoup(raw_text, 'html.parser')
		#f = open("test.txt", "w+")
		#f.write(soup.prettify())
		#f.close()

		title = soup.find("h1")
		#print(title.string)
		tag = soup.find("div", class_ = "paragraph")


		articles = tag.find_all("p")
		summarization = re.sub(r'\W.+電\W||\W.+導\W','',articles[0].string)
		article = ""
		for i in articles:
			article += re.sub(r'\W.+電\W||\W編.+\d+||\W.+導\W||\W譯.+\d+','',i.string)

		#print(summarization)
		#print(article)
		#print(f'{{"summarization": "{summarization}", "article": "{article}", "title": "{title.string}"}}\n')
		return f'{{"summarization": "{summarization}", "article": "{article}", "title": "{title.string}"}}\n'
	except Exception as e:
		#sys.stderr.write(str(e)+"\n")
		return None

date = '20210101'
while date < '20210720':
	parm = date+'0001.aspx'
	batchText = ''
	for i in range(batchSize):
		parm = parmgenerator(parm)
		newsUrl = url + parm
		#print(newsUrl)
		text = crawling(newsUrl)
		if text != None:
			batchText += text
	
	with open('./CNA_News/'+date+'.txt', 'a+') as fp:
		fp.write(batchText)
	date = dateGenerator(date)
"""


response = requests.request("GET", url, headers=HEADERS)
raw_text = response.text.encode('utf8')
#print(raw_text)

soup = BeautifulSoup(raw_text, 'html.parser')
#f = open("test.txt", "w+")
#f.write(soup.prettify())
#f.close()

title = soup.find("h1")
print(title.string)
tag = soup.find("div", class_ = "paragraph")


articles = tag.find_all("p")
summarization = re.sub(r'\W.+電\W','',articles[0].string)
article = ""
for i in articles:
	article += re.sub(r'\W.+電\W||\W編.+\d+','',i.string)

print(summarization)
print(article)
"""
"""



options = Options()
options.add_argument("--disable-notifications")
chrome = webdriver.Chrome('/mnt/c/Users/小傑/Desktop/chromedriver_win32/chromedriver.exe', chrome_options=options)


links = []
url = "https://www.worldgymtaiwan.com/locations"
chrome.maximize_window()
chrome.get(url)
time.sleep(3)
for i in range(1, 17):
	chrome.find_element_by_xpath(f"/html/body/div/main/div/div[2]/div[2]/div[1]/div[2]/ul/li[{i}]").click()
	time.sleep(2)
	soup = BeautifulSoup(chrome.page_source, "html.parser")
	
	results = soup.find_all("i", class_ = "icon-location")

	for result in results:
		next_node = result.find_next_siblings("a")
		link = next_node[0].get("href")
		links.append(link)

	time.sleep(1)

print(links)
chrome.quit()

with open('links.txt', "w") as fp:
	for i in links:
		fp.writelines(i+"\n")


links = []
with open('links.txt', 'r') as fp:
	lines = fp.readlines()
	for line in lines:
		links.append(line.split("\n")[0])



def revertShortLink(url):
	resp = requests.head(url, allow_redirects=True, headers = constants.HEADERS)
	return resp.url

cid = []
for link in links:
	link = revertShortLink(link)
	#print(link)
	try:#print(re.search(r":0x\w*", link).group())
		cid.append(int(re.search(r":0x\w*", link).group()[1:], 16))
	except Exception as e:
		sys.stderr.write(str(e)+"\n")

print(cid)
print(len(cid))
with open('word_gym_cid.txt', 'w') as fp:
	for i in cid:
		fp.write(str(i)+"\n")


for i in links:
	print(i)	
	print(revertShortLink(i))




res = requests.request("GET", url, headers = constants.HEADERS)
#print(res.text)
soup = BeautifulSoup(res.text, "html.parser")
#print(soup.prettify())
#print(soup.find_all("i", class_ = "icon-location"))
results = soup.find_all("i", class_ = "icon-location")
links = []
for result in results:
	next_node = result.find_next_siblings("a")
	link = next_node[0].get("href")
	links.append(link)

"""
