import urllib.request, urllib.parse, urllib.error
import json
import ssl
from urllib.request import urlretrieve
import vk, os, time, math
import requests,re
def download_photo(album_url,tag):

	connection=urllib.request.urlopen(album_url)
	data = connection.read().decode()
	print('Retrieved', len(data), 'characters')
	try:
	    js = json.load(data)
	except:
	    js = None

	if not js or 'status' not in js or js['status'] != 'OK':
	    print('==== Failure To Retrieve ====')


	parsed =eval(data)

	c=0
	photos=[]
	for item in parsed['response']['items']:
		max_width =0
		prev_height=0
		photo_url=""
		for photo in item["sizes"]:
			if(photo["width"]>=max_width ):
				photo_url=photo["url"]
				max_width = photo["width"]

		# print(photo_url)
		if(photo_url!=""):
			photos.append(photo_url)
			c=c+1
	print(tag+"|"+str(c)+" photos")
	print(tag+"|"+str(len(photos))+" photos")

	# print(photos)
	count =0;
	for photo_url in photos:

		image_url = re.sub('//////','//',re.sub('\\\/', '///', photo_url))
		r = requests.get(image_url) # create HTTP response object 
		# print(image_url)
		pattern_matched = re.findall('[A-Za-z0-9]+.jpg',image_url)
		if(len(pattern_matched)>0):
			filename=tag+"_"+str(count)+"_"+pattern_matched[0]
		else:
			print(image_url)
		# send a HTTP request to the server and save 
		# the HTTP response in a response object called r 
		with open(filename,'wb') as f: 
			 f.write(r.content)
		count = count +1 

count = 0;


def get_url(owner_id,album_id,chronological,maxN,access_token):
	base='https://api.vk.com/method/photos.get?'
	owner_string = 'owner_id='+owner_id
	album_string= '&album_id='+album_id
	rev_string = '&rev='+chronological
	count_string='&count='+maxN
	access_token_string ='&access_token='+access_token
	photo_sizes_string="&photo_sizes=1"
	extended_string = "&extended=1"
	version_string="&v=5.103"
	url=base+owner_string+album_string+rev_string+count_string+photo_sizes_string+access_token_string+version_string
	return url

download_photo(url,"some_tag")