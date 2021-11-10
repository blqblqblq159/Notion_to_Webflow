import requests
import json
import pandas as pd

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

def get_page_ids(database_id, headers) -> list:
    page_ids = []
    URL = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.request("POST", URL, headers=headers)
    content = json.loads(res.content)
    for page in content["results"]:
        condition = True #create custom condition for page to be included in process
        if(condition):
            page_ids.append(page["id"])
    return page_ids

def get_page_content(page_id, headers) -> dict:
    URL = f"https://api.notion.com/v1/blocks/{page_id}/children"
    res = requests.request("GET", URL, headers=headers2)
    return json.loads(res.content)

def parse_page_content(content) -> pd.DataFrame():
    column_names = ["block_num", "type", "text", "link", "annotations", "color"]
    df = pd.DataFrame(columns = column_names)
    for block_num, block in enumerate(content["results"]):
        type = block["type"]
        text_contents = block[type]["text"]
        for piece in text_contents:
            text = piece["text"]["content"]

            if piece["text"]["link"] == None:
                link = None
            else:
                link = piece["text"]["link"]["url"]

            annotations = []
            possible_annotations = ["bold", "italic", "strikethrough", "underline", "code"]
            for x in possible_annotations:
                if piece["annotations"][x] == True:
                    annotations.append(x)
            if annotations == []:
                annotations = None
            
            color = piece["annotations"]["color"]

            row = {"block_num": block_num, "type": type, "text": text, "link": link, "annotations": annotations, "color": color}
            df = df.append(row, ignore_index = True)
    return df
            
if __name__ == "__main__":
    page_ids = get_page_ids(database_id, headers1)
    for page_id in page_ids:
        page_contents = get_page_content(page_id, headers2)
        df = parse_page_content(page_contents)
        print(df)