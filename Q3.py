import ollama
import json #again, because bbc formats their page to make webscraping as hard as possible
import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.com/travel/article/20240222-air-canada-chatbot-misinformation-what-travellers-should-know"

soup = BeautifulSoup(requests.get(url).content, "html.parser")
data = json.loads(soup.select_one("#__NEXT_DATA__").text)

page_text = ""

page = next(
    v for k, v in data["props"]["pageProps"]["page"].items() if k.startswith("@")
)
for c in page["contents"]:
    if c["type"] == "text":
        page_text += c["model"]["blocks"][0]["model"]["text"] + " "


response = ollama.chat(model='llama2', messages=[
  {
    'role': 'user',
    'content': f"Go through this article \" {page_text} \" and summarise it, give me information about all the key entities being talked about, and identify the general sentiment about the entities give me the answer in three distinct sections" ,
    
  },
])
print(response['message']['content'])


# Output:
# Section 1: Key Entities Talked About in the Article

# * Air Canada: A Canadian airline that uses a chatbot to provide information and assistance to passengers.
# * Jake Moffatt: A passenger who used Air Canada's chatbot to request a bereavement fare for his grandmother's funeral, but was denied the discount.
# * British Columbia Civil Resolution Tribunal: A tribunal that ruled in favor of Moffatt and awarded him $812.02 in damages and tribunal fees.
# * Chatbot: A computer program that uses artificial intelligence to simulate human conversation, used by Air Canada and other companies to provide customer service.        
# * WestJet: Another Canadian airline that has also implemented a chatbot for customer service.
# * Expedia: A travel company that has launched a ChatGPT plug-in to help with trip planning.

# Section 2: Sentiment About the Entities

# * Air Canada: The airline is seen as responsible for the actions of its chatbot, as it is a separate legal entity that is responsible for its own actions. The tribunal rejected Air Canada's argument that Moffatt should have gone to a link provided by the chatbot to see the correct policy.
# * Jake Moffatt: Moffatt is seen as a victim of Air Canada's chatbot, as he was denied the bereavement fare he requested despite the chatbot promising it to him.
# * British Columbia Civil Resolution Tribunal: The tribunal is seen as fair and impartial in its decision, as it ruled in favor of Moffatt and held Air Canada responsible for the mistakes made by its chatbot.
# * Chatbot: The chatbot is seen as a technology that can make mistakes, as it is powered by artificial intelligence and may not always provide accurate information.        
# * WestJet: WestJet is not directly involved in the case, but their use of a chatbot for customer service highlights the growing trend of airlines relying on AI technology.
# * Expedia: Expedia's use of ChatGPT plug-in suggests that they are also embracing AI technology for trip planning, which may increase the reliance on AI in the travel industry.

# Section 3: General Sentiment About the Article

# * The article highlights the growing trend of airlines relying on AI technology, particularly chatbots, to provide customer service.
# * The case involving Air Canada and Jake Moffatt is seen as a landmark ruling that establishes a common sense principle: if companies hand over part of their business to AI, they are responsible for what the AI does.
# * The article also notes that while AI technology has advanced rapidly, regulatory frameworks have yet to catch up, leaving passengers vulnerable to mistakes made by chatbots.
# * The article concludes by suggesting that passengers may want to consider using old-fashioned human help when trip-planning or navigating fares, and that globally uniform protections for airline passengers are needed to ensure fairness and accountability.