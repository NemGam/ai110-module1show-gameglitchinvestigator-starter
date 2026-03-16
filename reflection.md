# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

Main issues:
- The hints were backwards
- Pressing "New Game" after finishing the game does nothing (except for creating a new secret number)
- The developer debug history lags 1 turn behind the actual history

Additional issues I found:
- Final score is different from debug score
- Number of attempts in the sidebar differs from actual allowed attempts
- Score keeps resetting to 0 sometimes even if you submit the same guess multiple times (if the guess is close enough)

---

## 2. How did you use AI as a teammate?

I utilized Copilot as a teammate who helped me to refactor logic into a separate file as well as find some obvious bugs.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Copilot suggested to add more variables to the state reset that I've missed. To verify that, I went into the game and checked that everything is reset on a new game start.


- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

It ran hints test before fixing the bug and said it worked just fine but when I ran the same tests it showed incorrect results. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

First I traced the logic to see if it makes sense. Then I played multiple times trying to break that section of the game.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

I ran pytests on hints to check if the hint is correct but due to the simplicity of that check I made only a few. This test showed me how important it is to split the logic into smaller testable chunks. 

- Did AI help you design or understand any tests? How?

AI helped me to design the "new game" test and even update it after we came up with more variables to reset.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit is like a forgetful robot that re-reads an entire instruction manual every time someone presses a button. Session state is the clipboard it checks before re-reading, it remembers what happened before so the robot doesn't forget the game progress, secret number, and attempt count.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Breaking logic into smaller, testable chunks that can be unit tested independently. This made it much easier to verify my fixes and catch bugs early. I'd apply this to future projects by writing helper functions in separate modules

- What is one thing you would do differently next time you work with AI on a coding task?

I'd trust AI outputs less blindly and always verify test results myself. When Copilot said the hints test passed but my manual run showed failures, I learned that AI can confidently give wrong answers

- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI is a great brainstorming partner for refactoring and spotting obvious bugs, but it's not a substitute for your own verification. This project showed me that AI works best when I treat it as a teammate to bounce ideas off, not as an authority