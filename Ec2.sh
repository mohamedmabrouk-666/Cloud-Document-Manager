
#!/bin/bash

REPO_DIR="/opt/job-app-repo"


AWS_REGION="us-east-1"
S3_BUCKET="document-manager-602"

DB_HOST="database-1.caxcaqcocc4x.us-east-1.rds.amazonaws.com"    
DB_NAME="document_manager"
DB_USER="admin"
DB_PASSWORD="admin1234"

GITHUB_REPO="https://github.com/mohamedmabrouk-666/Cloud-Document-Manager"

# Install required packages
sudo apt-get update -y
sudo apt-get install -y python3 python3-venv python3-pip 
sudo apt install -y mariadb-client


# Clone project
# sudo git clone --depth 1 --branch main "$GITHUB_REPO" "$REPO_DIR"

# Create virtual environment
sudo python3 -m venv "$REPO_DIR/venv"

# Install requirements
sudo "$REPO_DIR/venv/bin/pip" install -r "$REPO_DIR/app/requirements.txt"

# Set environment variables
export DB_HOST="$DB_HOST"
export DB_PORT="3306"
export DB_NAME="$DB_NAME"
export DB_USER="$DB_USER"
export DB_PASSWORD="$DB_PASSWORD"
export S3_BUCKET="$S3_BUCKET"
export AWS_REGION="$AWS_REGION"

# Create database and tables in RDS
mysql \
    --host="$DB_HOST" \
    --user="$DB_USER" \
    --password="$DB_PASSWORD" \
    --protocol=tcp < "$REPO_DIR/database/schema.sql"

# Run Flask application
cd "$REPO_DIR/app"
"$REPO_DIR/venv/bin/python" app.py
