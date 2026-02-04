# GitHub Template Repository Setup

Two ways to automatically include the Cursor Starter Kit in new GitHub repositories:

## Option 1: GitHub Template Repository (Recommended)

Create a template repository that includes the starter kit, then use GitHub's "Use this template" feature.

### Step-by-Step Setup

#### Step 1: Create the Template Repository

**Option A: Using GitHub CLI (Recommended)**

```bash
# Create a new public repository for the template
gh repo create cursor-starter-kit-template \
  --public \
  --description "Template repository with Cursor Starter Kit" \
  --clone

# Navigate to the cloned repository
cd cursor-starter-kit-template
```

**Option B: Using GitHub Web Interface**

1. Go to https://github.com/new
2. Repository name: `cursor-starter-kit-template`
3. Description: "Template repository with Cursor Starter Kit"
4. Visibility: Public (or Private if you prefer)
5. **Do NOT** check "Add a README file" (we'll add the starter kit files)
6. Click "Create repository"

Then clone it:
```bash
gh repo clone <your-username>/cursor-starter-kit-template
cd cursor-starter-kit-template
```

#### Step 2: Copy Starter Kit Files

From your current repository, copy the starter kit to the template repo:

```bash
# Make sure you're in the template repository directory
cd cursor-starter-kit-template

# Copy all starter kit files (adjust path as needed)
cp -r /Users/ankit/Playground/_quantRepos/quant/cursor-starter-kit/* .

# Or if you're in the quant repo:
cp -r ../cursor-starter-kit/* .
```

**Files that should be copied:**
- `.cursorrules`
- `.cursorignore`
- `.gitignore`
- `.env.example`
- `README.md`
- `cursor-scripts/` (entire directory)
- `cursor-chats/` (entire directory with `.gitkeep`)
- `cursor-usage/` (entire directory with `.gitkeep`)
- `cursor-web-search/` (entire directory with `.gitkeep`)
- `mcp-bypass-skeleton/` (entire directory)
- `tests/` (entire directory)
- `install.sh` (optional - for manual installation)

**Note:** Do NOT copy `install.sh` if you want the template to be the final state (no installation needed).

#### Step 3: Verify Files

```bash
# Check that all files are present
ls -la
ls cursor-scripts/
ls tests/

# Verify key files exist
test -f .cursorrules && echo "✅ .cursorrules" || echo "❌ Missing .cursorrules"
test -f cursor-scripts/cursor_usage.py && echo "✅ cursor_usage.py" || echo "❌ Missing cursor_usage.py"
test -f tests/run_all.py && echo "✅ tests/run_all.py" || echo "❌ Missing tests"
```

#### Step 4: Commit and Push

```bash
# Stage all files
git add -A

# Commit
git commit -m "Initial template: Cursor Starter Kit

Includes:
- Cursor workflow scripts (usage tracking, chat export, web search)
- AI behavior rules (.cursorrules)
- Test suite
- MCP bypass skeleton
- Directory structure for chats, usage, web search"

# Push to GitHub
git push origin main
```

#### Step 5: Enable Template Mode

1. Go to your template repository on GitHub
2. Click **Settings** (top right of repository page)
3. Scroll down to **Template repository** section
4. Check the box: **☑ Template repository**
5. Click **Save** (or the changes auto-save)

**Verification:** After enabling, you should see a green **"Use this template"** button on the repository's main page.

#### Step 6: Test the Template

Create a test repository to verify it works:

**Option A: Using GitHub Web Interface**

1. Go to your template repository page
2. Click the green **"Use this template"** button
3. Select **"Create a new repository"**
4. Enter repository name: `test-cursor-kit`
5. Choose visibility (Private/Public)
6. **Optionally** check "Include all branches" (usually not needed)
7. Click **"Create repository from template"**

**Option B: Using GitHub CLI**

```bash
gh repo create test-cursor-kit \
  --template <your-username>/cursor-starter-kit-template \
  --private \
  --clone
```

**Verify the test repo:**
```bash
cd test-cursor-kit
ls -la
# Should see: .cursorrules, cursor-scripts/, tests/, etc.
```

#### Step 7: Using the Template for New Repos

**Every time you create a new repository:**

1. Go to your template repository: `https://github.com/<your-username>/cursor-starter-kit-template`
2. Click **"Use this template"** button
3. Click **"Create a new repository"**
4. Enter your new repository name
5. Choose visibility
6. Click **"Create repository from template"**

**Or use CLI:**
```bash
gh repo create my-new-project \
  --template <your-username>/cursor-starter-kit-template \
  --private \
  --clone
```

### Maintaining the Template

The template repository is **automatically synced** via a git hook whenever you commit changes to `cursor-starter-kit/`.

#### Setup (one-time)
```bash
cd /path/to/quant
./cursor-starter-kit/install-hook.sh
```

#### Daily Use
Just commit changes — the hook automatically syncs:
```bash
git add cursor-starter-kit/
git commit -m "update: Add feature"
git push
```

#### Manual Sync (if needed)
```bash
cd /path/to/quant/cursor-starter-kit
./sync-template.sh --dry-run  # Preview
./sync-template.sh --yes      # Sync, commit, push
```

**Note:** New repos created from the template will automatically get the latest version. Existing repos won't be affected (they have their own copy).

See `TEMPLATE-MAINTENANCE.md` for full documentation.

### Pros
- ✅ Built into GitHub UI
- ✅ One-click setup
- ✅ Works for all team members
- ✅ No local scripts needed

### Cons
- ❌ Requires maintaining a separate template repo
- ❌ Need to update template when starter kit changes

---

## Option 2: CLI Automation Script

Use the `create-repo-with-kit.sh` script to automate repo creation + installation.

### Setup

1. **Make script executable**:
   ```bash
   chmod +x cursor-starter-kit/create-repo-with-kit.sh
   ```

2. **Create an alias** (optional):
   ```bash
   # Add to ~/.zshrc
   alias new-repo='/path/to/cursor-starter-kit/create-repo-with-kit.sh'
   ```

### Usage

```bash
# Basic usage
./create-repo-with-kit.sh my-project --private --clone

# With description
./create-repo-with-kit.sh my-project --private --description "My awesome project" --clone

# In an organization
./create-repo-with-kit.sh my-project --org my-org --public --clone
```

### What it does

1. Creates GitHub repository via `gh repo create`
2. Clones the repository locally
3. Runs `install.sh` to add starter kit
4. Commits and pushes starter kit files
5. Provides next steps

### Pros
- ✅ Always uses latest starter kit
- ✅ Can customize per repo
- ✅ Works with any repo creation method

### Cons
- ❌ Requires GitHub CLI installed
- ❌ Requires running script manually
- ❌ Two-step process (create + install)

---

## Recommendation

**Use Option 1 (Template Repository)** for:
- Team workflows
- Consistent setup across projects
- One-click creation

**Use Option 2 (CLI Script)** for:
- Custom per-repo configurations
- Always using latest starter kit
- Automation in scripts/workflows

---

## Hybrid Approach

You can use both:
1. Create a template repo for quick starts
2. Use the CLI script when you need customization
3. Update template periodically from main starter kit
