#!/bin/bash

# Lock Cloudflare Account ID for this deployment
export CLOUDFLARE_ACCOUNT_ID="5a183e617c2e686d9b59b6b75b398b58"

# 1. Run check-identity script to verify safe context
"$(dirname "$0")/check-identity.sh"
RESULT=$?
if [ $RESULT -ne 0 ]; then
  echo -e "\033[0;31m❌ Deployment aborted: Identity validation failed.\033[0m"
  exit 1
fi

# 2. Build the project
echo "Building project..."
npm run build
if [ $? -ne 0 ]; then
  echo -e "\033[0;31m❌ Build failed.\033[0m"
  exit 1
fi

# 3. Deploy using Wrangler OAuth session
echo "Deploying to Cloudflare Pages..."
env -u CLOUDFLARE_API_TOKEN npx wrangler pages deploy dist --project-name giangkhoi-website --branch main
if [ $? -ne 0 ]; then
  echo -e "\033[0;31m❌ Deployment failed.\033[0m"
  exit 1
fi

echo -e "\033[0;32m🎉 Deployment completed successfully!\033[0m"
exit 0
