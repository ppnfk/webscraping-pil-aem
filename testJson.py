import json

d = {
  "properties": {
    "cq:model": "/conf/wknd/settings/dam/cfm/models/article1",
    "title": "#{title}",
    "description": "#{description}",
    "metadata": {
      "cq:tags": ["auto_gen_news"]
    },
    "elements": {
      "image": {
        "variationsOrder": [],
        ":type": "string",
        "variations": {},
        "dataType": "string",
        "title": "Article Image",
        "multiValue": False,
        "value": "#{image}}"
      },
      "articleBody": {
        "variationsOrder": [],
        ":type": "text/html",
        "variations": {},
        "dataType": "string",
        "title": "Article Text Content",
        "multiValue": False,
        "value": "#{articleBody}}"
      },
      "author": {
        "variationsOrder": [],
        ":type": "string",
        "variations": {},
        "dataType": "string",
        "title": "Author",
        "multiValue": False,
        "value": "#{author}}"
      },
      "articleId": {
        "variationsOrder": [],
        ":type": "double",
        "variations": {},
        "dataType": "double",
        "title": "Article ID",
        "multiValue": False,
        "value": "#{articleId}"
      },
      "description": {
        "variationsOrder": [],
        ":type": "text/html",
        "variations": {},
        "dataType": "string",
        "title": "Article Description",
        "multiValue": False,
        "value": "<p>5 mins read</p>"
      },
      "language": {
        "variationsOrder": [],
        ":type": "string",
        "variations": {},
        "dataType": "string",
        "title": "Article Language",
        "multiValue": False,
        "value": "english"
      },
      "publishedDate": {
        "variationsOrder": [],
        ":type": "calendar",
        "variations": {},
        "dataType": "calendar",
        "title": "Article Publish Date",
        "multiValue": False,
        "value": "#{timestamp}"
      },
      "video": {
        "variationsOrder": [],
        ":type": "string",
        "variations": {},
        "dataType": "string",
        "title": "Article Video",
        "multiValue": False
      },
      "title": {
        "variationsOrder": [],
        ":type": "string",
        "variations": {},
        "dataType": "string",
        "title": "Article Title",
        "multiValue": False,
        "value": "{#title}"
      },
      "category": {
        "variationsOrder": [],
        ":type": "string",
        "variations": {},
        "dataType": "string",
        "title": "Article Category",
        "multiValue": False,
        "value": "blog"
      }
    }
  }
}

print(json.dumps(d, indent=4))
