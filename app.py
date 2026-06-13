import streamlit as st
import requests
from datetime import datetime

# ----------------------------
# CONFIGURATION
# ----------------------------
API_KEY = st.secrets["API_KEY"]
BASE_URL = "https://newsapi.org/v2/top-headlines"

st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

# ----------------------------
# TITLE
# ----------------------------
st.title("📰 Advanced News Dashboard")
st.markdown("Fetch and explore the latest headlines from around the world.")

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("News Filters")

country_options = {
    "United States": "us",
    "India": "in",
    "Singapore": "sg",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Japan": "jp"
}

country_name = st.sidebar.selectbox(
    "Select Country",
    list(country_options.keys())
)

country = country_options[country_name]

category = st.sidebar.selectbox(
    "Select Category",
    [
        "general",
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "technology"
    ]
)

keyword = st.sidebar.text_input(
    "Search Keywords",
    placeholder="e.g. AI, Tesla, Cricket"
)

num_articles = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=10
)

refresh = st.sidebar.button("🔄 Refresh News")

# ----------------------------
# FETCH FUNCTION
# ----------------------------
@st.cache_data(ttl=300)
def get_news(country, category, keyword, page_size):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "category": category,
        "pageSize": page_size
    }

    if keyword.strip():
        params["q"] = keyword

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "status": "error",
            "message": f"API Error: {response.status_code}"
        }

# ----------------------------
# LOAD NEWS
# ----------------------------
with st.spinner("Fetching latest headlines..."):
    data = get_news(
        country,
        category,
        keyword,
        num_articles
    )

# ----------------------------
# DISPLAY RESULTS
# ----------------------------
if data.get("status") == "ok":

    articles = data.get("articles", [])

    st.success(f"Found {len(articles)} articles")

    for idx, article in enumerate(articles, start=1):

        with st.container():

            col1, col2 = st.columns([1, 3])

            with col1:
                if article.get("urlToImage"):
                    st.image(
                        article["urlToImage"],
                        use_container_width=True
                    )

            with col2:
                st.subheader(f"{idx}. {article.get('title', 'No Title')}")

                source = article.get("source", {}).get("name", "Unknown")

                published = article.get("publishedAt")

                if published:
                    try:
                        published = datetime.fromisoformat(
                            published.replace("Z", "+00:00")
                        ).strftime("%d %b %Y %H:%M")
                    except:
                        pass

                st.caption(
                    f"Source: {source} | Published: {published}"
                )

                description = article.get(
                    "description",
                    "No description available."
                )

                st.write(description)

                if article.get("url"):
                    st.link_button(
                        "Read Full Article",
                        article["url"]
                    )

            st.divider()

else:
    st.error(data.get("message", "Failed to fetch news"))

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.markdown(
    "Built with Streamlit + NewsAPI"
)