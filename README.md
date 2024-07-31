
# Flask Student Performance API

## Overview

This project is a simple Flask web application for managing student performance data. The application allows you to upload CSV files to insert data into a MySQL database, and provides endpoints to create, read, update, and delete student records.

## Project Structure

- `app.py`: Main Flask application file that contains routes and logic for file uploads and database interactions.
- `Dockerfile`: Docker configuration file to containerize the Flask application.
- `requirements.txt`: List of Python dependencies required to run the Flask application.

## Setup

### Prerequisites

- Python 3.8+
- Docker (optional but recommended for containerization)

### Installation

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**

   Create a virtual environment and install the required packages:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configure MySQL**

   Ensure you have a MySQL server running with the following configuration:

   - Host: `172.31.80.1`
   - Port: `3306`
   - User: `admin`
   - Password: `root@123`
   - Database: `student_performance`

   Adjust the connection settings in `app.py` if necessary.

4. **Run the Flask Application**

   ```bash
   python app.py
   ```

   The application will be accessible at `http://localhost:5000`.

### Docker Setup

To containerize the Flask application using Docker:

1. **Build the Docker Image**

   ```bash
   docker build -t flask-student-performance .
   ```

2. **Run the Docker Container**

   ```bash
   docker run -p 5000:5000 flask-student-performance
   ```

   The application will be accessible at `http://localhost:5000` from within the container.

## API Endpoints

### Upload CSV

- **URL**: `/upload`
- **Method**: `POST`
- **Description**: Upload a CSV file to insert data into the database.
- **Parameters**: `file` (form-data)

### Get Records

- **URL**: `/get`
- **Method**: `GET`
- **Description**: Retrieve all student records from the database.

### Update Record

- **URL**: `/update/<id>`
- **Method**: `PUT`
- **Description**: Update a specific student record by ID.
- **Parameters**: JSON body with fields `StudentName`, `Gender`, `Age`, `GPA`.

### Create Record

- **URL**: `/create`
- **Method**: `POST`
- **Description**: Create a new student record.
- **Parameters**: JSON body with fields `StudentName`, `Gender`, `Age`, `GPA`.

### Delete Record

- **URL**: `/delete/<id>`
- **Method**: `DELETE`
- **Description**: Delete a student record by ID.

## File Descriptions

### `app.py`

Contains the Flask application logic:

- Connects to the MySQL database.
- Defines routes for handling file uploads, CRUD operations.
- Uses Pandas for reading CSV files and inserting data into the database.

### `Dockerfile`

Contains instructions to build a Docker image for the application:

- Uses Python 3.8 as the base image.
- Copies application files into the Docker container.
- Installs dependencies from `requirements.txt`.
- Exposes port 5000 and runs the Flask application.

### `requirements.txt`

Lists the required Python packages:

- `Flask`
- `pandas`
- `mysql-connector-python`
