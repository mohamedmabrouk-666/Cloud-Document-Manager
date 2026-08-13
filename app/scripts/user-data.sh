#!/bin/bash

REPO_DIR="/opt/job-app-repo"

GITHUB_REPO="https://github.com/mohamedmabrouk-666/Cloud-Document-Manager"

apt-get update -y

apt-get install -y git

git clone --depth 1 --branch main "$GITHUB_REPO" "$REPO_DIR"

bash "$REPO_DIR/Ec2.sh"
