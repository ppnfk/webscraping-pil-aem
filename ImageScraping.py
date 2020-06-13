import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from PIL import Image


def download_article_images(article):
    """ by given a article link of medium.com, we try to download the topic image """
    r = requests.get(article["link"])
    s = BeautifulSoup(r.text, 'html.parser')
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    # setting filename and image URL
    try:
        image_url = s.article.findAll('img')[3].get('src', None)
        path = urllib.parse.urlparse(image_url).path
        ext = os.path.splitext(path)[1]
        filename = 'original/' + article["img_filename"] + ext
        # print(filename)
        urllib.request.urlretrieve(image_url, filename)
    except IndexError as ie:
        pass
    finally:
        pass


def reduce_all_image_size():
    srcFolder = 'original/'
    dstFolder = 'reduced/'

    for filename in os.listdir(srcFolder):
        src_filename = f'{srcFolder}{filename}'
        clean_name = os.path.splitext(filename)[0]
        dst_filename = f'{dstFolder}{filename}'
        try:
            img = Image.open(src_filename)
            img.save(dst_filename, quality=50)
        except Exception as e:
            print(dst_filename)
            img.save(f'{dstFolder}{filename}')
        finally:
            pass