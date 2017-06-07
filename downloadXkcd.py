#! C:\Python34\python.exe

import requests, bs4, os

url = "http://xkcd.com"					# starting url
os.makedirs("xkcd", exist_ok = True)	# store comics in ./xkcd
while not url.endswith('#'):
	# Download the page
	print ("Downloading page %s..." %url)
	res = requests.get(url)
	res.raise_for_status()
	
	soup = bs4.BeautifulSoup(res.text)
	
	# Find the URL of the comic image
	comicElem = soup.select('#comic img')
	
	# A few XKCD pages have special content that isn’t a simple
	# image file. That’s fine; you’ll just skip those. If your
	# selector doesn’t find any elements, then soup.select
	# ('#comic img') will return a blank list. When that happens,
	# the program can just print an error message and move on
	# without downloading the image.
	# Example, https://xkcd.com/1663 doesn't have any image.
	# So, comicElem = []
	
	if comicElem == []:
		print("Could not find comic image at %s" %url)
	else:
		try:
			comicUrl = 'http:' + comicElem[0].get('src')
			
			# Download the image 
			print("Downloading the image %s" %comicUrl)
			res = requests.get(comicUrl)
			res.raise_for_status()
		except requests.exceptions.MissingSchema:	
		# requests.exceptions.MissingSchema means that the URL
		# schema (e.g. http or https) is missing.
		# skip downloading this comic 

			prevLink = soup.select("a[rel='prev']")[0]
			url = "http://xkcd.com" + prevLink.get('href')
			continue
			
	# Save the image in ./xkcd
	imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
	for chunk in res.iter_content(100000):
		imageFile.write(chunk)
	imageFile.close()
	
	# Get the Prev button's url
	prevLink = soup.select("a[rel='prev']")[0]
	url = "http://xkcd.com" + prevLink.get('href')

print("Done!")