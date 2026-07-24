from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Four Friends Number Game API",
    description="Simple Number Game for Four Friends",
    version="1.0"
)

# ===================================
# Pydantic Models
# ===================================

class FriendsGameRequest(BaseModel):
    friend1_name: str
    friend1_score: int

    friend2_name: str
    friend2_score: int

    friend3_name: str
    friend3_score: int

    friend4_name: str
    friend4_score: int


class FriendsGameResponse(BaseModel):
    winner: str
    highest_score: int
    total_score: int
    average_score: float
    message: str


# ===================================
# Home Page
# ===================================

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Friends Number Game</title>
        </head>
        <body style="font-family:Arial;text-align:center;margin-top:50px;">
            <h1>🎮 Four Friends Number Game API</h1>
            <p>Go to <a href="/docs">/docs</a> to play the game.</p>
        </body>
    </html>
    """


# ===================================
# Main Game API
# ===================================

@app.post("/play", response_model=FriendsGameResponse)
def play_game(data: FriendsGameRequest):

    scores = {
        data.friend1_name: data.friend1_score,
        data.friend2_name: data.friend2_score,
        data.friend3_name: data.friend3_score,
        data.friend4_name: data.friend4_score
    }

    winner = max(scores, key=scores.get)
    highest_score = scores[winner]

    total_score = sum(scores.values())
    average_score = total_score / 4

    return FriendsGameResponse(
        winner=winner,
        highest_score=highest_score,
        total_score=total_score,
        average_score=average_score,
        message=f"🏆 Congratulations {winner}! You won the game with {highest_score} points."
    )


# ===================================
# Bonus - View Scores
# ===================================

@app.post("/scores")
def show_scores(data: FriendsGameRequest):

    return {
        "Players": [
            {
                "Name": data.friend1_name,
                "Score": data.friend1_score
            },
            {
                "Name": data.friend2_name,
                "Score": data.friend2_score
            },
            {
                "Name": data.friend3_name,
                "Score": data.friend3_score
            },
            {
                "Name": data.friend4_name,
                "Score": data.friend4_score
            }
        ]
    }


# ===================================
# Bonus - Score Board
# ===================================

game_history = []

@app.post("/play_history")
def play_history(data: FriendsGameRequest):

    result = play_game(data)

    game_history.append(result.model_dump())

    return result


@app.get("/history")
def history():

    return {
        "total_games": len(game_history),
        "history": game_history[-10:]
    }
