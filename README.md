# Chat-Application
TCP-based Chat Application

1. Server Program
• Accepts multiple client connections concurrently.
• Stores the usernames of connected clients.
• Broadcasts messages from one client to all others.
• Responds to /list command by sending a list of currently connected usernames to
requesting client.
• Handles client disconnections gracefully.

2. Client Program
• Connects to the server with a unique username.
• Can send messages to the server.
• Can use the /list command to view other connected users.
• Displays messages received from other clients via the server.
