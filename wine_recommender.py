import pandas as pd
import streamlit as st
from knowmore import show_know_more
import random
import base64
import os
import re

st.set_page_config(page_title="GenesisGrape 🍷", layout="wide")

REVIEWS_CSV = "reviews.csv"

def load_reviews_from_csv():
    if os.path.exists(REVIEWS_CSV):
        try:
            df = pd.read_csv(REVIEWS_CSV)
            return list(df.itertuples(index=False, name=None))
        except pd.errors.EmptyDataError:


            return []
    return []


def save_reviews_to_csv(reviews):
    df = pd.DataFrame(reviews, columns=["rating", "review"])
    df.to_csv(REVIEWS_CSV, index=False)


def main():
    df = load_data()
    categories = ['Red', 'White', 'Sparkling', 'Dessert', 'Rose', 'Special']
    wine_category = st.selectbox("Choose wine category:", ["All"] + categories)

    sweetness_options = sorted(df['sweetness'].dropna().unique().tolist())
    sweetness = st.selectbox("Choose sweetness level:", ["All"] + sweetness_options)

    price_range = st.selectbox("Choose your budget:", [
        "All",
        "Below $10",
        "$10 - $20",
        "$20 - $50",
        "$50 - $100",
        "Above $100"
    ])

    selected_mood = st.selectbox("✨ (Optional) What's the Event about?", ["None"] + list(mood_wine_types.keys()))

    filtered = df.copy()

    filters_applied = (
            wine_category != "All"
            or sweetness != "All"
            or price_range != "All"
            or selected_mood != "None"
    )

    if filters_applied:
        if selected_mood != "None":
            mood_types = mood_wine_types[selected_mood]
            filtered = filtered[filtered['type'].isin(mood_types)]

        if wine_category != "All":
            filtered = filtered[filtered['Category'].str.contains(wine_category, case=False, na=False)]

        if sweetness != "All":
            filtered = filtered[filtered['sweetness'].str.contains(sweetness, case=False, na=False)]

        if price_range == "Below $10":
            filtered = filtered[filtered['Cost'] < 10]
        elif price_range == "$10 - $20":
            filtered = filtered[(filtered['Cost'] >= 10) & (filtered['Cost'] <= 20)]
        elif price_range == "$20 - $50":
            filtered = filtered[(filtered['Cost'] > 20) & (filtered['Cost'] <= 50)]
        elif price_range == "$50 - $100":
            filtered = filtered[(filtered['Cost'] > 50) & (filtered['Cost'] <= 100)]
        elif price_range == "Above $100":
            filtered = filtered[filtered['Cost'] > 100]
        top10 = (
            filtered.sort_values(by='rating', ascending=False)
            .drop_duplicates(subset=['name', 'producer'])  # 👈 this line prevents duplicates
            .head(10)
        )

        if top10.empty:
            st.warning("No wines found with those filters. Try loosening them a bit.")
        else:


                import urllib.parse

                for _, row in top10.iterrows():
                    with st.container():
                        wine_name_clean = urllib.parse.quote(row['name'])
                        google_link = f"https://www.google.com/search?q=site:lcbo.com+{wine_name_clean}"

                        html_block = f"""
                        <div class='wine-box'>
                            <div class='wine-title'>🍷 {row['name']}</div>
                            <div class='wine-details'>
                                <p>🏷️ <b>Producer:</b> {row['producer']}</p>
                                <p>🍇 <b>Style:</b> {row['style']}</p>
                                <p>🍬 <b>Sweetness:</b> {row['sweetness']}</p>
                                <p>💰 <b>Approx Price:</b> ${row['Cost']:.2f}</p>
                                <p>⭐ <b>Rating:</b> {row['rating']:.1f}</p>
                             <p>🍸 <b>Preferred Wine Glasses:</b> <span style='color:gold; font-weight:bold;'>{row['Glass type']}</span></p>
                                <a href='{google_link}' target='_blank' style='display:inline-block; margin-top:10px; background-color:#8B0000; color:white; padding:6px 12px; border-radius:6px; text-decoration:none;'>🔎 Find on LCBO (via Google)</a>
                                <p style='color:gold; font-style:italic; font-size:13px; margin-top:6px;'>Click the button above to search this wine on LCBO using Google — it’ll take you straight to the right page</p>
                            </div>
                        </div>
                        """
                        st.markdown(html_block, unsafe_allow_html=True)




    else:
        st.markdown(f"""
            <div class='fun-fact-box'>
                🍷 <b>Wine Fact:</b> {random.choice(wine_facts)}
            </div>
        """, unsafe_allow_html=True)
    # 💬 Universal Review Section (Always Visible)
    st.markdown("---")
    st.subheader("💬 Got something to say?")

    rating = st.slider(
        "Give it a rating:",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )

    # Review input
    review_text = st.text_area("Leave a quick note (optional, but we'd love to hear from you!)")

    # Submit logic
    if st.button("Send Review"):
        if review_text.strip():
            st.success(f"Review added! ⭐ {rating}/5")
            # Save logic here: (rating, review_text) → CSV or session
        else:
            st.warning("Please leave a quick note to submit.")


        if review_text.strip():
            st.session_state.reviews.append((rating, review_text))
            save_reviews_to_csv(st.session_state.reviews)  # Save to CSV
            st.session_state.visible_reviews = 2  # Reset count
            st.success("Thanks a bunch! 🍷 Your review has been added.")
        else:
            st.warning("Just a quick note would be great!")

    if st.session_state.reviews:
        st.markdown("### ⭐ What others are saying")

        total_reviews = len(st.session_state.reviews)
        visible_count = st.session_state.visible_reviews
        visible_reviews = list(reversed(st.session_state.reviews))[:visible_count]

        for i, (r, txt) in enumerate(visible_reviews, 1):
            st.markdown(f"**{i}.** ⭐ {r}/5")
            st.markdown(f"{txt}")

        if visible_count < total_reviews:
            if st.button("Load More Reviews"):
                st.session_state.visible_reviews += 2



