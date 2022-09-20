#!/bin/bash

# Constants
VERSION=$1
APP_NAME="crypto-screener"
PACKAGE_NAME="$APP_NAME-$VERSION.tar.gz"
APP_PACKAGE_FOLDER="dist"
APP_FOLDER="$HOME/App/$APP_NAME"

echo "Start deploy app: $PACKAGE_NAME to $APP_FOLDER"
rm -rf "$APP_FOLDER/$APP_NAME-$VERSION"
mkdir -p $APP_FOLDER
cp "$APP_PACKAGE_FOLDER/$PACKAGE_NAME" "$APP_FOLDER"
cd "$APP_FOLDER" || exit 1
tar -xvzf "$PACKAGE_NAME"
echo "Finished deploy app"