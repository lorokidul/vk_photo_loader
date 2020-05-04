import requests, re

API_VERSION = '5.103'
USER_ID = 'some user id'
token = 'some token'
album_id = 'wall'


def download_photo(album_id, tag):
    response = requests.get('https://api.vk.com/method/photos.get',
                                params={'owner_id': USER_ID,
                                        'album_id': album_id,
                                        'rev': '1',
                                        'count': '999',
                                        'access_token': token,
                                        'photo_sizes': '1',
                                        'v': API_VERSION})
    parsed = response.json()
    print(parsed)
    if 'error' in parsed.keys():
        print(parsed['error']['error_msg'])
    else:
        c = 0
        photos = []



        for item in parsed['response']['items']:
            max_width = 0
            prev_height = 0
            photo_url = ""
            for photo in item["sizes"]:
                if (photo["width"] >= max_width):
                    photo_url = photo["url"]
                    max_width = photo["width"]

            # print(photo_url)
            if (photo_url != ""):
                photos.append(photo_url)
                c = c + 1
        print(tag + "|" + str(c) + " photos")

        count = 0
        for photo_url in photos:

            image_url = photo_url
            r = requests.get(image_url)  # create HTTP response object
            pattern_matched = re.findall('[A-Za-z0-9]+.jpg', image_url)
            if (len(pattern_matched) > 0):
                filename = tag + "_" + str(count) + "_" + pattern_matched[0]
            else:
                print(image_url)

            with open(filename, 'wb') as f:
                f.write(r.content)
            count = count + 1;


    count = 0;

download_photo("wall", "some_tag")
