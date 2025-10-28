# 💰 Finance Manager 📊

## Live Application for use - ## 
https://a-finance-manager.streamlit.app/ - It is deployed, may take some time to wake up but will surely work broski

Welcome to the **Finance Manager**! 🎉 This application helps you effortlessly track your income and expenses, giving you a clear overview of your financial health. 📈 Say goodbye to financial stress and hello to smart money management! 🚀

## ✨ Features

*   **Income Tracking:** Easily record all your sources of income. 💸
*   **Expense Management:** Categorize and log your daily expenditures. 🧾
*   **Real-time Dashboard:** Visualize your financial data with intuitive charts and graphs. 📊
*   **User Authentication:** Securely manage your financial data with user accounts. 🔒
*   **Cloud Storage:** Your data is safely stored in the cloud (Firebase Firestore). ☁️
*   **AI Financial Advisor:** Get personalized financial insights and tips powered by Groq AI. 🤖
*   **Savings Goal Planner:** Set and track your savings goals. 🎯

## 🛠️ Technologies Used

*   **Frontend/Backend Framework:** Streamlit 🚀 (Python-based web framework)
*   **Database/Authentication:** Google Firebase (Firestore & Authentication) 🔥
*   **AI Integration:** Groq API (for AI Financial Advisor and expense categorization) 🧠
*   **Data Handling:** Pandas 🐼
*   **Charting:** Altair 📈
*   **Styling:** Custom CSS 🎨

## 🚀 Getting Started

Follow these steps to get your Finance Manager up and running!

### Prerequisites

*   Python 3.x installed 🐍
*   `pip` (Python package installer) 📦
*   A Firebase project set up with Web App configuration. You'll need your Firebase API key, Auth Domain, Project ID, Storage Bucket, Messaging Sender ID, and App ID.
*   A Groq API Key.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/finance-manager.git
    cd finance-manager
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv finance_venv
    ```

3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        .\finance_venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source finance_venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables:**
    *   Create a `.env` file in the project root directory.
    *   Add your Groq API key to this file:
        ```
        GROQ_API_KEY="YOUR_GROQ_API_KEY"
        ```
    *   For Firebase configuration, Streamlit expects secrets to be in a `.streamlit/secrets.toml` file. Create this file and add your Firebase configuration:
        ```toml
        # .streamlit/secrets.toml
        [firebase]
        apiKey = "YOUR_API_KEY"
        authDomain = "YOUR_AUTH_DOMAIN"
        projectId = "YOUR_PROJECT_ID"
        storageBucket = "YOUR_STORAGE_BUCKET"
        messagingSenderId = "YOUR_MESSAGING_SENDER_ID"
        appId = "YOUR_APP_ID"
        ```
    *   Alternatively, you can directly modify `app_files/firebase_utils.py` to hardcode your Firebase config, but using `secrets.toml` is recommended for security.

### Running the Application

1.  **Ensure your virtual environment is active.**
2.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

3.  Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`) 🌐

## 📝 Usage

1.  **Register/Login:** Create a new account or log in with your existing credentials. 👤
2.  **Add Income:** Navigate to the income section and add your earnings. ➕💰
3.  **Add Expense:** Go to the expense section and record your spending, categorizing it appropriately (AI-powered categorization!). ➖💸
4.  **View Dashboard:** Check your dashboard for a quick overview of your financial status, including trends and expense distribution. 📈
5.  **Set Savings Goals:** Plan and track your savings for specific items or events. 🎯
6.  **Chat with AI Advisor:** Ask your AI Financial Advisor questions and get personalized advice. 🤖

## 🔄 Workflow Diagram

Here's a simplified text-based workflow of how the Finance Manager operates:

```
+-------------------+       +-----------------------+       +-------------------+       +-------------------+
|     User (Browser)  |       |   Streamlit Application   |       |      Firebase       |       |       Groq API      |
+---------+---------+       +-----------+-----------+       +---------+---------+       +---------+---------+
          |                               |                               |                               |
          | 1. Access App (streamlit run) |                               |                               |
          |------------------------------>|                               |                               |
          |                               |                               |                               |
          | 2. Register/Login Request     |                               |                               |
          | (via Streamlit UI)            |                               |                               |
          |------------------------------>| 3. Authenticate User          |                               |
          |                               |------------------------------>|                               |
          |                               |                               | 4. Auth Response              |
          |                               |<------------------------------|                               |
          |                               |                               |                               |
          | 5. Session Management         |                               |                               |
          |<------------------------------|                               |                               |
          |                               |                               |                               |
          | 6. Add Income/Expense         |                               |                               |
          | (via Streamlit UI)            |                               |                               |
          |------------------------------>| 7. Categorize Expense (AI)    |                               |
          |                               |-------------------------------------------------------------->|
          |                               |                               |                               | 8. Category/Advice    |
          |                               |<--------------------------------------------------------------|
          |                               | 9. Store Data (Firestore)     |                               |
          |                               |------------------------------>|                               |
          |                               |                               | 10. Data Stored               |
          |                               |<------------------------------|                               |
          |                               |                               |                               |
          | 11. View Data Request         |                               |                               |
          | (Dashboard, Income, Expenses) |                               |                               |
          |------------------------------>| 12. Fetch Data (Firestore)    |                               |
          |                               |------------------------------>|                               |
          |                               |                               | 13. Data Retrieved            |
          |                               |<------------------------------|                               |
          |                               |                               |                               |
          | 14. Display Data/Insights     |                               |                               |
          |<------------------------------|                               |                               |
          |                               |                               |                               |
          | 15. AI Advisor Query          |                               |                               |
          |------------------------------>| 16. Process Query (AI)        |                               |
          |                               |-------------------------------------------------------------->|
          |                               |                               |                               | 17. AI Response       |
          |                               |<--------------------------------------------------------------|
          |                               |                               |                               |
+---------+---------+       +-----------+-----------+       +---------+---------+       +---------+---------+
```

## 🤝 Contributing

We welcome contributions! If you have suggestions, bug reports, or want to add new features, please feel free to:

1.  Fork the repository. 🍴
2.  Create a new branch (`git checkout -b feature/YourFeature`). 🌿
3.  Make your changes. 💻
4.  Commit your changes (`git commit -m 'Add some feature'`). ✅
5.  Push to the branch (`git push origin feature/YourFeature`). ⬆️
6.  Open a Pull Request. 📥