def set_bg_image(image_file, opacity=0.1):
    # Load and encode the image
    with open(image_file, "rb") as img:
        b64 = base64.b64encode(img.read()).decode()
    # Inject CSS: white translucent layer + your background
    css = f"""
    <style>
    .stApp {{
        background:
          linear-gradient(rgba(255,255,255,{opacity}), rgba(255,255,255,{opacity})),
          url("data:image/jpeg;base64,{b64}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# 🚀 Call it with your red splash and desired translucency
set_bg_image("bgg.jpeg", opacity=0.1)


def load_data():
    df = pd.read_excel('winefinaldataset.xlsx', sheet_name='Final')

    df['Cost'] = df['Cost'].astype(str).str.replace('$', '').str.strip()
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['Cost', 'rating'])

    grouped = (
        df.groupby(['name', 'producer', 'style', 'sweetness', 'Cost', 'Category', 'type'])
        .agg({
            'Glass type': lambda x: ', '.join(pd.Series(x).dropna().unique()[:3]).replace('\n', ' ').replace('\r', ' '),
            'rating': 'mean'
        })
        .reset_index()
    )

    # 💫 Add default glasses to "Special" wines with missing or empty glass type
    default_glass = "Burgundy Glass, Bordeaux Glass, White Wine Glass"

    grouped['Glass type'] = grouped.apply(
        lambda row: default_glass if row['Category'] == "Special" and (
                    pd.isna(row['Glass type']) or not str(row['Glass type']).strip())
        else row['Glass type'],
        axis=1
    )

    return grouped


df = load_data()

# 💾 Initialize session state for favorites and reviews


if "reviews" not in st.session_state:
    st.session_state.reviews = load_reviews_from_csv()

if "visible_reviews" not in st.session_state:
    st.session_state.visible_reviews = 2  # Start with 2 reviews

mood_wine_types = {
    "Date": ["Pinot Noir/Chardonnay", "Rose", "Sparkling", "Moscato", "Champagne", "Red", "Dessert Wine"],
    "Party": ["Sparkling", "Champagne", "Fortified Wine", "Tawny Port", "Ruby Port", "Red Blend"],
    "Chill": ["White Blend", "Riesling", "Sparkling White", "Mead", "Fruit Wines"],
    "Professional": ["Cabernet Sauvignon", "Red Blend", "Late Bottled Vintage Port", "Sherry", "Vermouth"],
}

wine_facts = [
    "A standard wine glass holds about 5 ounces — sip, don't chug!",
    "Red wines are served slightly below room temperature — cool and classy.",
    "Sparkling wines are best in tall, narrow flutes to preserve the bubbles.",
    "Fortified wines like Port last longer once opened. Cheers to that!",
    "Sweet wines pair amazingly with spicy food. Don’t fight it!",
    "Decanting your wine can make it taste smoother by letting it breathe.",
    "Old wine bottles had bigger corks because they didn’t know about sealing tech.",
    "The swirl in your glass isn’t just fancy — it releases the wine’s aroma.",
    "Rosé gets its pink color from limited skin contact during fermentation.",
    "Some wines improve with age, but most are meant to be enjoyed young.",
    "The shape of the glass affects how the wine hits your tongue. Science, baby!",
    "Champagne isn’t just for celebrations — it pairs with nearly every meal.",
    "The word 'sommelier' means wine steward, the boss of your wine experience.",
    "Wine legs (those droplets on the glass) don’t mean quality — just alcohol content.",
    "In some cultures, wine is a symbol of life and celebration — fiesta time!",
    "The oldest known winery dates back over 6,000 years. History in a bottle!",
    "A wine’s terroir includes soil, climate, and grape variety — the wine’s fingerprint.",
    "Bubbles in sparkling wine are tiny carbon dioxide bubbles — that’s the fizz magic.",
    "Natural wine skips the additives — raw and real, like your wild side.",
    "Wine tasting is as much about the nose as the tongue — smell that beauty!"
]

# CSS including sexy shimmering effect and animations
st.markdown("""
<style>
body {
    background: radial-gradient(circle at center, #4b004b, #2e003e 60%, #15001b 90%);
    color: #f4e1f5;
    font-family: 'Georgia', serif;
}

.top-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding-top: 10px;
    margin-bottom: 20px;
}
.top-header h1 {
    font-family: 'Georgia', serif;
    color: #ffd700;
    font-size: 48px;
    margin: 0;
}
.top-header p {
    font-family: 'Georgia', serif;
    color: #f4e1f5;
    font-size: 18px;
    font-style: italic;
    margin: 4px 0 0 0;
}

