import random
import streamlit as st
from logic_utils import check_guess, get_range_for_difficulty, update_score
import json
import os

# CSS Theme Dictionary
THEMES = {
    "Default (System)": "",
    "Cyberpunk": """
        <style>
        .stApp { background-color: #0d0e15; }
        h1, h2, h3, p, div, span, label { color: #00ff41 !important; }
        [data-testid="stSidebar"] { background-color: #000000; border-right: 2px solid #00ff41; }
        .stButton>button { border: 2px solid #00ff41; color: #00ff41 !important; background-color: transparent; }
        .stButton>button:hover { background-color: #00ff41; color: #000000 !important; }
        div[data-baseweb="select"] > div { background-color: #000000; border: 1px solid #00ff41; color: #00ff41; }
        </style>
    """,
    "Retro Sunset": """
        <style>
        .stApp { background-color: #2b1055; }
        h1, h2, h3, p, div, span, label { color: #ff9e7d !important; }
        [data-testid="stSidebar"] { background-color: #1a083a; border-right: 2px solid #f67280; }
        .stButton>button { background: linear-gradient(45deg, #f67280, #c06c84); color: white !important; border: none; font-weight: bold; }
        .stButton>button:hover { filter: brightness(1.2); }
        div[data-baseweb="select"] > div { background-color: #351c75; border: 1px solid #f67280; color: white; }
        </style>
    """
}


def reset_game_state(low: int, high: int, difficulty: str):
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.game_difficulty = difficulty
    st.session_state.game_id = st.session_state.get("game_id", 0) + 1


def get_feedback_message(outcome: str):
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Go LOWER!"
    return "📈 Go HIGHER!"


SCORES_FILE = "high_scores.json"


def load_high_scores():
    default_scores = {"Easy": 0, "Normal": 0, "Hard": 0}
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default_scores
    return default_scores


def save_high_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

# Theme Switcher Logic
st.sidebar.header("🎨 Appearance")
selected_theme = st.sidebar.selectbox("Choose a Theme", list(THEMES.keys()))

# Inject the chosen CSS
if THEMES[selected_theme]:
    st.markdown(THEMES[selected_theme], unsafe_allow_html=True)

st.title("🎮 Game Glitch Investigator")

# Sidebar Configuration
if "high_scores" not in st.session_state:
    st.session_state.high_scores = load_high_scores()

st.sidebar.divider()
st.sidebar.header("⚙️ Settings")
difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}

attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"**Range:** {low} to {high}")
st.sidebar.caption(f"**Attempts allowed:** {attempt_limit}")

# Initialize or Check State
required_keys = {"secret", "attempts", "score",
                 "status", "history", "game_difficulty", "game_id"}
if not required_keys.issubset(st.session_state.keys()) or st.session_state.game_difficulty != difficulty:
    reset_game_state(low, high, difficulty)

st.sidebar.divider()
st.sidebar.header("🏆 High Scores")

# Display the high scores using Streamlit's native metric component
for diff_level, best_score in st.session_state.high_scores.items():
    st.sidebar.metric(label=f"{diff_level} Best", value=best_score)

# Main Game UI
st.subheader("Make a guess")
attempts_left = attempt_limit - st.session_state.attempts

# Visual Progress Bar for Attempts
progress_fraction = max(0.0, attempts_left / attempt_limit)
st.progress(progress_fraction, text=f"Attempts left: {attempts_left}")

# Game Over / Win State Checks
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.balloons()
        st.success(
            f"You won! The secret was {st.session_state.secret}. Final score: {st.session_state.score}")
    else:
        st.error(
            f"Game over! The secret was {st.session_state.secret}. Final score: {st.session_state.score}")

    if st.button("New Game 🔁"):
        reset_game_state(low, high, difficulty)
        st.rerun()
    st.stop()

# Gameplay Form
with st.form("guess_form", clear_on_submit=True):
    guess_int = st.number_input(
        f"Enter a number between {low} and {high}:",
        step=1
    )

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        submit = st.form_submit_button("Submit Guess 🚀")
    with col2:
        show_hint = st.checkbox("Show hints", value=True)

# Out-of-form New Game Button
if st.button("Restart Game 🔁"):
    reset_game_state(low, high, difficulty)
    st.rerun()

# Logic Execution
if submit:
    if guess_int < low or guess_int > high:
        st.error(
            f"⚠️ Whoops! **{guess_int}** is out of bounds. Please guess a number between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)
        message = get_feedback_message(outcome)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"

            current_difficulty = st.session_state.game_difficulty
            if st.session_state.score > st.session_state.high_scores[current_difficulty]:
                st.session_state.high_scores[current_difficulty] = st.session_state.score
                st.toast(f"New High Score for {current_difficulty}!", icon="🏆")
                save_high_scores(st.session_state.high_scores)

            st.rerun()
        else:
            if show_hint:
                st.warning(f"**{guess_int}** was incorrect. {message}")

            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.rerun()

# History Display
if st.session_state.history:
    st.divider()
    st.subheader("📜 Guess History")
    history_str = " → ".join([str(g) for g in st.session_state.history])
    st.info(history_str)

st.divider()
st.caption("Built by an AI that claims this code is production-ready. (And is now styling via CSS injection).")
