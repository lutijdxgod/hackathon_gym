Requirements
Before starting, make sure you have these installed:

Python 3.9+

1. Clone the Repository
git clone https://github.com/yourusername/your-repo-name.git cd your-repo-name

2. Set Up a Virtual Environment (Optional but Recommended)
python3 -m venv venv
source venv/bin/activate # On Windows, use env\Scripts\activate

3. Install Dependencies
Install all required Python packages by running:

pip install -r requirements.txt

4. Create .env file
The example file is .env.example

6. Create alembic.ini file
The example file is alembic.ini.example

7. Perform migrations
alembic upgrade head

8. Run the FastAPI Application
To start the FastAPI app with Uvicorn, run:

uvicorn app.main:app --reload The --reload flag automatically restarts the server when you make code changes.

9. Open the Application
Once the server is running, open your browser and go to:

http://127.0.0.1:8000/ You should see a welcome message.

7. Interactive API Docs
FastAPI automatically generates documentation for your API. Visit the interactive API docs at:

Swagger UI: http://127.0.0.1:8000/docs Redoc: http://127.0.0.1:8000/redoc
