# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [X] Describe the game's purpose.

The game's purpose is to guess a number in some range in a limited number of guesses.

- [X] Detail which bugs you found.

Main issues:
- The hints were backwards
- Pressing "New Game" after finishing the game does nothing (except for creating a new secret number)
- The developer debug history lags 1 turn behind the actual history

Additional issues I found:
- Final score is different from debug score
- Number of attempts in the sidebar differs from actual allowed attempts
- Score keeps resetting to 0 sometimes even if you submit the same guess multiple times (if the guess is close enough)


- [X] Explain what fixes you applied.

1. Fixed hints being backwards (by changing signs)
2. New Game now properly resets the state.
3. Developer Debug was removed completely
4. Synchronized attempts counters
5. Score is counted correctly now

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features


