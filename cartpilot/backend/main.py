from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import cart_pilot_agent
import sqlite3

app = FastAPI()

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Setup for Payment Reservations ---
def init_db():
    conn = sqlite3.connect("cartpilot.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            token TEXT PRIMARY KEY,
            total_amount REAL,
            status TEXT,
            payment_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class AgentRequest(BaseModel):
    prompt: str

class VerifyPaymentRequest(BaseModel):
    token: str
    razorpay_payment_id: str

@app.post("/api/agent/run")
async def run_agent(request: AgentRequest):
    result = cart_pilot_agent(request.prompt)
    
    # Store reservation token in database
    if result.get("status") == "success":
        token = result.get("reserve_token")
        total_cost = result.get("total_cost", 0)
        if token:
            conn = sqlite3.connect("cartpilot.db")
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO reservations (token, total_amount, status) VALUES (?, ?, ?)",
                          (token, total_cost, "RESERVED"))
            conn.commit()
            conn.close()
    
    return result

@app.post("/api/agent/verify-payment")
async def verify_payment(req: VerifyPaymentRequest):
    """Verify Razorpay payment and update reservation status"""
    conn = sqlite3.connect("cartpilot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE reservations SET status = 'PAID', payment_id = ? WHERE token = ?",
                   (req.razorpay_payment_id, req.token))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Reservation verified and settled.", "razorpay_payment_id": req.razorpay_payment_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)