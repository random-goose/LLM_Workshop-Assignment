import replicate
import os
import json #because bbc formats their page to make webscraping as hard as possible
import requests
from bs4 import BeautifulSoup



os.environ["REPLICATE_API_TOKEN"] = "r8_ayuYJyHpCmCouLZvcQdXuUFk054XpDG0tZudL"



url = "https://www.bbc.com/travel/article/20240222-air-canada-chatbot-misinformation-what-travellers-should-know"

soup = BeautifulSoup(requests.get(url).content, "html.parser")
data = json.loads(soup.select_one("#__NEXT_DATA__").text)

page_text = ""

page = next(
    v for k, v in data["props"]["pageProps"]["page"].items() if k.startswith("@")
)
for c in page["contents"]:
    if c["type"] == "headline":
        page_text += c["model"]["blocks"][0]["model"]["text"] + "\n\n"
    elif c["type"] == "text":
        page_text += c["model"]["blocks"][0]["model"]["text"] + " "


output = replicate.run(
    "mistralai/mistral-7b-instruct-v0.1:5fe0a3d7ac2852264a25279d1dfb798acbc4d49711d126646594e212cb821749",
    input={
        "prompt": f"Go through this article \" {page_text} \" and summarise it, give me information about all the key entities being talked about, and identify the general sentiment about the entities give me the answer in three distinct sections" ,
        "temperature" : 0.3,   #the lowest it will go
        "max_new_tokens": 1000,
        
    }
)


for item in output:
    if (item == "."):
        print()
    else:
        print(item, end="")




# output
        

# Section 1: Key Entities

# * Air Canada
# * Jake Moffatt
# * British Columbia Civil Resolution Tribunal
# * Gabor Lukacs
# * Air Passenger Rights
# * WestJet
# * Expedia
# * Civil Aviation Authority

# Section 2: Summary of Key Points

# * Air Canada's chatbot gave incorrect information to Jake Moffatt, who was promised a discount that wasn't available.
# * The British Columbia Civil Resolution Tribunal ruled that Air Canada was responsible for the chatbot's actions and had to pay Jake Moffatt $812.02 in damages and tribunal fees.
# * The decision sets a precedent that airlines cannot hide behind chatbots.
# * The case is being considered a landmark one that potentially sets a precedent for airline and travel companies that are increasingly relying on AI and chatbots for customer interactions.

# Section 3: General Sentiment

# * The general sentiment about Air Canada is negative due to the incorrect information given by its chatbot and the ruling that it is responsible for the chatbot's actions.
# * The general sentiment about Jake Moffatt is positive as he was wronged by Air Canada's chatbot and received compensation.
# * The general sentiment about the British Columbia Civil Resolution Tribunal is positive as it ruled in favor of Jake Moffatt and held Air Canada responsible for the chatbot's actions.
# * The general sentiment about Gabor Lukacs and Air Passenger Rights is positive as they are advocating for passengers' rights and holding airlines accountable for the actions of their chatbots.
# * The general sentiment about WestJet and Expedia is neutral as they are also using AI and chatbots for customer interactions but are not specifically mentioned in the article.
# * The general sentiment about the Civil Aviation Authority is neutral as it is not specifically mentioned in the article.