# AI-Powered Finance Manager

## Live Demo
[https://a-finance-manager.streamlit.app/] - *It is deployed, may take some time to wake up but will surely work broski*

## Project Overview
The AI-Powered Finance Manager is a comprehensive web application designed to help users track their income and expenses, plan savings goals, and receive personalized financial advice powered by AI. Built with Streamlit, Firebase for backend services, and Groq for AI capabilities, this application offers a user-friendly interface for managing personal finances effectively.

## Features

*   **User Authentication:** Secure login and signup functionality using email and password, powered by Firebase Authentication.
*   **Dashboard**:
    *   Overview of total income, total expenses, and net income.
    *   Interactive charts visualizing income vs. expense trends over time.
    *   Pie chart displaying expense distribution by category.
    *   AI-powered financial summary and actionable tips based on your financial data.
*   **Expense Tracker**:
    *   Easily add new expenses with descriptions, amounts, and dates.
    *   Automatic categorization of expenses using Groq's AI model.
    *   View and manage a list of all recorded expenses.
    *   Option to delete existing expenses.
*   **Income Manager**:
    *   Record various sources of income with descriptions, amounts, and dates.
    *   View and manage a list of all recorded incomes.
    *   Option to delete existing incomes.
*   **Savings Goal Planner**:
    *   Set financial goals by specifying a product name, target price, and target date.
    *   Calculates the monthly saving needed to achieve the goal.
    *   Tracks progress towards each savings goal.
    *   Option to delete savings goals.
*   **AI Financial Advisor**:
    *   An interactive chat interface where users can ask financial questions.
    *   The AI can provide general financial advice or specific insights based on the user's recorded financial data.
*   **Settings**:
    *   Update user profile information (name, preferred currency).
    *   Switch between Light and Dark themes for the application interface.

## Technologies Used

*   **Frontend:** Streamlit
*   **Backend/Database:** Firebase (Firestore for data storage, Authentication for user management)
*   **AI/LLM:** Groq API (for expense categorization and financial advice)
*   **Data Manipulation:** Pandas
*   **Charting:** Altair
*   **Environment Management:** Python, `python-dotenv`

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/finance-manager.git
cd finance-manager
```

### 2. Set up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv finance_venv
# On Windows
.\finance_venv\Scripts\activate
# On macOS/Linux
source finance_venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
*If `requirements.txt` does not exist, you can generate it using `pip freeze > requirements.txt` after installing the necessary packages manually (streamlit, firebase-admin, pyrebase4, groq, pandas, altair, python-dotenv).*

### 4. Firebase Project Setup

1.  **Create a Firebase Project:** Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
2.  **Enable Firestore:** In your Firebase project, navigate to "Firestore Database" and create a new database. Choose "Start in production mode" and select a location.
3.  **Enable Authentication:** Go to "Authentication" and enable "Email/Password" as a sign-in method.
4.  **Generate Service Account Key:**
    *   In the Firebase Console, go to "Project settings" (the gear icon).
    *   Select "Service accounts".
    *   Click "Generate new private key" and then "Generate key". This will download a JSON file (e.g., `your-project-name-firebase-adminsdk-xxxxx-xxxxxx.json`).
    *   **Rename this downloaded JSON file to `firebase_config.json`**.
    *   **Important:** This file contains sensitive credentials. Keep it secure and do not share it publicly.

### 5. Groq API Key Setup

1.  **Get a Groq API Key:** Sign up or log in to [Groq Cloud](https://console.groq.com/) and generate an API key.
2.  **Create a `.env` file:** In the root directory of your project (the same directory as `app.py`), create a file named `.env`.
3.  **Add your Groq API Key:** Open the `.env` file and add your Groq API key in the following format:

    ```
    GROQ_API_KEY="YOUR_GROQ_API_KEY"
    ```
    Replace `