#!/bin/bash
# Deploy Chabad History Wiki to Netlify
set -e

export NETLIFY_AUTH_TOKEN=nfp_2WntL676njwwXYtQyT6hiSJxHHfAw4kZ2711
export XDG_CONFIG_HOME=/tmp/netlify-config
NETLIFY=/tmp/netlify-work/node_modules/.bin/netlify

echo "Building Quartz site..."
cd /workspace/group/chabad-history-wiki
npx quartz build

echo "Deploying to Netlify..."
$NETLIFY deploy --prod --dir public --message "${1:-Redeploy}"

echo "Done! Live at https://chabad-history-wiki.netlify.app"
