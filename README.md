# id-checker-app

This is a full stack app written in python(Django) and vue.js for frontend. The app's purpose is to allow users to inout their South Africa ID number to check if there are any important public holidays on their date of birth and stores the information in a mysql databse.

## How to Start the Backend Server

### Prerequisites

Ensure the following are installed on your system:
- Python (3.10 or above recommended)
- MySQL
- Virtualenv

### Steps to Start the Backend Server

1. **Clone the repository** and navigate to the `backend` directory:
   ```bash
   cd backend

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Run server
   ```bash
   cd id_checker
   python manage.py runserver   
