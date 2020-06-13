import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import os
import json
import time, datetime

# template json for creating articles on AEM by RESTApi
aeq_json_template = {
    "properties": {
        "cq:model": "/conf/wknd/settings/dam/cfm/models/article1",
        "contentFragment": True,
        "title": "Add Content Fragment",
        "elementsOrder": [
            "articleId",
            "title",
            "description",
            "articleBody",
            "category",
            "language",
            "author",
            "publishedDate",
            "image",
            "video"
        ],
        "metadata": {
            "cq:tags": ["auto_gen_news"]
        },
        "elements": {
            "image": {
                ":type": "string",
            },
            "articleBody": {
                ":type": "text/html",
            },
            "author": {
                ":type": "string",
            },
            "articleId": {
                ":type": "double",
            },
            "description": {
                ":type": "text/html",
            },
            "language": {
                ":type": "string",
                "value": "english"
            },
            "publishedDate": {
                ":type": "calendar",
            },
            "video": {
                ":type": "string",
                "value": ""
            },
            "title": {
                ":type": "string",
            },
            "category": {
                ":type": "string",
                "value": "blog"
            }
        }
    }
}


def get_articles(article_divs):
    """given a list of article div, return a dict of articles with information we want"""
    articles_dictionary = []
    id_offset = 6
    for idx, item in enumerate(article_divs):
        article = {}
        href = article_divs[idx].a.get('href', None)
        title = article_divs[idx].a.getText()
        article["articleId"] = idx + id_offset
        article["link"] = href
        article["title"] = title
        # use title adding - as the image_filename which we will use to save image later.
        article["img_filename"] = re.sub('[^a-zA-Z0-9]', '-', title).lower().strip("-")
        articles_dictionary.append(article)
    return articles_dictionary


def get_img_filename_extension(article):
    """given a article, get the image extension by its link """
    try:
        r = requests.get(article["link"])
        s = BeautifulSoup(r.text, 'html.parser')
        image_url = s.article.findAll('img')[3].get('src', None)
        path = urllib.parse.urlparse(image_url).path
        ext = os.path.splitext(path)[1]
        article["img_filename"] += ext
        if os.path.splitext(article["img_filename"])[1] == "":
            article["img_filename"] += ".jpeg"
    except Exception as e:
        article["img_filename"] = ""
    finally:
        pass


def create_aem_article(article):
    url = 'http://10.1.2.250:4502/api/assets/wknd/en/articles/article'
    r = requests.get(article["link"])
    s = BeautifulSoup(r.text, 'html.parser')
    try:
        article["articleBody"] = str(s.article.select('.n.p')[2])
    except Exception as e:
        article["articleBody"] = str(s.article.select('.n.p')[0])
    finally:
        aeq_json_template["properties"]["name"] = article["title"]
        aeq_json_template["properties"]["title"] = article["title"]
        aeq_json_template["properties"]["description"] = article["description"]
        if not article["img_filename"]:
            aeq_json_template["properties"]["elements"]["image"]["value"] = ""
        else:
            aeq_json_template["properties"]["elements"]["image"]["value"] = "/content/dam/wknd/en/articles-assets/" + \
                                                                            article["img_filename"]
        aeq_json_template["properties"]["elements"]["articleBody"]["value"] = article["articleBody"]
        aeq_json_template["properties"]["elements"]["author"]["value"] = article["author"]
        aeq_json_template["properties"]["elements"]["description"]["value"] = article["description"]
        aeq_json_template["properties"]["elements"]["articleId"]["value"] = article["articleId"]
        aeq_json_template["properties"]["elements"]["title"]["value"] = article["title"]
        aeq_json_template["properties"]["elements"]["publishedDate"]["value"] = article["publishDate"]

    # print(article["img_filename"])
    # print(json.dumps(aeq_json_template))
    newHeaders = {
        "User-Agent": "python-requests/2.11.1",
        'Content-type': 'application/json',
        'Accept': 'text/plain'}

    response = requests.post(url + str(article["articleId"]), data=json.dumps(aeq_json_template), headers=newHeaders,
                             auth=('******', '******'))
    print("Status code: ", response.status_code)


def get_authors(authors, articles):
    for idx, item in enumerate(authors):
        author = item.a.getText()
        articles[idx]["author"] = author


def trans_to_timestamp(dateyear):
    date_list = dateyear.split(',')
    date = date_list[0]
    if len(date_list) > 1:
        year = date_list[1]
    else:
        year = "2020"

    return int(time.mktime(datetime.datetime.strptime(f'{date} {year}', "%b %d %Y").timetuple()) * 1000)


def get_publish_date(publish_dates, articles):
    for idx, item in enumerate(publish_dates):
        infolist = item.getText().split('·')
        publish_date = infolist[0]
        description = infolist[1]

        articles[idx]["publishDate"] = trans_to_timestamp(publish_date)
        articles[idx]["description"] = description


if __name__ == '__main__':

    with open('popular_medium.htm', 'r') as file:
        data = file.read().replace('\n', '')

    soup = BeautifulSoup(data, 'html.parser')
    article_links = soup.select('.gg.gh')
    authors = soup.select('.r.hu')
    publish_dates = soup.select('.gz.n.dv')

    articles = get_articles(article_links)
    get_authors(authors, articles)
    get_publish_date(publish_dates, articles)

    for article in articles:
        get_img_filename_extension(article)
        create_aem_article(article)
