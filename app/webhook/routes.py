from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app.extensions import github_events


webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/github-webhook", methods=["POST"])
def github_webhook():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    # Defaults
    author = "unknown"
    request_id = None
    action = None
    from_branch = None
    to_branch = None
    timestamp = datetime.utcnow().isoformat()

    if event_type == "push":
        request_id = data.get("after")
        author = data.get("pusher", {}).get("name", "unknown")
        ref = data.get("ref", "")  # e.g. refs/heads/main
        to_branch = ref.split("/")[-1] if ref else None
        action = "PUSH"

    elif event_type == "pull_request":
        pr_action = data.get("action")  # "opened", "closed", etc.
        pr = data.get("pull_request", {})

        # Handle only 'opened' pull requests
        if pr_action == "opened":
            request_id = str(pr.get("id"))
            author = pr.get("user", {}).get("login", "unknown")
            from_branch = pr.get("head", {}).get("ref")
            to_branch = pr.get("base", {}).get("ref")
            action = "PULL REQUEST"

        # Handle merged pull requests (i.e., merged == true and action == "closed")
        elif pr_action == "closed" and pr.get("merged", False):
            request_id = str(pr.get("id"))
            author = pr.get("user", {}).get("login", "unknown")
            from_branch = pr.get("head", {}).get("ref")
            to_branch = pr.get("base", {}).get("ref")
            action = "MERGE"

        else:
            return jsonify({"message": f"Ignored pull_request action: {pr_action}"}), 200

    else:
        return jsonify({"message": f"Ignored event type: {event_type}"}), 200

    # Build and insert event
    event = {
        "request_id": request_id,
        "author": author,
        "action": action,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    }

    result = github_events.insert_one(event)
    event["_id"] = str(result.inserted_id)

    return jsonify({"message": "Event stored", "event": event}), 201


# This route displays the latest events
@webhook_bp.route("/latest-events", methods=["GET"])
def latest_events():
    events = list(github_events.find().sort("timestamp", -1).limit(10))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify({"events": events})


# This route serves the index.html
@webhook_bp.route("/")
def index():
    return render_template("index.html")