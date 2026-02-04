#!/bin/zsh
#
# Create a new GitHub repository with Cursor Starter Kit
#
# Usage:
#   ./create-repo-with-kit.sh <repo-name> [options]
#
# Options:
#   --private, --public, --internal  Repository visibility
#   --description "text"            Repository description
#   --clone                         Clone after creation
#   --org <org-name>                Create in organization
#
# Examples:
#   ./create-repo-with-kit.sh my-new-project --private --clone
#   ./create-repo-with-kit.sh my-project --org my-org --public
#

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STARTER_KIT_DIR="$SCRIPT_DIR"
INSTALL_SCRIPT="$STARTER_KIT_DIR/install.sh"

# Check for gh CLI
if ! command -v gh &> /dev/null; then
    echo "${YELLOW}❌ GitHub CLI (gh) not found${NC}"
    echo ""
    echo "Install it with:"
    echo "  brew install gh"
    echo "  gh auth login"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "${YELLOW}❌ Not authenticated with GitHub${NC}"
    echo ""
    echo "Run: gh auth login"
    exit 1
fi

# Parse arguments
REPO_NAME=""
VISIBILITY=""
DESCRIPTION=""
CLONE=false
ORG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --private|--public|--internal)
            VISIBILITY="$1"
            shift
            ;;
        --description)
            DESCRIPTION="$2"
            shift 2
            ;;
        --clone)
            CLONE=true
            shift
            ;;
        --org)
            ORG="$2"
            shift 2
            ;;
        --help|-h)
            head -20 "$0" | grep -E "^#|^$" | sed 's/^# //'
            exit 0
            ;;
        *)
            if [ -z "$REPO_NAME" ]; then
                REPO_NAME="$1"
            else
                echo "${YELLOW}⚠️  Unknown option: $1${NC}"
            fi
            shift
            ;;
    esac
done

if [ -z "$REPO_NAME" ]; then
    echo "${YELLOW}❌ Repository name required${NC}"
    echo ""
    echo "Usage: $0 <repo-name> [options]"
    echo "Run with --help for more information"
    exit 1
fi

# Build gh repo create command
GH_CMD="gh repo create"

if [ -n "$ORG" ]; then
    GH_CMD="$GH_CMD $ORG/$REPO_NAME"
else
    GH_CMD="$GH_CMD $REPO_NAME"
fi

if [ -n "$VISIBILITY" ]; then
    GH_CMD="$GH_CMD $VISIBILITY"
fi

if [ -n "$DESCRIPTION" ]; then
    GH_CMD="$GH_CMD --description \"$DESCRIPTION\""
fi

if [ "$CLONE" = true ]; then
    GH_CMD="$GH_CMD --clone"
fi

echo "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo "${BLUE}  Create GitHub Repo with Cursor Starter Kit${NC}"
echo "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "Repository: ${ORG:+$ORG/}$REPO_NAME"
echo "Visibility: ${VISIBILITY:---public (default)}"
echo ""

# Create repository
echo "${BLUE}Creating GitHub repository...${NC}"
eval "$GH_CMD" || {
    echo "${YELLOW}❌ Failed to create repository${NC}"
    exit 1
}

echo "${GREEN}✅ Repository created${NC}"
echo ""

# Determine repo path
if [ "$CLONE" = true ]; then
    REPO_PATH="$(pwd)/$REPO_NAME"
    if [ -n "$ORG" ]; then
        REPO_PATH="$(pwd)/$REPO_NAME"
    fi
else
    if [ -n "$ORG" ]; then
        REPO_PATH="/tmp/$REPO_NAME"
        echo "${BLUE}Cloning repository to $REPO_PATH...${NC}"
        gh repo clone "$ORG/$REPO_NAME" "$REPO_PATH" || {
            echo "${YELLOW}❌ Failed to clone repository${NC}"
            exit 1
        }
    else
        USERNAME=$(gh api user --jq .login)
        REPO_PATH="/tmp/$REPO_NAME"
        echo "${BLUE}Cloning repository to $REPO_PATH...${NC}"
        gh repo clone "$USERNAME/$REPO_NAME" "$REPO_PATH" || {
            echo "${YELLOW}❌ Failed to clone repository${NC}"
            exit 1
        }
    fi
fi

# Install starter kit
echo ""
echo "${BLUE}Installing Cursor Starter Kit...${NC}"
cd "$REPO_PATH"
INSTALL_SKIP_EXISTING=0 INSTALL_FORCE=1 "$INSTALL_SCRIPT" "$REPO_PATH" || {
    echo "${YELLOW}❌ Failed to install starter kit${NC}"
    exit 1
}

# Commit and push
echo ""
echo "${BLUE}Committing starter kit files...${NC}"
git add -A
git commit -m "add: Cursor Starter Kit

- Added cursor-scripts for workflow automation
- Added .cursorrules for AI behavior
- Added tests for verification
- See README.md for usage" || {
    echo "${YELLOW}⚠️  No changes to commit (starter kit may already be present)${NC}"
}

echo "${BLUE}Pushing to GitHub...${NC}"
git push || {
    echo "${YELLOW}⚠️  Push failed or no changes${NC}"
}

echo ""
echo "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo "${GREEN}✅ Repository created with Cursor Starter Kit!${NC}"
echo "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "Repository: $(gh repo view --json url -q .url)"
echo "Local path: $REPO_PATH"
echo ""
echo "${BLUE}Next steps:${NC}"
echo "1. cd $REPO_PATH"
echo "2. Add API keys to .env"
echo "3. Run tests: python tests/run_all.py"
echo ""
