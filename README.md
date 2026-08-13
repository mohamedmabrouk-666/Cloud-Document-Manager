# Cloud Document Manager

A simple web application for uploading and managing documents using AWS.

The main goal of this project is to practice deploying a real application on AWS and working with cloud infrastructure.

## Architecture

The application follows a 3-tier architecture:

![AWS Architecture](architecture.png)

```text
User
  |
  v
Application Load Balancer
  |
  v
EC2 Instances
  |
  +---------> Amazon RDS (MySQL)
  |
  +---------> Amazon S3
```

### Tiers

**Presentation Tier**

* HTML
* CSS

**Application Tier**

* Flask
* Python
* EC2

**Data Tier**

* Amazon RDS
* MySQL
* Amazon S3

## AWS Services

* Amazon VPC
* Amazon EC2
* Application Load Balancer
* Auto Scaling
* Amazon RDS
* Amazon S3
* AWS IAM
* Amazon CloudWatch
* Security Groups

## Application Features

* Upload documents
* Store document files in Amazon S3
* Store document information in Amazon RDS
* List uploaded documents
* Download documents
* Delete documents
* Health check endpoint for the Load Balancer

## Project Structure

```text
cloud-document-manager/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
│
├── database/
│   └── schema.sql
│
├── .gitignore
└── README.md
```

## Environment Variables

The application uses the following environment variables:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
S3_BUCKET
AWS_REGION
```

## Running Locally

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r app/requirements.txt
```

Set the required environment variables and run:

```bash
python3 app/app.py
```

The application will run on:

```text
http://localhost:5000
```

Health check:

```text
http://localhost:5000/health
```

## Cloud Architecture

The application servers run on EC2 instances behind an Application Load Balancer.

The application stores:

* Document files in Amazon S3
* Document metadata in Amazon RDS

EC2 instances use an IAM role to access S3 without storing AWS access keys inside the application.

## What I Practiced

Through this project, I practiced:

* Building a 3-tier application architecture
* AWS VPC networking
* Public and private subnets
* EC2 deployment
* Application Load Balancer
* Auto Scaling
* Amazon RDS
* Amazon S3
* IAM roles and permissions
* Security Groups
* CloudWatch monitoring

## Notes

This project is mainly focused on the cloud infrastructure and AWS architecture. The application itself is intentionally kept simple so that the main focus remains on deploying and operating the application in AWS.
