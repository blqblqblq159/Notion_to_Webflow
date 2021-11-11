import requests
import json
import pandas as pd

#Notion
secret_key = "secret_cpn7S1LfX2zIaeW3faN9JYdUSfOrR5txXifbLcLY08b"
database_id = "8ff8bb638a2b47df8a9eaa0b662588d1"

headers1 = {
    "Authorization": f"Bearer {secret_key}",
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json"
}

headers2 = {
    "Authorization": f"Bearer {secret_key}",
    "Notion-Version": "2021-08-16"
}

#Webflow
API_key = "5a373be964aa6f0336e7daf76484fb1749d194c34b803d199bf21ccefb049381"
site_id = "618bc51a1ffb6da00af1d0b9"
collection_id = "618bc51a1ffb6defebf1d0dd"
headers = {
    "Authorization": f"Bearer {API_key}",
    "accept-version": "1.0.0"
}
ignore = {"_archived", "_draft", "created-on", "updated-on", "published-on", "created-by", "updated-by", "published-by"}

def get_page_id_titles(database_id, headers) -> dict:
    page_id_titles = {}
    URL = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.request("POST", URL, headers=headers)
    content = json.loads(res.content)
    for page in content["results"]:
        condition = True #create custom condition for page to be included in process
        if(condition):
            page_id_titles[page["id"]] = page["properties"]["Name"]["title"][0]["text"]["content"]
    return page_id_titles

def get_page_content(page_id, headers) -> dict:
    URL = f"https://api.notion.com/v1/blocks/{page_id}/children"
    res = requests.request("GET", URL, headers=headers2)
    return json.loads(res.content)

def parse_page_content(content) -> list:
    page_content_full = []
    for block in content["results"]:
        type = block["type"]
        page_content = {}
        page_content[type]=[]
        if "text" in block[type].keys(): #ignore figures
            for piece in block[type]["text"]:
                text = piece["text"]["content"]

                if piece["text"]["link"] == None:
                    link = None
                else:
                    link = piece["text"]["link"]["url"]

                annotations = []
                possible_annotations = ["bold", "italic", "strikethrough", "underline", "code"]
                for x in possible_annotations:
                    if piece["annotations"][x]:
                        annotations.append(x)
                
                color = piece["annotations"]["color"]

                row = {"text": text, "link": link, "annotations": annotations, "color": color}
                page_content[type].append(row.copy())
            page_content_full.append(page_content.copy())
    return page_content_full

def get_blogpost_schema(API_key, collection_id, headers, ignore) -> set:
    URL = f"https://api.webflow.com/collections/{collection_id}"
    res = requests.request("GET", URL, headers=headers)
    fields = json.loads(res.content)["fields"]
    schema = set()
    for field in fields:
        schema.add(field["slug"])
    return schema - ignore

def get_webflow_title_ids(collection_id, headers) -> dict:
    URL = f"https://api.webflow.com/collections/{collection_id}/items"
    res = requests.request("GET", URL, headers=headers)
    items = json.loads(res.content)["items"]
    webflow_title_ids = {}
    for item in items:
        webflow_title_ids[item["name"]] = item["_id"]
    return webflow_title_ids

def create_webflow_blog_content(page_content) -> str:
    blog_content = ""
    typedict = {"heading_1": "h1", "heading_2": "h2", "heading_3": "h3", "paragraph": "p", "code": "p", "bulleted_list_item": "p", "quote": "blockquote"}
    annotationdict = {"bold": "strong", "italic": "em"}
    for item in page_content:
        type = list(item.keys())[0]
        info = item[type]
        blog_content_piece = ""
        for piece in info:
            blog_content_part = piece["text"]
            if piece["link"] != None:
                link = piece["link"]
                if "http://"==link[0:6]:
                    link = link[7:]
                blog_content_part = f'<a href={link}>{blog_content_part}</a>'
            for annotation in piece["annotations"]:
                if annotation in annotationdict.keys():
                    webflow_annotation = annotationdict[annotation]
                    blog_content_part = f"<{webflow_annotation}>{blog_content_part}</{webflow_annotation}>"
            blog_content_piece += blog_content_part
        webflow_type = typedict[type]
        blog_content += f"<{webflow_type}>{blog_content_piece}</{webflow_type}>"
    return blog_content
    
if __name__ == "__main__":
    page_id_titles = get_page_id_titles(database_id, headers1)
    webflow_title_ids = get_webflow_title_ids(collection_id, headers)
    for page_id, page_title in page_id_titles.items():
        page_contents = get_page_content(page_id, headers2)
        with open("page_contents.json", "w") as f:
            f.truncate(0)
            json.dump(page_contents, f, indent=4)
        page_content = parse_page_content(page_contents)
        with open("page_sontent.json", "w") as f:
            f.truncate(0)
            json.dump(page_content, f, indent=4)
        webflow_blog_content = create_webflow_blog_content(page_content)
        message = {
            "fields": {
            "name": page_title,
            "slug": page_title.replace(" ","-"),
            "_archived": False,
            "_draft": False,
            "blog-content": webflow_blog_content,
            "blog-post-summary": "",
            "main-image": "580e63fe8c9a982ac9b8b749"
            }
        }
        if page_title in webflow_title_ids.keys():
            item_id = webflow_title_ids[page_title]
            URL = f"https://api.webflow.com/collections/{collection_id}/items/{item_id}"
            res = requests.request("PUT", URL, headers=headers, json=message)
        else:
            URL = f"https://api.webflow.com/collections/{collection_id}/items"
            res = requests.request("POST", URL, headers=headers, json=message)
