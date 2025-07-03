import re
import streamlit as st

def run_easy(quote, author, first_name, last_name):
    bio = quote["bio_description"]
    
    # Extract and clean all name parts
    name_parts = set(author.lower().split())
    
    # Redact all name parts in bio (case-insensitive)
    for name in name_parts:
        # Escape for regex, match whole word
        pattern = re.compile(rf'\b{re.escape(name)}\b', flags=re.IGNORECASE)
        bio = pattern.sub('[REDACTED]', bio)

    with st.expander("More Details >>"):
        st.write(bio)

    guess = st.text_input("Enter your guessed name of the author", key="easy_guess")
    if st.button("Submit"):
        st.session_state.easy_games += 1
        st.session_state.answered = True
        if first_name in guess.lower() or last_name in guess.lower():
            st.success("✅ Correct!")
            st.session_state.easy_score += 1
        else:
            st.error("❌ Wrong!")
