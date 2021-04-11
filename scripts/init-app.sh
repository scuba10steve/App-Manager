#!/usr/bin/env bash
set -x
PORT=8080

curl -XPOST "http://localhost:$PORT/app" -H "Content-Type: application/json" -d "{    \"app_id\": 1,    \"has_installer\": false,    \"has_uninstaller\": false,    \"installed\": true,    \"name\": \"app-manager\",    \"source_url\": \"https://github.com/scuba10steve/App-Manager/releases/download/v0.1.0/package-v0.1.0.tar.bz2\",    \"system\": \"linux\"}"

set +x