import streamlit as st

MAX_HARD_GUESSES = 4

def run_hard(quote, author):
    if "guesses_left" not in st.session_state:
        st.session_state.guesses_left = MAX_HARD_GUESSES

    guess = st.text_input("Enter the author's full name", key="hard_guess")
    if st.button("Submit"):
        if st.session_state.answered:
            st.warning("Click 'Next Quote' to continue.")
        else:
            if guess.strip().lower() == author.lower():
                st.success("✅ Correct!")
                st.session_state.hard_score += 1
                st.session_state.hard_games += 1
                st.session_state.answered = True
            else:
                st.session_state.guesses_left -= 1
                if st.session_state.guesses_left > 0:
                    st.warning(f"❌ Incorrect. {st.session_state.guesses_left} guesses left.")
                    if st.session_state.guesses_left == 3:
                        st.info(f"Hint: Born on {quote['birth_date']} {quote['birth_place']}")
                    elif st.session_state.guesses_left == 2:
                        st.info(f"Hint: First name starts with '{author[0]}'")
                    elif st.session_state.guesses_left == 1:
                        st.info(f"Hint: Last name starts with '{author.split(' ')[-1][0]}'")
                else:
                    st.error(f"❌ Out of guesses. The correct author was: **{author}**")
                    st.session_state.hard_games += 1
                    st.session_state.answered = True
