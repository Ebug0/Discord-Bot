# Configuration file for Discord Bot
# Easily changeable settings for the bot

# List of user IDs (as strings) who can use the /leaderboard command
ALLOWED_LEADERBOARD_USERS = ["195618400796409856"]

# Channel ID where daily leaderboard posts (as integer or None to use channel name)
# If None, will use channel name "ebot-haven"
LEADERBOARD_CHANNEL_ID = None  # Set to channel ID (integer) or None for channel name

# Channel name to use if LEADERBOARD_CHANNEL_ID is None
LEADERBOARD_CHANNEL_NAME = "ebot-haven"

# Time for daily leaderboard post (24-hour format)
# Format: (hour, minute) - e.g., (8, 0) for 8:00 AM
LEADERBOARD_TIME = (8, 0)  # 8:00 AM

# Timezone for leaderboard time (None = server timezone, or specify timezone string)
# Examples: "UTC", "America/New_York", "Europe/London"
LEADERBOARD_TIMEZONE = None  # None uses server timezone

