import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from heapq import nlargest

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="URL Content Summarizer",
    page_icon="📰",
    layout="centered"
)

# ---------------- LIGHT BACKGROUND STYLE ----------------
st.markdown("""
<style>

.stApp {
background-color: #f4f8ff;
}

h1 {
text-align: center;
color: #2c3e50;
}

.summary-box{
background-color: #ffffff;
padding:20px;
border-radius:10px;
box-shadow:0px 4px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📰 URL Article Summarizer")

st.write("Paste a webpage link and generate a short summary.")

# ---------------- INPUTS ----------------
url = st.text_input("🔗 Enter URL")

word_count = st.slider(
    "✂️ Select summary length (words)",
    min_value=5,
    max_value=200,
    value=50
)

generate = st.button("Generate Summary")

# ---------------- GET ARTICLE ----------------
def extract_article(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")

    text = ""
    for p in paragraphs:
        text += p.text

    return text


# ---------------- SUMMARIZE FUNCTION ----------------
def summarize(text, word_limit):

    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    sentences = re.split(r'(?<=[.!?]) +', text)

    words = re.findall(r'\w+', text.lower())

    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    sentence_scores = {}

    for sent in sentences:
        for word in re.findall(r'\w+', sent.lower()):
            if word in freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freq[word]

    summary_sentences = nlargest(10, sentence_scores, key=sentence_scores.get)

    summary = " ".join(summary_sentences)

    summary_words = summary.split()[:word_limit]

    return " ".join(summary_words)


# ---------------- BUTTON ACTION ----------------
if generate:

    if url == "":
        st.warning("Please enter a valid URL")

    else:
        with st.spinner("Fetching and summarizing article..."):

            article = extract_article(url)

            if len(article) < 200:
                st.error("Could not extract enough content from this page.")
            else:
                result = summarize(article, word_count)

                st.success("Summary Generated")

                st.markdown("### 📄 Summary")

                st.markdown(
                    f'<div class="summary-box">{result}</div>',
                    unsafe_allow_html=True
                )