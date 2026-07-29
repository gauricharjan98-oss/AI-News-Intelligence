from langchain_core.prompts import ChatPromptTemplate

SUMMARY_PROMPT = ChatPromptTemplate.from_template(
"""
You are an AI News Analyst.

Your job is to read the article and produce:

Summary:
- Write 3-5 concise sentences.

Category:
Choose ONE:
- Research
- Product Update
- Business
- Open Source
- Tutorial
- Other

Article:

{article}
"""
)