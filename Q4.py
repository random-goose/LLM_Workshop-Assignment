import streamlit as st
import replicate
import os
import json
import requests
from bs4 import BeautifulSoup
import cohere


co = cohere.Client('k82ODlhoPoFpsJp5I53AmkkrjhL6bCfu1Rqwcgss')
os.environ["REPLICATE_API_TOKEN"] = "r8_ayuYJyHpCmCouLZvcQdXuUFk054XpDG0tZudL"

def scrape_article_text(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    data = json.loads(soup.select_one("#__NEXT_DATA__").text)
    page_text = ""
    page = next(
        v for k, v in data["props"]["pageProps"]["page"].items() if k.startswith("@")
    )
    for c in page["contents"]:
        if c["type"] == "text":
            page_text += c["model"]["blocks"][0]["model"]["text"] + " "
    return page_text

def summarize_article_m(page_text):
    output = replicate.run(
        "mistralai/mistral-7b-instruct-v0.1:5fe0a3d7ac2852264a25279d1dfb798acbc4d49711d126646594e212cb821749",
        input={
            "prompt": f"Go through this article \"{page_text}\" and summarize it, give me information about all the key entities being talked about, and identify the general sentiment about the entities give me the answer in three distinct sections",
            "temperature": 0.3,
            "max_new_tokens": 1000,
        }
    )
    return output

def summarize_article_c(page_text):
    response = co.chat(
	message=f"Go through this article \" {page_text} \" and summarise it, give me information about all the key entities being talked about, and identify the general sentiment about the entities give me the answer in three distinct sections" , 
	model="command", 
	temperature=0.9
    )

    answer = response.text

    return answer

st.title("Mixtral Article Summarizer")

url_input = st.text_input("Enter the URL of the article:")
if st.button("Summarize"):
    if url_input:
        try:
            page_text = scrape_article_text(url_input)
            llama1_output = summarize_article_m(page_text)
            llama2_output = summarize_article_c(page_text)

            st.header("Opensource LLM (Mixtral-7b-instruct) Output:")
            st.write(llama1_output)
            st.divider()
            st.header("Priprietry LLM (Cohere coral) Output:")
            st.write(llama2_output)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a valid URL.")
