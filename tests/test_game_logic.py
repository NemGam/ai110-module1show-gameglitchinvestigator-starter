from logic_utils import check_guess
from app import get_feedback_message, reset_game_state


class FakeSessionState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_hints_are_correct():
    # Hint text should point in the right direction for each outcome.
    assert get_feedback_message("Too High") == "📉 Go LOWER!"
    assert get_feedback_message("Too Low") == "📈 Go HIGHER!"
    assert get_feedback_message("Win") == "🎉 Correct!"


def test_game_resets_correctly(monkeypatch):
    fake_state = FakeSessionState(
        {
            "secret": 999,
            "attempts": 3,
            "score": 40,
            "status": "lost",
            "history": [10, 20, 30],
            "game_difficulty": "Easy",
            "game_id": 7,
        }
    )

    monkeypatch.setattr("app.st.session_state", fake_state)
    monkeypatch.setattr("app.random.randint", lambda low, high: 42)

    reset_game_state(1, 100, "Hard")

    assert fake_state.secret == 42
    assert fake_state.attempts == 0
    assert fake_state.score == 0
    assert fake_state.status == "playing"
    assert fake_state.history == []
    assert fake_state.game_difficulty == "Hard"
    assert fake_state.game_id == 8
