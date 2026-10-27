import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Multiplayer Game State Service")

# Establish network connection to the NoSQL DB container across subnets
try:
    r = redis.Redis(host='192.168.146.10', port=6379, decode_responses=True)
except Exception as e:
    print(f"Failed to connect to Redis data node: {e}")

class GameState(BaseModel):
    player_id: str
    match_id: str
    x_pos: float
    y_pos: float
    score: int

@app.post("/update_state")
def update_state(state: GameState):
    try:
        # Save player state map fields into Redis hashes
        key = f"player:{state.player_id}"
        r.hset(key, mapping={
            "match_id": state.match_id,
            "x_pos": state.x_pos,
            "y_pos": state.y_pos,
            "score": state.score
        })
        return {"status": "success", "message": f"State updated for {state.player_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database write failure: {str(e)}")

@app.get("/get_state/{player_id}")
def get_state(player_id: str):
    key = f"player:{player_id}"
    # Retrieve field data map from NoSQL engine
    data = r.hgetall(key)
    if not data:
        raise HTTPException(status_code=404, detail="Player state record not found")
    return {
        "player_id": player_id,
        "match_id": data["match_id"],
        "x_pos": float(data["x_pos"]),
        "y_pos": float(data["y_pos"]),
        "score": int(data["score"])
    }

@app.get("/health")
def health_check():
    try:
        r.ping()
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "unhealthy", "database": "disconnected"}

# docker cp main.py api_server:/main.py
# docker exec -d nosql_db redis-server --protected-mode no --bind 0.0.0.0
# docker exec -d api_server uvicorn main:app --host 0.0.0.0 --port 8000

# run this to check the connection with redis
# docker exec -it game_client curl http://192.168.145.10:8000/health
