#!/bin/bash

echo "This file need environment Variables"


echo "Copy Files"
rsync --delete-delay -vrz --progress * $TARGET_DIR || exit 1
