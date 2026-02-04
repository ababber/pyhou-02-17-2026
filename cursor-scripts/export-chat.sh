#!/bin/zsh

# Export Cursor CLI chat history to markdown
# Usage: export-chat.sh [output_dir]

SCRIPT_DIR="${0:a:h}"
REPO_ROOT="${SCRIPT_DIR}/.."
OUTPUT_DIR="${1:-${REPO_ROOT}/cursor-chats}"
CHATS_DIR="$HOME/.cursor/chats"

# Detect environment
if docker ps &>/dev/null; then
    ENV_TYPE="CLI"
else
    ENV_TYPE="IDE"
fi

TODAY=$(date +%Y-%d-%m)
# Output file will be determined by Python script based on size
OUTPUT_DIR_PY="${OUTPUT_DIR}"
ENV_TYPE_PY="${ENV_TYPE}"
TODAY_PY="${TODAY}"

# Find the most recent chat session
WORKSPACE_HASH=$(ls -t "$CHATS_DIR" 2>/dev/null | head -1)
if [[ -z "$WORKSPACE_HASH" ]]; then
    echo "No chat sessions found in $CHATS_DIR"
    exit 1
fi

# Find the most recent chat within that workspace
CHAT_ID=$(ls -t "$CHATS_DIR/$WORKSPACE_HASH" 2>/dev/null | head -1)
if [[ -z "$CHAT_ID" ]]; then
    echo "No chats found in $CHATS_DIR/$WORKSPACE_HASH"
    exit 1
fi

DB_PATH="$CHATS_DIR/$WORKSPACE_HASH/$CHAT_ID/store.db"
if [[ ! -f "$DB_PATH" ]]; then
    echo "Database not found: $DB_PATH"
    exit 1
fi

# Extract messages and format as markdown
python3 << EOF
import sqlite3
import json
import sys
import os
import glob
from datetime import datetime

db_path = "$DB_PATH"
output_dir = "$OUTPUT_DIR_PY"
env_type = "$ENV_TYPE_PY"
today = "$TODAY_PY"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all blobs
cursor.execute("SELECT data FROM blobs")
rows = cursor.fetchall()

def format_content(content):
    """Parse and format message content from JSON structure."""
    if not content:
        return ""
    
    # Content might be a JSON string or already parsed
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except (json.JSONDecodeError, TypeError):
            # If it's not JSON, return as-is (plain text)
            return content
    
    # If content is a list (array of message parts)
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict):
                part_type = part.get('type', '')
                if part_type == 'text':
                    text = part.get('text', '')
                    if text:
                        parts.append(text)
                elif part_type == 'tool-call':
                    # Format tool calls nicely
                    tool_name = part.get('toolName', 'unknown')
                    tool_id = part.get('toolCallId', '')[:8] if part.get('toolCallId') else ''
                    parts.append(f"<tool_call: {tool_name} (id: {tool_id})>")
                elif part_type == 'tool-result':
                    # Optionally include tool results (might be verbose)
                    tool_name = part.get('toolName', 'unknown')
                    parts.append(f"<tool_result: {tool_name}>")
        return "\n".join(parts)
    
    # If content is already a string, return it
    if isinstance(content, str):
        return content
    
    # Fallback: convert to string
    return str(content)

messages = []
for row in rows:
    try:
        # Handle both text and binary blobs
        blob_data = row[0]
        if isinstance(blob_data, bytes):
            try:
                blob_data = blob_data.decode('utf-8')
            except UnicodeDecodeError:
                continue  # Skip binary blobs
        
        data = json.loads(blob_data)
        if isinstance(data, dict) and 'role' in data:
            role = data.get('role', '')
            content = data.get('content', '')
            if role in ('user', 'assistant') and content:
                # Parse and format content
                formatted_content = format_content(content)
                if formatted_content:
                    messages.append((role, formatted_content))
    except (json.JSONDecodeError, TypeError, AttributeError):
        continue

conn.close()

if not messages:
    print("No user/assistant messages found")
    sys.exit(1)

# Find existing session files for today
pattern = f"{output_dir}/CURSOR-{env_type}_{today}_*.md"
existing_files = sorted(glob.glob(pattern))

# Determine output file
if not existing_files:
    # First file of the day
    session_num = 1
    output_file = f"{output_dir}/CURSOR-{env_type}_{today}_{session_num:02d}.md"
    file_exists = False
else:
    # Check size of most recent file
    latest_file = existing_files[-1]
    file_size = os.path.getsize(latest_file) if os.path.exists(latest_file) else 0
    
    if file_size >= MAX_FILE_SIZE:
        # Need new session file
        # Extract session number from latest file (format: _NN.md)
        import re
        match = re.search(r'_(\d+)\.md$', latest_file)
        if match:
            session_num = int(match.group(1)) + 1
        else:
            session_num = len(existing_files) + 1
        output_file = f"{output_dir}/CURSOR-{env_type}_{today}_{session_num:02d}.md"
        file_exists = False
    else:
        # Append to existing file
        output_file = latest_file
        file_exists = True
        # Extract session number from filename (format: _NN.md)
        import re
        match = re.search(r'_(\d+)\.md$', output_file)
        session_num = int(match.group(1)) if match else 1

# Write to file
with open(output_file, 'a' if file_exists else 'w') as f:
    if not file_exists:
        f.write(f"# Cursor Chat Log - {today}\n\n")
        f.write(f"_Environment: Cursor {env_type}_\n\n")
        f.write("---\n\n")
        session_count = 1
    else:
        # Count existing sessions in file
        with open(output_file, 'r') as rf:
            content = rf.read()
            session_count = content.count('## Session') + 1
        f.write("\n---\n\n")
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    f.write(f"## Session {session_count} - {timestamp}\n\n")
    f.write("---\n\n")
    
    for role, content in messages:
        role_label = "User" if role == "user" else "Assistant"
        f.write(f"**{role_label}**\n\n")
        f.write(f"{content}\n\n")
        f.write("---\n\n")

print(f"Exported to {output_file}")
EOF
