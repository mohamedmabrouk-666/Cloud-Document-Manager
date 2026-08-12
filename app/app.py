import os
import uuid
from datetime import datetime

import boto3
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, send_file, abort
from io import BytesIO


app = Flask(__name__)

# =========================
# Configuration
# =========================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

S3_BUCKET = os.getenv("S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


# =========================
# AWS S3
# =========================

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


# =========================
# Database
# =========================

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# =========================
# Health Check
# =========================

@app.route("/health")
def health():
    return "OK", 200


# =========================
# Home
# =========================

@app.route("/")
def index():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, filename, description, uploaded_at
        FROM documents
        ORDER BY uploaded_at DESC
    """)

    documents = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        documents=documents
    )


# =========================
# Upload
# =========================

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")
    description = request.form.get("description", "")

    if not file or file.filename == "":
        return redirect(url_for("index"))

    # Generate unique S3 key
    file_extension = os.path.splitext(file.filename)[1]

    s3_key = f"documents/{uuid.uuid4()}{file_extension}"

    # Upload file to S3
    s3.upload_fileobj(
        file,
        S3_BUCKET,
        s3_key
    )

    # Save metadata in RDS
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO documents
        (filename, description, s3_key)
        VALUES (%s, %s, %s)
    """, (
        file.filename,
        description,
        s3_key
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("index"))


# =========================
# Download
# =========================

@app.route("/download/<int:document_id>")
def download(document_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT filename, s3_key
        FROM documents
        WHERE id = %s
    """, (document_id,))

    document = cursor.fetchone()

    cursor.close()
    connection.close()

    if not document:
        abort(404)

    response = s3.get_object(
        Bucket=S3_BUCKET,
        Key=document["s3_key"]
    )

    file_data = response["Body"].read()

    return send_file(
        BytesIO(file_data),
        download_name=document["filename"],
        as_attachment=True
    )


# =========================
# Delete
# =========================

@app.route("/delete/<int:document_id>", methods=["POST"])
def delete(document_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT s3_key
        FROM documents
        WHERE id = %s
    """, (document_id,))

    document = cursor.fetchone()

    if not document:
        cursor.close()
        connection.close()
        abort(404)

    # Delete from S3
    s3.delete_object(
        Bucket=S3_BUCKET,
        Key=document["s3_key"]
    )

    # Delete metadata from RDS
    cursor.execute("""
        DELETE FROM documents
        WHERE id = %s
    """, (document_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("index"))


# =========================
# Run Application
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )