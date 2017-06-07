#! C:\Python34\python.exe
# Open all Google search results on first page.

import requests, sys, bs4, webbrowser

print("Googling...")	# Displays texts while downloading the Google page
res = requests.get("https://google.com/search?q=" + ' '.join(sys.argv[1:] ))
res.raise_for_status()

# Retrieve top search results links.
soup = bs4.BeautifulSoup(res.text, 'html.parser')
linkElems = soup.select('.r a')

# Open a browser tab for each result.
for tab in range(len(linkElems)):
	webbrowser.open("https://google.com" +linkElems[tab].get('href'))