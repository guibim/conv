#!/usr/bin/env bash
set -o errexit

echo "Updating system packages..."
sudo apt-get update

echo "Installing ExifTool..."
sudo apt-get install -y exiftool

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
