#!/bin/bash

echo "This file need environment Variables"

export PATH=$PATH:/opt/node/bin

echo "Copy Files"
rsync --delete-delay -vrz --progress * $TARGET_DIR || exit 1

cd dirvish-stats
cd ui
npm install
rm -r ../../dirvish_server/dirvishserver/static/.h*
rm -r ../../dirvish_server/dirvishserver/static/*
node_modules/grunt-cli/bin/grunt deploy
cd ../../dirvish_server
