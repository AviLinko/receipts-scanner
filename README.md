# receipts-scanner


This project is a full-stack receipt scanning application built using **Python Flask** for the backend, with the frontend (React) pre-built and served from the backend. The application allows users to capture a receipt using their device’s camera, upload it to an AWS S3 bucket, extract text using **Google Vision API**, and summarize the products using **ChatGPT API**. Product data is stored in a PostgreSQL database and displayed in the frontend for easy tracking.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Setup and Installation](#setup-and-installation)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Future Improvements](#future-improvements)

## Features
- **Camera Capture**: Capture a photo of a receipt using the device's camera.
- **AWS S3 Integration**: Upload captured images to an AWS S3 bucket for storage.
- **Google Vision API**: Extract text from the uploaded images to recognize product names and prices.
- **ChatGPT Integration**: Summarize the extracted text to generate a structured list of products and quantities.
- **PostgreSQL Integration**: Store and retrieve products and their quantities in a PostgreSQL database.
- **Frontend Served via Backend**: The React frontend is built and served directly from the Flask backend.

## Technologies
- **Frontend**: React, JavaScript, HTML, CSS (pre-built and served via Flask)
- **Backend**: Python, Flask, Google Vision API, ChatGPT API, AWS S3
- **Database**: PostgreSQL
- **Deployment**: Docker (optional for containerization)

## Setup and Installation

### Prerequisites
- **Python 3.x** (for backend)
- **PostgreSQL** (for database)
- **AWS S3 account**
- **Google Vision API key**
- **ChatGPT API key**

### Backend (Flask)
1. Navigate to the `backend` directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

