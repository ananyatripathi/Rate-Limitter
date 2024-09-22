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
- [API Endpoints](#api-endpoints)
  - [Token Bucket Algorithm](#token-bucket-algorithm)
  - [Leaking Bucket Algorithm](#leaking-bucket-algorithm)
  - [Fixed Window Counter Algorithm](#fixed-window-counter-algorithm)
  - [Sliding Window Log Algorithm](#sliding-window-log-algorithm)
- [Dependencies](#dependencies)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2.	Create a virtual environment and activate it:
   
   ```
    python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
4.	
