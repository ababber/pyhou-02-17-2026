#!/bin/zsh

# cursor-new-chat.sh - Export current chat and clear history for fresh start
# Usage: ./cursor-scripts/cursor-new-chat.sh [--no-export]
#
# Options:
#   --no-export    Skip export, just clear history

SCRIPT_DIR="${0:a:h}"
REPO_ROOT="${SCRIPT_DIR}/.."
CHATS_DIR="$HOME/.cursor/chats"

# Parse arguments
SKIP_EXPORT=false
for arg in "$@"; do
    if [[ "$arg" == "--no-export" ]]; then
        SKIP_EXPORT=true
    fi
done

# Get workspace hash (most recent)
WORKSPACE_HASH=$(ls -t "$CHATS_DIR" 2>/dev/null | head -1)

if [[ -z "$WORKSPACE_HASH" ]]; then
    echo "No chat sessions found. Nothing to clear."
    exit 0
fi

# Count existing chats
CHAT_COUNT=$(ls "$CHATS_DIR/$WORKSPACE_HASH" 2>/dev/null | wc -l | tr -d ' ')

echo "Found $CHAT_COUNT chat session(s) for this workspace"

# Export current chat first (unless skipped)
if [[ "$SKIP_EXPORT" == "false" ]]; then
    echo ""
    echo "Exporting current chat..."
    "$SCRIPT_DIR/export-chat.sh"
    EXPORT_STATUS=$?
    
    if [[ $EXPORT_STATUS -ne 0 ]]; then
        echo "Export may have failed (exit code: $EXPORT_STATUS)"
        echo "Continue with clear anyway? (y/N)"
        read -r CONFIRM
        if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
            echo "Aborted."
            exit 1
        fi
    fi
else
    echo "Skipping export (--no-export flag)"
fi

# Clear chat history
echo ""
echo "Clearing chat history for workspace: $WORKSPACE_HASH"
rm -rf "$CHATS_DIR/$WORKSPACE_HASH"

if [[ $? -eq 0 ]]; then
    echo ""
    echo "Chat history cleared successfully!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Next: Exit this CLI session (Ctrl+C)"
    echo "  Then: Start a new CLI agent"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "Failed to clear chat history"
    exit 1
fi
