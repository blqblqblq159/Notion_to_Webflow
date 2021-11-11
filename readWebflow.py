import requests
import json
import pandas as pd

API_key = "5a373be964aa6f0336e7daf76484fb1749d194c34b803d199bf21ccefb049381"
site_id = "618bc51a1ffb6da00af1d0b9"
collection_id = "618bc51a1ffb6defebf1d0dd"

headers = {
    "Authorization": f"Bearer {API_key}",
    "accept-version": "1.0.0"
}

message = {
    "fields": {
        "name": "Exciting blog post title",
        "slug": "exciting-post",
        "_archived": False,
        "_draft": False,
        "blog-content": "<h1>Blog post contents...</h1><p>a paragraph</p><p>another paragraph</p>",
        "blog-post-summary": "Summary of exciting blog post",
        "main-image": "580e63fe8c9a982ac9b8b749"
    }
}

URL = f"https://api.webflow.com/collections/{collection_id}/items"

res = requests.request("GET", URL, headers=headers)

# try:
#     with open("blogposts_id.json", "r") as f:
#         blogposts_id = json.load(f)
# except:
#     blogposts_id = {}

# blogposts_id[message["fields"]["name"]] = json.loads(res.content)["_id"]

# with open("blogposts_id.json", "w") as f:
#     json.dump(blogposts_id, f, indent=2)


print(res.status_code)

with open("response.json", "w") as f:
    f.truncate(0)
    json.dump(json.loads(res.content), f, indent=2)