.wine-box {
    background-color: #1c1c1c;
    color: #ffd700;
    border-radius: 10px;
    padding: 8px;
    margin: 8px 0;
    position: relative;
    cursor: pointer;
    overflow: hidden;
    transition: all 0.4s ease-in-out;
    border: 1px solid transparent;
}

.wine-box:hover {
    border: 1px solid #ffd700;
    box-shadow: 0 0 25px 6px #ffd700;
    background-color: #2a2a2a;
}

.wine-title {
    font-size: 20px;
    font-weight: bold;
    color: #ffd700;
    margin-bottom: 4px;
}

.wine-details {
    max-height: 0;
    opacity: 0;
    transition: all 0.4s ease-in-out;
    overflow: hidden;
    color: #fff;
    font-size: 14px;
}

.wine-box:hover .wine-details {
    max-height: 500px;
    opacity: 1;
    margin-top: 8px;
}
.fun-fact-box {
    border: 1px solid #ffd700;
    background-color: rgba(255, 255, 255, 0.05);
    color: #ffd700;
    border-radius: 10px;
    padding: 12px 20px;
    text-align: center;
    font-size: 14px;
    font-style: italic;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.4);
    margin: 30px 0 10px 0;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
}

/* Smooth transition on selectboxes */
.stSelectbox > div > div {
    transition: all 0.4s ease-in-out;
}
.stSelectbox:hover > div > div {
   box-shadow: 0 0 12px 3px dimgray !important;
    border-color: dimgray !important;
    border-radius: 8px;
}
@media only screen and (max-width: 768px) {
    .top-header h1 {
        font-size: 30px;
    }
    .top-header p {
        font-size: 14px;
    }
    .wine-title {
        font-size: 16px;
    }
    .wine-details {
        font-size: 13px;
    }
    .wine-box {
        padding: 6px;
        margin: 6px 0;
    }
    .fun-fact-box {
        padding: 8px 10px;
        font-size: 13px;
    }
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-header">
<h1>GenesisGrape 🍷</h1>
<p>“Your First Step Into the World of Wine”</p>
</div>
""", unsafe_allow_html=True)


# Filters


if __name__ == "__main__":
    page = st.sidebar.selectbox("🍇 Navigate", ["🍷 Recommender", "📚 Know More"])

    if page == "🍷 Recommender":
        main()
    elif page == "📚 Know More":
        show_know_more()




