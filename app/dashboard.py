import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


import streamlit as st
from collections import Counter
import pandas as pd

from db.database import SessionLocal
from db.models import ContentItem



# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI News Intelligence",
    page_icon="🤖",
    layout="wide"
)



# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
"""
<style>


/* Whole app background */

.stApp {

    background:
    linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #1e3a8a,
        #2563eb
    );

    color:white;

}



/* Remove default white blocks */

[data-testid="stHeader"] {

    background:transparent;

}



/* Global text */

html, body, 
.stMarkdown,
.stText,
p,
h1,h2,h3,h4,
label,
span {

    color:white !important;

    font-family:
    "Arial",
    sans-serif;

}



/* Title */

h1 {

    font-size:65px !important;

    font-weight:900;

    letter-spacing:-3px;

}



/* Sidebar */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
    180deg,
    #020617,
    #1e40af
    );

}


section[data-testid="stSidebar"] * {

    color:white !important;

}



/* Metric cards */


.metric-card {


    background:
    linear-gradient(
    135deg,
    #1d4ed8,
    #3b82f6
    );


    border-radius:20px;

    padding:25px;

    border:2px solid rgba(255,255,255,0.3);

    box-shadow:
    0 10px 30px rgba(0,0,0,0.4);


}



.metric-title {


    font-size:18px;

    opacity:0.8;


}



.metric-value {


    font-size:45px;

    font-weight:900;


}




/* News cards */


.news-card {


    background:

    rgba(255,255,255,0.12);


    backdrop-filter:blur(10px);


    border-radius:20px;


    padding:25px;


    margin-bottom:25px;


    border:

    1px solid rgba(255,255,255,0.3);


    box-shadow:

    0 10px 30px rgba(0,0,0,0.3);


}



.news-card h2 {


    color:white !important;


}



.news-card p {


    color:#e2e8f0 !important;


    font-size:17px;


}



/* Category badge */


.category {


    display:inline-block;


    background:#38bdf8;


    color:#020617 !important;


    padding:8px 15px;


    border-radius:30px;


    font-weight:bold;


}



/* Buttons */


.stButton button {


    background:#38bdf8 !important;


    color:#020617 !important;


    border-radius:20px;


    font-weight:bold;


}



/* Link buttons */


a {


    color:#7dd3fc !important;


}



/* Divider */


hr {

border:1px solid rgba(255,255,255,0.3);

}



</style>

""",

unsafe_allow_html=True

)




# --------------------------------------------------
# HEADER
# --------------------------------------------------


st.markdown(
"""
# 🤖 AI NEWS
# INTELLIGENCE SYSTEM


### Autonomous AI News Research Agent

Collect → Analyze → Summarize → Deliver


---
"""
)




# --------------------------------------------------
# DATABASE
# --------------------------------------------------


session = SessionLocal()



articles = (

    session.query(ContentItem)

    .filter(ContentItem.summary != None)

    .order_by(ContentItem.created_at.desc())

    .all()

)



session.close()



if not articles:


    st.warning(
        "No summarized articles found. Run the pipeline first."
    )

    st.stop()




# --------------------------------------------------
# METRICS
# --------------------------------------------------


total_articles = len(articles)



categories = [

    a.category.strip()
    if a.category
    else "Unknown"

    for a in articles

]



sources = [

    a.source_id

    for a in articles

]



unique_categories = len(set(categories))

unique_sources = len(set(sources))



col1,col2,col3 = st.columns(3)



with col1:

    st.markdown(

    f"""

    <div class="metric-card">

    <div class="metric-title">
    TOTAL NEWS
    </div>

    <div class="metric-value">
    {total_articles}
    </div>


    </div>

    """,

    unsafe_allow_html=True

    )



with col2:

    st.markdown(

    f"""

    <div class="metric-card">

    <div class="metric-title">
    CATEGORIES
    </div>

    <div class="metric-value">
    {unique_categories}
    </div>


    </div>

    """,

    unsafe_allow_html=True

    )



with col3:


    st.markdown(

    f"""

    <div class="metric-card">


    <div class="metric-title">
    SOURCES
    </div>


    <div class="metric-value">
    {unique_sources}
    </div>


    </div>

    """,

    unsafe_allow_html=True

    )





st.divider()




# --------------------------------------------------
# SIDEBAR FILTER
# --------------------------------------------------


st.sidebar.title(
    "🔎 FILTER SYSTEM"
)



selected_category = st.sidebar.selectbox(

    "CATEGORY",

    ["ALL"] + sorted(list(set(categories)))

)



search = st.sidebar.text_input(

    "SEARCH NEWS"

)




filtered_articles = articles



if selected_category != "ALL":

    filtered_articles = [

        a for a in filtered_articles

        if (a.category or "Unknown")
        == selected_category

    ]



if search:


    filtered_articles = [

        a for a in filtered_articles

        if search.lower()
        in a.title.lower()

    ]





# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------


st.header(
    "📊 NEWS DISTRIBUTION"
)



chart_df = pd.DataFrame(

    Counter(categories).items(),

    columns=[
        "Category",
        "Count"
    ]

)



st.bar_chart(

    chart_df,

    x="Category",

    y="Count"

)



st.divider()




# --------------------------------------------------
# NEWS FEED
# --------------------------------------------------


st.header(
    "🔥 LATEST INTELLIGENCE"
)




for article in filtered_articles:


    category = (

        article.category

        if article.category

        else "Unknown"

    )


    summary = (

        article.summary

        if article.summary

        else "No summary available."

    )



    st.markdown(

    f"""

    <div class="news-card">


    <h2>
    {article.title}
    </h2>


    <div class="category">

    {category}

    </div>


    <br><br>


    <p>

    {summary}

    </p>


    </div>

    """,

    unsafe_allow_html=True

    )



    if article.url:


        st.link_button(

            "READ ORIGINAL ARTICLE",

            article.url

        )



# --------------------------------------------------
# FOOTER
# --------------------------------------------------


st.divider()



st.markdown(

"""
## ⚡ SYSTEM ARCHITECTURE


RSS → Python → SQLite → Groq LLM → LangGraph → Streamlit


### Autonomous AI News Research Agent v1.0

Built with:
RSS + Python + SQLite + Groq + LangGraph + Streamlit

"""

)