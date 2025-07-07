# GitHub Webhook Event Tracker

This project captures **GitHub webhook events** like Push, Pull Request, and Merge, and stores them in MongoDB. A simple frontend polls the backend every 15 seconds and displays the latest events.

## How It Works

1. A GitHub webhook is configured on a separate repo (`action-repo`)
2. When a push, PR, or merge happens, GitHub sends a POST request to:

   ```
   /github-webhook
   ```
3. Flask parses the event and stores it in MongoDB
4. A `/latest-events` endpoint returns stored events as JSON
5. `index.html` calls this endpoint every 15 seconds and updates the UI

---

### Setup

```bash
# Clone this repo
git clone https://github.com/AshishAgam/webhook-repo.git
cd webhook-repo

# Create virtual environment
python -m venv venv
source venv\Scripts\activate  # or on Linux venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Start Flask Server

```bash
python run.py
```

### Start Ngrok

```bash
ngrok http 5000
```

Copy the HTTPS forwarding URL and set it in your **GitHub Webhook settings** (on the action-repo).

---

