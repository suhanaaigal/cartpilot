# CartPilot AI 🛒🤖

**AI-powered e-commerce agent for intelligent product search, budget constraint solving, and product bundling.**

CartPilot understands natural-language shopping requests, performs semantic vector search, and creates optimized product bundles while respecting the user's budget.

### 🚀 Features

* 💰 **Budget Constraint Solving** – Enforces limits like "under ₹50,000".
* 🧠 **Semantic Search** – Uses ChromaDB for intent-based product retrieval.
* 🔗 **Smart Bundling** – Matches compatible accessories and avoids duplicates.
* 💳 **Payment Integration** – Demonstrates Razorpay checkout and payment states.
* 🗃️ **Transaction Management** – Uses SQLite for reservation and payment tracking.

### 🛠️ Tech Stack

**Frontend:** HTML, Tailwind CSS, JavaScript
**Backend:** Python, FastAPI
**Vector Database:** ChromaDB
**Database:** SQLite
**Payment:** Razorpay JS SDK

### ⚙️ Setup

Clone the repository:

```bash
git clone https://github.com/suhanaaigal/cartpilot.git
cd cartpilot
```

Install dependencies:

```bash
pip install fastapi uvicorn chromadb pydantic
```

Start the backend:

```bash
python app.py
```

Backend runs on:

```text
http://127.0.0.1:8005
```

In a new terminal, start the frontend:

```bash
python -m http.server 8080
```

Open:

```text
http://127.0.0.1:8080
```

### 🧪 Example Prompts

```text
iPhone under 50k with charger
Mobile under 10000
Laptop for heavy gaming
```

### 🔮 Future Scope

* LLM-based intent parsing
* AI guardrails
* Live inventory and pricing APIs
* Advanced bundle optimization

---

**CartPilot AI — Turning e-commerce search into intelligent constraint solving.**
