import os
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)


prompt = ChatPromptTemplate.from_template(
"""
You are an AI news analyst.

Read the article text and return:

SUMMARY:
Write a clean 3-4 sentence summary.

CATEGORY:
Choose only one category from:
- AI Agents
- Machine Learning
- AI Research
- Industry News
- Robotics
- Generative AI
- Software Development
- Other


Article:
{article}


Return format:

SUMMARY:
<summary>

CATEGORY:
<category>

"""
)



def clean_text(text):

    text = re.sub(r"\*+", "", text)

    text = text.replace("#","")

    return text.strip()



def summarize_article(article):

    chain = prompt | llm


    response = chain.invoke(
        {
            "article": article
        }
    )


    result = response.content


    result = clean_text(result)


    return result