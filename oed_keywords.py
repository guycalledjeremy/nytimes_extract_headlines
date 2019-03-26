from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

keyword_dict = {}

for i in range(1, 96):
	url = 'http://www.oed.com/search?browseType=sortAlpha&dateFilter=1900+-+1999&page=' + str(i)+ '&pageSize=100&scope=SENSE&sort=entry&subjectClass=Technology&timeline=false&type=dictionarysearch&print'
	html = urlopen(url)
	soup = BeautifulSoup(html, 'html.parser')

	allYears = soup.find_all('span', 'year')
	wordYears = allYears[:100]
	allWords = soup.find_all('span', 'word')
	for i, word in enumerate(allWords):
		w_soup = BeautifulSoup(str(word), 'html.parser')
		w = w_soup.get_text()
		if ("n." in w):
			keyword = w.split(", ")[0].split(" in ")[0].strip()
			keyword = keyword.replace("\u02cc", "")
			keyword = keyword.replace("\u02c8", "")
			keyword = keyword.replace("–", "-") # not working for year keywords, ex. 1956-7
			keyword = keyword.replace("\u2020\u00a0", "")
			keyword = keyword.replace("\u00f6", "o")
			keyword = keyword.replace("\u00e8", "e")
			keyword = keyword.replace("\u00e9", "e")
			if keyword in keyword_dict:
				keyword_dict[keyword].append(allYears[i].get_text().strip())
			else:
				keyword_dict[keyword] = [allYears[i].get_text().strip()]
output_file = open("oed_keywords.json","w+")
output_file.write(json.dumps(keyword_dict))
output_file.close()
print("Output file with OED keywords created.")