import json
import os
from collections import defaultdict

# File to store scoreboard data
SCOREBOARD_FILE = "scoreboard.json"

# In-memory storage: {user_id: {"count": int, "username": str, "ping": bool}}
_scoreboard_data = defaultdict(lambda: {"count": 0, "username": "", "ping": True})

def load_data():
    """Load scoreboard data from JSON file on startup"""
    global _scoreboard_data
    if os.path.exists(SCOREBOARD_FILE):
        try:
            with open(SCOREBOARD_FILE, 'r') as f:
                data = json.load(f)
                # Migrate old data format to include "ping" field (default True)
                for user_id, user_data in data.items():
                    if "ping" not in user_data:
                        user_data["ping"] = True
                # Convert to defaultdict format
                _scoreboard_data = defaultdict(lambda: {"count": 0, "username": "", "ping": True}, data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading scoreboard data: {e}")
            _scoreboard_data = defaultdict(lambda: {"count": 0, "username": "", "ping": True})
    else:
        _scoreboard_data = defaultdict(lambda: {"count": 0, "username": "", "ping": True})

def save_data():
    """Save scoreboard data to JSON file"""
    try:
        # Convert defaultdict to regular dict for JSON serialization
        data_to_save = dict(_scoreboard_data)
        with open(SCOREBOARD_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=2)
    except IOError as e:
        print(f"Error saving scoreboard data: {e}")

def increment_count(user_id, username):
    """Increment count for a user when they say '67'"""
    user_id_str = str(user_id)
    _scoreboard_data[user_id_str]["count"] += 1
    _scoreboard_data[user_id_str]["username"] = username
    # Set ping to True by default if not already set
    if "ping" not in _scoreboard_data[user_id_str]:
        _scoreboard_data[user_id_str]["ping"] = True
    # Save periodically (every increment for now, could be optimized)
    save_data()

def get_leaderboard(limit=10):
    """
    Get top N users from leaderboard
    Returns list of tuples: (user_id, count, username, ping) sorted by count descending
    """
    # Sort by count descending, then by user_id for consistency
    sorted_users = sorted(
        _scoreboard_data.items(),
        key=lambda x: (x[1]["count"], x[0]),
        reverse=True
    )
    
    # Return top N as list of tuples: (user_id, count, username, ping)
    return [
        (user_id, data["count"], data["username"], data.get("ping", True))
        for user_id, data in sorted_users[:limit]
        if data["count"] > 0  # Only include users with count > 0
    ]

def get_user_count(user_id):
    """Get individual user's count"""
    user_id_str = str(user_id)
    return _scoreboard_data[user_id_str]["count"]

def set_ping_preference(user_id, ping_enabled):
    """Set whether a user should be pinged in leaderboard (True/False)"""
    user_id_str = str(user_id)
    _scoreboard_data[user_id_str]["ping"] = ping_enabled
    save_data()

def get_ping_preference(user_id):
    """Get whether a user should be pinged in leaderboard (defaults to True)"""
    user_id_str = str(user_id)
    return _scoreboard_data[user_id_str].get("ping", True)

