import requests
import json
import pandas as pd

API_key = "5a373be964aa6f0336e7daf76484fb1749d194c34b803d199bf21ccefb049381"
site_id = "618bc51a1ffb6da00af1d0b9"
collection_id = "618bc51a1ffb6defebf1d0dd"
item_id = "618e23298a6816eaa5181480"

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

message = {
    "fields": {
        "_archived": False,
        "_draft": False,
        "blog-post-summary": None,
        "name": "How traceability and graph databases help build our future",
        "blog-content": "<h1>Summary</h1><p>We first discuss the future relevance of traceability as predicted by Gartner and McKinsey. Then, we showcase part of the power and flexibility of graph database technology Neo4j within the context of food traceability.</p><h1>Background</h1><p>Traceability is the ability to trace all processes from procurement of raw materials to production, consumption and disposal to clarify \"when and where the product was produced by whom.\" This subject has been increasing in important in many sectors, such as </p><p>Automotive</p><p>Electronics</p><p>Pharmaceutical</p><p>Food</p><p><a href=https://www.gartner.com/en/documents/3981951/top-10-strategic-technology-trends-for-2020-transparency>Gartner</a> put traceability as one of the top 10 strategic technology trends for 2020. In their words:</p><blockquote><em>Enterprise architecture and technology innovation leaders must take responsibility for introducing technologies and best practices that increase transparency and traceability to manage a wide range of social, legal and commercial risks.</em></blockquote><p><a href=https://www.mckinsey.com/industries/agriculture/our-insights/agriculture-sector-preparing-for-disruption-in-the-food-value-chain>McKinsey</a> sees food traceability as one of the four trends that will greatly influence the direction of the agriculture sector in the coming years:</p><blockquote><em>We see a future in which digital platforms enable full transparency and traceability across the food value chain\u2014creating an environment in which actors in the value chain can more easily buy and sell to each other, compare prices, and review and rate suppliers.</em></blockquote><p><a href=https://www.mckinsey.com/business-functions/mckinsey-digital/our-insights/how-big-data-will-revolutionize-the-global-food-chain>McKinsey</a> also see traceability as an important factor in <strong>environmental foodprint management:</strong></p><blockquote><em>Environmental-footprint management\u00a0is another challenge that digitization can help to address. For instance, Cisco\u2019s Internet of Everything will provide consumers with the means to trace a food product back along its entire chain of production, from farmer\u2019s field to supermarket shelf. A scannable code on packaging will take users to a website that provides a detailed analysis of every stage and process undergone by that product\u2019s specific production batch.</em></blockquote><p>To facilitate this techno-agricultural revolution, it is important that we choose the correct technologies for the job to guarantee speed, scalability and robustness of our traceability pipeline. In the following we will showcase by example why graph databases, in particular Neo4j, are a strong technology for such traceability systems.</p><h1>Why use Neo4j?</h1><p>Neo4j is a graph database, you can think of it as a database that places its emphasis primarily on the <strong>relationships</strong> between the datapoints, rather than the datapoints themselves. In our context, we want to primarily know <strong>where</strong> our food product come from. This means we want to find all the processes to which our final product is <strong>related</strong>. A great fit for neo4j!</p><h1>Processing traceability data with Neo4j</h1><p>We've set up a fictitious data stream, containing production and distribution data of bread. The process starts out with the harvest of grain, this grain is then processed to flour, which gets baked to bread, this bread then gets distributed to vending machines, where purchases are made by customers. The figure below gives us the schema of this data, the processes in the schema are encircled. We start with a Grainbatch on the left and trace the production and consumption to purchases by customers on the right.</p><p>As we will see below, Neo4j enables us to easily query this kind of deeply nested data.</p><h3>Scenario</h3><p>Let's imagine the scenario where a hardworking farmer harvests a batch of grain, let's say Grainbacth 0. Unbenownst to him, some chemical company in the area has been dumping their waste products in the vicinity, contaminating the soil and the Grainbatch that he harvested. As such, all the bread that is produced from this Grainbatch is contaminated and we want to find all the customers that bought bread originating from the Grainbatch to alert them and hopefully prevent them from consuming it.</p><p>In databases where the <strong>relations</strong> are not first class citizens, it would be quite cumbersome to make a query for this kind of scenario. We could easily make an error in the query, that would leave some customers completely out in the cold.</p><p>In Neo4j however, this query is a piece of cake. We can use the following one-liner to find all the necessary customers:</p><p>Query = \"MATCH (:Grainbatch {id:0})-[*]->(a:Customer) RETURN DISTINCT a.id as CustomerID\"</p><p><strong>An important feature is that the above query stays consistent if the schema for our data ends up changing:</strong></p><p>If for some bread types we end up using flour that is first refined in some flour refinery process, we would get a schema for our data as in the figure below.</p><p>With other database solutions, we would have to adapt our query for all the different paths to find the customers. It's extremely easy to make a mistake here by forgetting some niche path(s) in the query. In Neo4j, the original query keeps functioning without fault. It is very robust in this context.</p><h1>Other advantages of Neo4j</h1><h3>Speed</h3><p>Since <strong>relations</strong> are first class citizens in Neo4j, querying over long paths like this is extremely time efficient compared to other database solutions. <a href=https://neo4j.com/news/how-much-faster-is-a-graph-database-really/>Link</a></p><h3>Scalability</h3><p>A database would not be worth much without the potential of large scalability. Luckily, a lot of work has been put in making Neo4j extremely scalable, with proof of concept graphs of more than a trillion relationships. <a href=https://neo4j.com/developer-blog/behind-the-scenes-worlds-biggest-graph-database/>Link</a></p><h3>New insights</h3><p>Neo4j's graph model brings a unique way of viewing data. Its integrated graph data science library allows us to uncover patterns in data that would previously be invisible. <a href=https://neo4j.com/product/graph-data-science/>Link</a></p><p>Within the context of traceability, these insights could be used to get a better onderstanding of the entire supply-chain. Allowing us to quickly predict and mitigate potential bottlenecks, optimize route planning and more. <a href=https://neo4j.com/blog/top-10-use-cases-supply-chain-management/>Link</a></p><h1>Conclusion</h1><p>In this short post, we discussed traceability as a solution for the increased desire for transparancy from consumers and as one of the main drivers for the next agricultural era.</p><p>We found that graph databases are an excellent technological option in this context with high robustness, speed and ease of use. This reduces potential mistakes by data engineers and facilitates strong analytics and transparancy over the entire supply chain.</p><h1>Final words</h1><p>If you would like to see the entire food traceability demo, enter your e-mail below and we will send you a link asap. </p><p>In the full demo, a kafka stream is set up in docker to populate Neo4j and mySQL instances with traceability data. In a jupyter notebook, we then make an ease-of-use comparison between both databases.</p><p>If you have any questions, remarks or suggestions, I'd be delighted to hear from you at: wannes.debreuck@humain.ai</p><p></p>",
        "slug": "How-traceability-and-graph-databases-help-build-our-future"
    }
}

# URL = f"https://api.webflow.com/collections/{collection_id}/items/{item_id}"

# res = requests.request("PUT", URL, headers=headers, json=message)

URL = f"https://api.webflow.com/collections/{collection_id}/items/{item_id}"
res = requests.request("GET", URL, headers=headers)
print(res.status_code)
with open("response.json", "w") as f:
    f.truncate(0)
    json.dump(json.loads(res.content), f, indent=2)

# try:
#     with open("blogposts_id.json", "r") as f:
#         blogposts_id = json.load(f)
# except:
#     blogposts_id = {}

# blogposts_id[message["fields"]["name"]] = json.loads(res.content)["_id"]

# with open("blogposts_id.json", "w") as f:
#     json.dump(blogposts_id, f, indent=2)


