# Flask Rate Limiting API

This Flask application demonstrates four rate-limiting algorithms: 
- **Token Bucket** 
- **Leaking Bucket** 
- **Fixed Window Counter**
- **Sliding Window Log**

Each algorithm has its own API endpoint for configuration and handling requests.

## Table of Contents
- [Installation](#installation)
- [Run the Application](#run-the-application)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
   
2. Create a virtual environment and activate it:
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   
3.	Install dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

4.	Install the required Flask and CORS packages if they aren’t listed in requirements.txt:
   
   ```bash
   pip install Flask flask-cors pydantic
   ```


## Run the application

To start the Flask server, run:

   ```bash
   python app.py
   ```

The application will run at http://127.0.0.1:5000/.


