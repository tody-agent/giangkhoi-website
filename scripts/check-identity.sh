#!/bin/bash

# Path to the identity configuration file
IDENTITY_FILE="$(dirname "$0")/../.project-identity.json"

if [ ! -f "$IDENTITY_FILE" ]; then
  echo -e "\033[0;31m❌ Error: .project-identity.json not found in project root!\033[0m"
  exit 1
fi

# Extract expected values using python (guaranteed to be installed on mac)
EXPECTED_GH_ACCOUNT=$(python3 -c "import json; print(json.load(open('$IDENTITY_FILE'))['github']['account'])")
EXPECTED_GH_EMAIL=$(python3 -c "import json; print(json.load(open('$IDENTITY_FILE'))['github']['userEmail'])")
EXPECTED_CF_ACCOUNT=$(python3 -c "import json; print(json.load(open('$IDENTITY_FILE'))['cloudflare']['accountId'])")
EXPECTED_CF_PROJECT=$(python3 -c "import json; print(json.load(open('$IDENTITY_FILE'))['cloudflare']['projectName'])")

echo "=================================================="
echo "🛡️  Identity Guard: Verification in progress..."
echo "=================================================="

# 1. Verify Git User Email
CURRENT_GH_EMAIL=$(git config user.email)
if [ "$CURRENT_GH_EMAIL" != "$EXPECTED_GH_EMAIL" ]; then
  echo -e "\033[0;31m❌ Git user.email mismatch!\033[0m"
  echo "   Current:  '$CURRENT_GH_EMAIL'"
  echo "   Expected: '$EXPECTED_GH_EMAIL'"
  echo "   Fix: git config user.email \"$EXPECTED_GH_EMAIL\""
  exit 1
else
  echo -e "\033[0;32m✅ Git user.email is correct: $CURRENT_GH_EMAIL\033[0m"
fi

# 2. Verify gh CLI Login
CURRENT_GH_ACCOUNT=$(gh api user -q .login 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$CURRENT_GH_ACCOUNT" ]; then
  echo -e "\033[0;33m⚠️  Warning: Failed to fetch user from GitHub CLI. Check if you are logged in.\033[0m"
  echo "   Run: gh auth login"
  exit 1
fi

if [ "$CURRENT_GH_ACCOUNT" != "$EXPECTED_GH_ACCOUNT" ]; then
  echo -e "\033[0;31m❌ GitHub CLI account mismatch!\033[0m"
  echo "   Current:  '$CURRENT_GH_ACCOUNT'"
  echo "   Expected: '$EXPECTED_GH_ACCOUNT'"
  echo "   Fix: gh auth switch -u \"$EXPECTED_GH_ACCOUNT\" or gh auth login"
  exit 1
else
  echo -e "\033[0;32m✅ GitHub CLI account is correct: $CURRENT_GH_ACCOUNT\033[0m"
fi

# 3. Verify Remote URL
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null)
if [ -z "$CURRENT_REMOTE" ]; then
  echo -e "\033[0;33m⚠️  Warning: No remote 'origin' configured yet.\033[0m"
else
  if [[ ! "$CURRENT_REMOTE" == *"$EXPECTED_GH_ACCOUNT"* ]]; then
    echo -e "\033[0;31m❌ Git remote origin mismatch!\033[0m"
    echo "   Current remote: '$CURRENT_REMOTE'"
    echo "   Expected account/org: '$EXPECTED_GH_ACCOUNT'"
    exit 1
  else
    echo -e "\033[0;32m✅ Git remote matches expected owner: $EXPECTED_GH_ACCOUNT\033[0m"
  fi
fi

# 4. Verify Cloudflare Account ID environment check
if [ ! -z "$CLOUDFLARE_ACCOUNT_ID" ]; then
  if [ "$CLOUDFLARE_ACCOUNT_ID" != "$EXPECTED_CF_ACCOUNT" ]; then
    echo -e "\033[0;31m❌ Cloudflare Account ID mismatch in environment!\033[0m"
    echo "   Current:  '$CLOUDFLARE_ACCOUNT_ID'"
    echo "   Expected: '$EXPECTED_CF_ACCOUNT'"
    exit 1
  else
    echo -e "\033[0;32m✅ Cloudflare Account ID environment variable matches expected.\033[0m"
  fi
fi

echo -e "\033[0;32m🎉 Identity verification passed. Safe to proceed.\033[0m"
exit 0
