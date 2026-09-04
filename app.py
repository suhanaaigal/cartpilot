import re
import sqlite3
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb

app = FastAPI(title="CartPilot AI Engine")

# Enable CORS for browser frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. SQLite Database Setup ---
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

# --- 2. ChromaDB Setup & Dataset ---
chroma_client = chromadb.Client()

# Reset collection for fresh seed on startup
try:
    chroma_client.delete_collection(name="products")
except Exception:
    pass

collection = chroma_client.create_collection(name="products")

products_dataset = [
    # --- SMARTPHONES ---
    {
        "id": "p1",
        "doc": "Redmi 13C 5G 4GB RAM 128GB Storage affordable budget entry-level smartphone everyday use",
        "meta": {"id": "p1", "name": "Redmi 13C 5G (4GB RAM, 128GB)", "brand": "Redmi", "category": "smartphone", "price": 9999, "rating": 4.3}
    },
    {
        "id": "p2",
        "doc": "Realme 12 Pro+ 5G periscope camera curved AMOLED display mid-range camera phone",
        "meta": {"id": "p2", "name": "Realme 12 Pro+ 5G (8GB RAM, 256GB)", "brand": "Realme", "category": "smartphone", "price": 24999, "rating": 4.6}
    },
    {
        "id": "p3",
        "doc": "OnePlus Nord CE 4 5G Snapdragon 7 Gen 3 100W fast charging smooth performance mid-range",
        "meta": {"id": "p3", "name": "OnePlus Nord CE 4 5G", "brand": "OnePlus", "category": "smartphone", "price": 24999, "rating": 4.5}
    },
    {
        "id": "p4",
        "doc": "Samsung Galaxy S23 FE 5G 8GB RAM 128GB AMOLED Display flagship gaming high refresh rate",
        "meta": {"id": "p4", "name": "Samsung Galaxy S23 FE 5G", "brand": "Samsung", "category": "smartphone", "price": 49999, "rating": 4.5}
    },
    {
        "id": "p5",
        "doc": "iPhone 13 128GB A15 Bionic chip flagship camera high performance iOS premium",
        "meta": {"id": "p5", "name": "iPhone 13 (128GB)", "brand": "Apple", "category": "smartphone", "price": 45999, "rating": 4.7}
    },
    {
        "id": "p6",
        "doc": "iPhone 15 128GB Dynamic Island 48MP main camera USB-C port flagship Apple phone",
        "meta": {"id": "p6", "name": "iPhone 15 (128GB)", "brand": "Apple", "category": "smartphone", "price": 71900, "rating": 4.8}
    },
    {
        "id": "p7",
        "doc": "iQOO Neo 9 Pro 5G Snapdragon 8 Gen 2 extreme gaming phone high FPS liquid cooling",
        "meta": {"id": "p7", "name": "iQOO Neo 9 Pro 5G", "brand": "iQOO", "category": "smartphone", "price": 36999, "rating": 4.6}
    },

    # --- LAPTOPS ---
    {
        "id": "p8",
        "doc": "ASUS Vivobook 15 Intel Core i3 12th Gen 8GB RAM 512GB SSD thin light budget laptop college student work",
        "meta": {"id": "p8", "name": "ASUS Vivobook 15 Core i3", "brand": "ASUS", "category": "laptop", "price": 34990, "rating": 4.2}
    },
    {
        "id": "p9",
        "doc": "Lenovo IdeaPad Slim 3 AMD Ryzen 5 7520U 16GB RAM 512GB SSD coding student laptop office productivity",
        "meta": {"id": "p9", "name": "Lenovo IdeaPad Slim 3 Ryzen 5", "brand": "Lenovo", "category": "laptop", "price": 46990, "rating": 4.4}
    },
    {
        "id": "p10",
        "doc": "Apple MacBook Air M2 8GB Unified Memory 256GB SSD Retina display ultra thin lightweight long battery life",
        "meta": {"id": "p10", "name": "Apple MacBook Air M2", "brand": "Apple", "category": "laptop", "price": 89900, "rating": 4.9}
    },
    {
        "id": "p11",
        "doc": "HP Victus Gaming Laptop AMD Ryzen 5 5600H RTX 2050 4GB GPU 8GB RAM 512GB SSD high gaming performance",
        "meta": {"id": "p11", "name": "HP Victus Gaming (RTX 2050)", "brand": "HP", "category": "laptop", "price": 49999, "rating": 4.3}
    },
    {
        "id": "p12",
        "doc": "Acer Nitro V 15 Intel Core i5 13th Gen RTX 4050 6GB GPU 16GB RAM heavy gaming video editing laptop",
        "meta": {"id": "p12", "name": "Acer Nitro V 15 (RTX 4050)", "brand": "Acer", "category": "laptop", "price": 74990, "rating": 4.5}
    },

    # --- AUDIO & WEARABLES ---
    {
        "id": "p13",
        "doc": "boAt Airdopes 141 Bluetooth Wireless Earbuds 42H playback low latency gaming TWS",
        "meta": {"id": "p13", "name": "boAt Airdopes 141 TWS", "brand": "boAt", "category": "audio", "price": 1299, "rating": 4.1}
    },
    {
        "id": "p14",
        "doc": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones premium sound bluetooth microphone travel mic",
        "meta": {"id": "p14", "name": "Sony WH-1000XM5 ANC Headphones", "brand": "Sony", "category": "audio", "price": 28990, "rating": 4.8}
    },
    {
        "id": "p15",
        "doc": "Apple AirPods Pro 2nd Gen Active Noise Cancellation USB-C spatial audio premium TWS",
        "meta": {"id": "p15", "name": "Apple AirPods Pro (2nd Gen)", "brand": "Apple", "category": "audio", "price": 22900, "rating": 4.7}
    },
    {
        "id": "p16",
        "doc": "OnePlus Buds 3 TWS Active Noise Cancellation dual drivers deep bass Bluetooth earbuds",
        "meta": {"id": "p16", "name": "OnePlus Buds 3 TWS", "brand": "OnePlus", "category": "audio", "price": 5499, "rating": 4.4}
    },

    # --- CHARGERS & ACCESSORIES ---
    {
        "id": "p17",
        "doc": "Apple 20W USB-C Power Adapter official fast charger block for iPhone",
        "meta": {"id": "p17", "name": "Apple 20W USB-C Power Adapter", "brand": "Apple", "category": "accessory", "price": 1900, "rating": 4.8}
    },
    {
        "id": "p18",
        "doc": "Samsung Original 25W USB-C Fast Charging Adapter power adapter",
        "meta": {"id": "p18", "name": "Samsung Original 25W Type-C Adapter", "brand": "Samsung", "category": "accessory", "price": 1299, "rating": 4.6}
    },
    {
        "id": "p19",
        "doc": "Anker PowerBank 20000mAh 22.5W fast charging dual output portable power bank battery",
        "meta": {"id": "p19", "name": "Anker 20000mAh Power Bank", "brand": "Anker", "category": "accessory", "price": 3499, "rating": 4.5}
    },
    {
        "id": "p20",
        "doc": "Logitech MX Master 3S Wireless Performance Mouse ergonomic quiet clicks productivity office custom buttons",
        "meta": {"id": "p20", "name": "Logitech MX Master 3S Mouse", "brand": "Logitech", "category": "accessory", "price": 8995, "rating": 4.8}
    }
]

