from urllib.request import urlopen
from bs4 import BeautifulSoup

# testing one page first
keyword_list = []
html = urlopen('http://www.oed.com/search?browseType=sortAlpha&dateFilter=1900+-+1999&page=1&pageSize=100&scope=SENSE&sort=entry&subjectClass=Technology&timeline=false&type=dictionarysearch&print')
soup = BeautifulSoup(html, 'html.parser')
#print(soup.prettify())
allWords = soup.find_all('span', 'word')
for word in allWords:
	w_soup = BeautifulSoup(str(word), 'html.parser')
	if ("n." in w_soup.get_text()):
		print(w_soup.get_text())
	#if (lemma):
		#l_soup = BeautifulSoup(str(lemma[0]), 'html.parser')
		#print(l_soup.span.string)


