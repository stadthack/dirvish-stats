#!/bin/bash

echo "This file need environment Variables"

echo "Copy Files"
rsync --delete-delay -vrz --progress * $TARGET_HOST:$TARGET_DIR || exit 1
ssh $TARGET_HOST "cd $TARGET_HOST && bash install.sh"

