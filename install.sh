#!/bin/bash

cd dirvish-stats
cd ui
npm install
rm -r ../../dirvish_server/dirvishserver/static/.h*
rm -r ../../dirvish_server/dirvishserver/static/*
node_modules/grunt-cli/bin/grunt deploy
cd ../../dirvish_server
