import random
import streamlit as st
from scraper import load_quotes_from_cache, scrape_quotes
from easy import run_easy
from medium import run_medium
from hard import run_hard

MAX_GAMES_PER_ROUND = 50
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
LABELS = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}

def initialize_session_state():
    defaults = {
        "quote": None,
        "answered": False,
        "difficulty": "easy",  # lowercase key
        "prev_difficulty": "easy",
        "easy_score": 0,
        "medium_score": 0,
        "hard_score": 0,
        "easy_games": 0,
        "medium_games": 0,
        "hard_games": 0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def load_next_quote(quotes):
    if quotes:
        st.session_state.quote = random.choice(quotes)
        st.session_state.answered = False
        if st.session_state.difficulty == "hard":
            st.session_state.guesses_left = 4
        if "medium_attempts" in st.session_state:
            st.session_state.medium_attempts = 0

# Load quotes
quotes = load_quotes_from_cache()
if not quotes:
    quotes = scrape_quotes(start_index=0)

initialize_session_state()

# Reload if batch of 50 rounds complete
total_games = (
    st.session_state.easy_games +
    st.session_state.medium_games +
    st.session_state.hard_games
)

if total_games >= MAX_GAMES_PER_ROUND:
    st.warning("🔁 50 rounds completed. Loading next 10 quotes...")
    quotes = scrape_quotes(start_index=total_games)
    load_next_quote(quotes)
    st.rerun()

st.set_page_config(page_title="Who Said That?", layout="centered")
st.title("Who Said That? - Quote Guessing Game")

# Sidebar
st.sidebar.header("Difficulty")
difficulty = st.sidebar.radio(
    "Select difficulty",
    options=DIFFICULTY_LEVELS,
    format_func=lambda x: LABELS[x],  # shows capitalized labels
    index=DIFFICULTY_LEVELS.index(st.session_state.difficulty)
)

if difficulty != st.session_state.prev_difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.prev_difficulty = difficulty
    load_next_quote(quotes)
    st.rerun()
else:
    st.session_state.difficulty = difficulty

st.sidebar.header("Progress")
st.sidebar.text(f"Easy    = {st.session_state.easy_score} / {st.session_state.easy_games}")
st.sidebar.text(f"Medium  = {st.session_state.medium_score} / {st.session_state.medium_games}")
st.sidebar.text(f"Hard    = {st.session_state.hard_score} / {st.session_state.hard_games}")

if st.sidebar.button("🔄 Reset Game"):
    quotes = scrape_quotes(start_index=total_games)
    for key in [
        "easy_score", "medium_score", "hard_score",
        "easy_games", "medium_games", "hard_games"
    ]:
        st.session_state[key] = 0
    load_next_quote(quotes)
    st.rerun()

# Quote rendering
quote = st.session_state.quote or random.choice(quotes)
st.session_state.quote = quote

author = quote["author"]
first_name = author.split(" ")[0].lower()
last_name = author.split(" ")[-1].lower()

st.markdown("### Quote")
st.write(f"_{quote['text']}_")
st.caption("Tags: " + ", ".join(quote.get("tags", [])))

# Difficulty mode
if st.session_state.difficulty == "easy":
    run_easy(quote, author, first_name, last_name)
elif st.session_state.difficulty == "medium":
    run_medium(quote, author, first_name, last_name)
else:
    run_hard(quote, author)

# Show author bio after guess
if st.session_state.answered:
    st.markdown("### 📚 Author Bio")
    st.write(f"**{author}**")
    st.write(f"Born on {quote['birth_date']} {quote['birth_place']}")
    with st.expander("More Details >>"):
        st.write(quote["bio_description"])

    if st.button("➡️ Next Quote"):
        load_next_quote(quotes)
        st.rerun()