collection.add(
    documents=[item["doc"] for item in products_dataset],
    metadatas=[item["meta"] for item in products_dataset],
    ids=[item["id"] for item in products_dataset]
)

# --- 3. Request Models ---
class AgentRequest(BaseModel):
    prompt: str

class VerifyPaymentRequest(BaseModel):
    token: str
    razorpay_payment_id: str

# --- 4. Agent Endpoint ---
@app.post("/api/agent/run")
async def run_agent(req: AgentRequest):
    prompt_text = req.prompt.lower()
    
    # 1. Parse budget limit (e.g., 50k -> 50000)
    max_budget = 1000000
    k_match = re.search(r'(\d+)\s*k', prompt_text)
    num_match = re.search(r'(\d{4,6})', prompt_text)
    
    if k_match:
        max_budget = int(k_match.group(1)) * 1000
    elif num_match:
        max_budget = int(num_match.group(1))

    # 2. Vector search via ChromaDB
    results = collection.query(
        query_texts=[req.prompt],
        n_results=10
    )

    reasoning_logs = [
        f"Parsed user prompt: '{req.prompt}'",
        f"Detected maximum budget constraint: ₹{max_budget:,}" if max_budget < 1000000 else "No strict budget limit specified",
        f"Executed semantic query against ChromaDB vector repository"
    ]

    if not results or not results['metadatas'] or not results['metadatas'][0]:
        return {"status": "failed", "message": f"No product matches found within ₹{max_budget:,} constraint."}

    candidate_items = results['metadatas'][0]

    # Detect explicit brand requests in the prompt
    explicit_brand = None
    if "iphone" in prompt_text or "apple" in prompt_text:
        explicit_brand = "apple"
    elif "samsung" in prompt_text:
        explicit_brand = "samsung"
    elif "oneplus" in prompt_text:
        explicit_brand = "oneplus"

    # Prioritize items matching the explicitly requested brand
    if explicit_brand:
        candidate_items.sort(
            key=lambda x: (
                0 if explicit_brand in x['brand'].lower() or explicit_brand in x['name'].lower() else 1,
                -x['price']  # Pick highest specification device under max_budget
            )
        )

    selected_items = []
    total_cost = 0
    detected_brand = None

    # Step A: Select Primary Device (Smartphone/Laptop)
    for meta in candidate_items:
        if meta['category'] in ['smartphone', 'laptop'] and meta['price'] <= max_budget:
            selected_items.append(meta)
            total_cost += meta['price']
            detected_brand = meta['brand']
            reasoning_logs.append(f"Selected primary device: {meta['name']} (₹{meta['price']:,}) [Brand: {detected_brand}]")
            break

    # Step B: Select Matching Accessory (Deduplicating multiple adapters/chargers)
    remaining_candidates = [item for item in candidate_items if item.get('id') not in [x.get('id') for x in selected_items]]
    
    if detected_brand:
        remaining_candidates.sort(
            key=lambda x: (0 if x['brand'] == detected_brand else 1, x['price'])
        )

    added_adapter = False

    for meta in remaining_candidates:
        is_adapter = "adapter" in meta['name'].lower() or "charger" in meta['name'].lower()
        
        # Avoid adding multiple chargers
        if is_adapter and added_adapter:
            continue

        if (total_cost + meta['price']) <= max_budget:
            selected_items.append(meta)
            total_cost += meta['price']
            if is_adapter:
                added_adapter = True
            reasoning_logs.append(f"Bundled matching accessory: {meta['name']} (₹{meta['price']:,})")
        
        if len(selected_items) >= 2:  # Bundle Primary device + Primary matching accessory
            break

    if not selected_items:
        return {"status": "failed", "message": f"No product matches found within ₹{max_budget:,} constraint."}

    # 3. Generate & record reservation token in SQLite
    token = f"rzp_agentic_reserve_{uuid.uuid4().hex[:12]}"
    conn = sqlite3.connect("cartpilot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reservations (token, total_amount, status) VALUES (?, ?, ?)",
                   (token, total_cost, "RESERVED"))
    conn.commit()
    conn.close()

    reasoning_logs.append(f"Generated pre-authorization token: {token}")

    return {
        "status": "success",
        "max_budget": max_budget,
        "total_cost": total_cost,
        "reserve_token": token,
        "selected_items": selected_items,
        "reasoning_logs": reasoning_logs
    }

# --- 5. Payment Verification Endpoint ---
@app.post("/api/agent/verify-payment")
async def verify_payment(req: VerifyPaymentRequest):
    conn = sqlite3.connect("cartpilot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE reservations SET status = 'PAID', payment_id = ? WHERE token = ?",
                   (req.razorpay_payment_id, req.token))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Reservation settled successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8005)