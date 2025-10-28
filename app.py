
import streamlit as st
import os
from groq import Groq
from app_files.firebase_utils import initialize_firebase, get_firestore_db, initialize_pyrebase
from firebase_admin import firestore
import pandas as pd
import altair as alt
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for styling ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("app_files/style.css") 

# --- Firebase and Groq Initialization ---
@st.cache_resource
def init_connections():
    """
    Initializes Firebase and the Groq client.
    Caches the connections for performance.
    """
    try:
        # Check for Firebase config in secrets
        if "firebase" not in st.secrets:
            st.error("Firebase configuration not found in Streamlit secrets! Please add your Firebase config to `secrets.toml`.")
            st.stop()
        firebase_config = st.secrets["firebase"]

        # Check for Groq API key
        groq_api_key = os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            st.error("GROQ_API_KEY not found! Please create a `.env` file in the project root and add `GROQ_API_KEY=\"YOUR_API_KEY\"`.")
            st.stop()

        initialize_firebase(firebase_config)
        db = get_firestore_db()
        auth = initialize_pyrebase(firebase_config)
        groq_client = Groq(api_key=groq_api_key)
        return db, auth, groq_client
    except Exception as e:
        st.error(f"An error occurred during initialization: {e}")
        st.stop()

db, auth, groq_client = init_connections()

# --- Main App ---
def main():
    """
    Main function to run the Streamlit app.
    """
    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        app()
    else:
        login_signup()

def login_signup():
    """
    Handles the login and signup pages.
    """
    st.markdown("<h1 style='text-align: center; color: var(--primary-color);'>Welcome to your AI-Powered Finance Manager 💰</h1>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: var(--text-color);'>Login or Sign Up to manage your finances.</p>", unsafe_allow_html=True)

    security_disclaimer = """
    <div class="security-disclaimer">
        <h3>Your Security, Our Priority</h3>
        <p>Your privacy and data security are paramount. On our login and signup pages, all information you submit is protected with industry-standard encryption protocols (SSL/TLS) to ensure secure transmission. We utilize robust authentication mechanisms to safeguard your account from unauthorized access. Your personal data is stored securely, with access restricted to authorized personnel only, and is never shared with third parties without your explicit consent. We are committed to maintaining the highest standards of data protection to keep your information safe and private.</p>
    </div>
    """
    st.markdown(security_disclaimer, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container(border=True):
            choice = st.radio("", ["Login", "Sign Up"], label_visibility="hidden", horizontal=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if choice == "Login":
                st.markdown("<h3 style='text-align: center; color: var(--text-color);'>Login</h3>", unsafe_allow_html=True)
                email = st.text_input("✉️ Email", placeholder="Enter your email")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                if st.button("Login", use_container_width=True, type="primary"):
                    try:
                        user = auth.sign_in_with_email_and_password(email, password)
                        st.session_state.user = user
                        st.rerun()
                    except Exception as e:
                        st.error(f"Login failed: {e}")

            else:
                st.markdown("<h3 style='text-align: center; color: var(--text-color);'>Sign Up</h3>", unsafe_allow_html=True)
                email = st.text_input("✉️ Email", placeholder="Enter your email")
                password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
                if st.button("Sign Up", use_container_width=True, type="primary"):
                    try:
                        user = auth.create_user_with_email_and_password(email, password)
                        st.session_state.user = user
                        # Create user profile in Firestore
                        user_ref = db.collection('users').document(user['localId'])
                        user_ref.set({
                            "email": email,
                            "created_at": firestore.SERVER_TIMESTAMP,
                            "theme": "Light" # Default theme
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"Signup failed: {e}")

def app():
    """
    The main application logic after the user has logged in.
    """
    user_id = st.session_state.user['localId']
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    user_data = user_doc.to_dict()

    # Apply theme
    if user_data and 'theme' in user_data:
        st.markdown(f"<body class='{user_data['theme'].lower()}-theme'>", unsafe_allow_html=True)

    st.sidebar.title(f"Welcome, {user_data.get('email', '')}!")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    # --- Sidebar Navigation ---
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("", ["📊 Dashboard", "💸 Expense Tracker", "💰 Income Manager", "🎯 Savings Goal Planner", "🤖 AI Financial Advisor", "⚙️ Settings"], label_visibility="hidden")


    # --- Page Routing ---
    if page == "📊 Dashboard":
        st.markdown("<h1 style='color: var(--text-color);'>📊 Dashboard</h1>", unsafe_allow_html=True)
        
        if st.button("Refresh Data", type="secondary"):
            st.cache_resource.clear()
            st.rerun()
        st.markdown("--- ")

        # Fetch data
        incomes_ref = db.collection('incomes').where('user_id', '==', user_id).stream()
        expenses_ref = db.collection('expenses').where('user_id', '==', user_id).stream()

        incomes = [income.to_dict() for income in incomes_ref]
        expenses = [expense.to_dict() for expense in expenses_ref]

        # Calculate metrics
        total_income = sum([income['amount'] for income in incomes])
        total_expenses = sum([expense['amount'] for expense in expenses])
        net_income = total_income - total_expenses

        st.markdown("<h3 style='color: var(--text-color);'>Overview</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Income", f"{user_data.get('currency', '$')} {total_income:.2f}", delta_color="normal")
        with col2:
            st.metric("Total Expenses", f"{user_data.get('currency', '$')} {total_expenses:.2f}", delta_color="inverse")
        with col3:
            st.metric("Net Income", f"{user_data.get('currency', '$')} {net_income:.2f}", delta_color="normal")
        
        st.markdown("--- ")

        # Trend chart
        if incomes or expenses:
            if incomes:
                income_df = pd.DataFrame(incomes)
                income_df['date'] = pd.to_datetime(income_df['date'])
                income_df = income_df.set_index('date').resample('M')['amount'].sum().reset_index()
                income_df['type'] = 'Income'
            else:
                income_df = pd.DataFrame()

            if expenses:
                expense_df = pd.DataFrame(expenses)
                expense_df['date'] = pd.to_datetime(expense_df['date'])
                expense_df = expense_df.set_index('date').resample('M')['amount'].sum().reset_index()
                expense_df['type'] = 'Expense'
            else:
                expense_df = pd.DataFrame()

            trend_df = pd.concat([income_df, expense_df])

            st.markdown("<h3 style='color: var(--text-color);'>Income vs. Expense Trend</h3>", unsafe_allow_html=True)
            st.altair_chart(alt.Chart(trend_df).mark_line().encode(
                x=alt.X('date:T', title='Date'),
                y=alt.Y('amount:Q', title='Amount'),
                color=alt.Color('type:N', legend=alt.Legend(title="Type"))
            ).properties(
                title="Monthly Income and Expense Trend"
            ).interactive(), use_container_width=True)

        # Expense distribution
        if expenses:
            expense_df = pd.DataFrame(expenses)
            expense_by_category = expense_df.groupby('category')['amount'].sum().reset_index()

            st.markdown("<h3 style='color: var(--text-color);'>Expense Distribution</h3>", unsafe_allow_html=True)
            st.altair_chart(alt.Chart(expense_by_category).mark_arc().encode(
                theta=alt.Theta(field="amount", type="quantitative"),
                color=alt.Color(field="category", type="nominal", title="Category")
            ).properties(
                title="Expense Distribution by Category"
            ), use_container_width=True)

        # AI-powered insights
        if total_income > 0 or total_expenses > 0:
            st.markdown("<h3 style='color: var(--text-color);'>AI Financial Summary</h3>", unsafe_allow_html=True)
            with st.container(border=True):
                with st.spinner("Generating summary..."):
                    messages = [
                        {
                            "role": "user",
                            "content": f"Here is my financial data:\n- Total Income: {total_income}\n- Total Expenses: {total_expenses}\n- Expenses by Category: {expense_by_category.to_dict() if expenses else {}}\n\nProvide a brief summary of my financial health and one actionable tip.",
                        }
                    ]
                    chat_completion = groq_client.chat.completions.create(
                        messages=messages,
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                    )
                    summary = chat_completion.choices[0].message.content
                    st.write(summary)

    elif page == "💸 Expense Tracker":
        st.markdown("<h1 style='color: var(--text-color);'>💸 Expense Tracker</h1>", unsafe_allow_html=True)
        st.markdown("--- ")

        col1, col2 = st.columns([1,2])
        with col1:
            with st.container(border=True):
                st.markdown("<h3 style='color: var(--text-color);'>Add New Expense</h3>", unsafe_allow_html=True)
                with st.form("expense_form", clear_on_submit=True):
                    description = st.text_input("Expense Description:", placeholder="e.g., Groceries, Dinner with friends")
                    amount = st.number_input("Amount:", min_value=0.01, step=0.01, format="%.2f")
                    date = st.date_input("Date:")
                    submitted = st.form_submit_button("Add Expense", type="primary")

                    if submitted:
                        if description and amount and date:
                            # Use Groq to categorize the expense
                            with st.spinner("Categorizing expense..."):
                                prompt = f"Categorize the following expense into one of these categories: Food, Transportation, Entertainment, Utilities, Shopping, Health, Other. Expense: {description}"
                                chat_completion = groq_client.chat.completions.create(
                                    messages=[
                                        {
                                            "role": "user",
                                            "content": prompt,
                                        }
                                    ],
                                model="meta-llama/llama-4-scout-17b-16e-instruct",
                                )
                                category = chat_completion.choices[0].message.content.strip()

                            # Save the expense to Firebase
                            expense_data = {
                                "user_id": user_id,
                                "description": description,
                                "amount": amount,
                                "date": str(date),
                                "category": category,
                                "created_at": firestore.SERVER_TIMESTAMP
                            }
                            db.collection('expenses').add(expense_data)
                            st.success("Expense added successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill out all the fields.")
        with col2:
            with st.container(border=True):
                st.markdown("<h3 style='color: var(--text-color);'>Your Expenses</h3>", unsafe_allow_html=True)
                # Display expenses
                expenses_ref = db.collection('expenses').where('user_id', '==', user_id).order_by('date', direction=firestore.Query.DESCENDING).stream()
                expenses = [{**expense.to_dict(), "id": expense.id} for expense in expenses_ref]

                if expenses:
                    # Create a DataFrame for better display and sorting
                    expenses_df = pd.DataFrame(expenses)
                    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
                    expenses_df = expenses_df.sort_values(by='date', ascending=False).reset_index(drop=True)

                    st.dataframe(expenses_df[['date', 'description', 'category', 'amount']].style.format({'amount': "{:.2f}"}), use_container_width=True)

                    st.markdown("--- ")
                    st.markdown("<h4 style='color: var(--text-color);'>Delete Expense</h4>", unsafe_allow_html=True)
                    expense_to_delete = st.selectbox("Select expense to delete:", options=expenses_df['description'] + " - " + expenses_df['amount'].astype(str) + " - " + expenses_df['date'].dt.strftime('%Y-%m-%d'), index=None)
                    if st.button("Delete Selected Expense", type="secondary"):
                        if expense_to_delete:
                            # Find the ID of the selected expense
                            selected_expense_id = expenses_df[expenses_df.apply(lambda x: x['description'] + " - " + str(x['amount']) + " - " + x['date'].strftime('%Y-%m-%d') == expense_to_delete, axis=1)]['id'].iloc[0]
                            db.collection('expenses').document(selected_expense_id).delete()
                            st.success("Expense deleted successfully!")
                            st.rerun()
                        else:
                            st.warning("Please select an expense to delete.")
                else:
                    st.info("You haven't added any expenses yet.")

    elif page == "💰 Income Manager":
        st.markdown("<h1 style='color: var(--text-color);'>💰 Income Manager</h1>", unsafe_allow_html=True)
        st.markdown("--- ")
        col1, col2 = st.columns([1,2])
        with col1:
            with st.container(border=True):
                st.markdown("<h3 style='color: var(--text-color);'>Add New Income</h3>", unsafe_allow_html=True)
                with st.form("income_form", clear_on_submit=True):
                    description = st.text_input("Income Description:", placeholder="e.g., Salary, Freelance work")
                    amount = st.number_input("Amount:", min_value=0.01, step=0.01, format="%.2f")
                    date = st.date_input("Date:")
                    submitted = st.form_submit_button("Add Income", type="primary")

                    if submitted:
                        if description and amount and date:
                            # Save the income to Firebase
                            income_data = {
                                "user_id": user_id,
                                "description": description,
                                "amount": amount,
                                "date": str(date),
                                "created_at": firestore.SERVER_TIMESTAMP
                            }
                            db.collection('incomes').add(income_data)
                            st.success("Income added successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill out all the fields.")
        with col2:
            with st.container(border=True):
                st.markdown("<h3 style='color: var(--text-color);'>Your Incomes</h3>", unsafe_allow_html=True)
                # Display incomes
                incomes_ref = db.collection('incomes').where('user_id', '==', user_id).order_by('date', direction=firestore.Query.DESCENDING).stream()
                incomes = [{**income.to_dict(), "id": income.id} for income in incomes_ref]

                if incomes:
                    # Create a DataFrame for better display and sorting
                    incomes_df = pd.DataFrame(incomes)
                    incomes_df['date'] = pd.to_datetime(incomes_df['date'])
                    incomes_df = incomes_df.sort_values(by='date', ascending=False).reset_index(drop=True)

                    st.dataframe(incomes_df[['date', 'description', 'amount']].style.format({'amount': "{:.2f}"}), use_container_width=True)

                    st.markdown("--- ")
                    st.markdown("<h4 style='color: var(--text-color);'>Delete Income</h4>", unsafe_allow_html=True)
                    income_to_delete = st.selectbox("Select income to delete:", options=incomes_df['description'] + " - " + incomes_df['amount'].astype(str) + " - " + incomes_df['date'].dt.strftime('%Y-%m-%d'), index=None)
                    if st.button("Delete Selected Income", type="secondary"):
                        if income_to_delete:
                            # Find the ID of the selected income
                            selected_income_id = incomes_df[incomes_df.apply(lambda x: x['description'] + " - " + str(x['amount']) + " - " + x['date'].strftime('%Y-%m-%d') == income_to_delete, axis=1)]['id'].iloc[0]
                            db.collection('incomes').document(selected_income_id).delete()
                            st.success("Income deleted successfully!")
                            st.rerun()
                        else:
                            st.warning("Please select an income to delete.")
                else:
                    st.info("You haven't added any income yet.")

    elif page == "🎯 Savings Goal Planner":
        st.markdown("<h1 style='color: var(--text-color);'>🎯 Savings Goal Planner</h1>", unsafe_allow_html=True)
        st.markdown("--- ")
        col1, col2 = st.columns([1,2])
        with col1:
            with st.container(border=True):
                st.markdown("<h3 style='color: var(--text-color);'>Set New Savings Goal</h3>", unsafe_allow_html=True)
                with st.form("savings_goal_form", clear_on_submit=True):
                    product_name = st.text_input("Product Name:", placeholder="e.g., New Laptop, Vacation")
                    price = st.number_input("Price:", min_value=0.01, step=0.01, format="%.2f")
                    target_date = st.date_input("Target Date:")
                    submitted = st.form_submit_button("Set Goal", type="primary")

                    if submitted:
                        if product_name and price and target_date:
                            today = datetime.now().date()
                            months_to_save = (target_date.year - today.year) * 12 + (target_date.month - today.month)
                            if months_to_save <= 0:
                                st.error("Target date must be in the future.")
                            else:
                                monthly_saving = price / months_to_save
                                goal_data = {
                                    "user_id": user_id,
                                    "product_name": product_name,
                                    "price": price,
                                    "target_date": str(target_date),
                                    "monthly_saving": monthly_saving,
                                    "created_at": firestore.SERVER_TIMESTAMP
                                }
                                db.collection('savings_goals').add(goal_data)
                                st.success("Savings goal set successfully!")
                                st.rerun()
                        else:
                            st.error("Please fill out all the fields.")
        with col2:
            with st.container(border=True):
                st.markdown("<h3 style='color: var(--text-color);'>Your Savings Goals</h3>", unsafe_allow_html=True)
                # Display savings goals
                goals_ref = db.collection('savings_goals').where('user_id', '==', user_id).stream()
                goals = [{**goal.to_dict(), "id": goal.id} for goal in goals_ref]

                if goals:
                    for goal in goals:
                        st.subheader(f"**{goal['product_name']}**")
                        
                        # Calculate progress
                        # Fetch incomes and expenses up to the current date for progress calculation
                        incomes_for_progress_ref = db.collection('incomes').where('user_id', '==', user_id).where('date', '>=', goal['created_at']).stream()
                        expenses_for_progress_ref = db.collection('expenses').where('user_id', '==', user_id).where('date', '>=', goal['created_at']).stream()
                        incomes_for_progress = [i.to_dict() for i in incomes_for_progress_ref]
                        expenses_for_progress = [e.to_dict() for e in expenses_for_progress_ref]

                        total_saved = sum([i['amount'] for i in incomes_for_progress]) - sum([e['amount'] for e in expenses_for_progress])
                        progress = total_saved / goal['price']
                        if progress < 0: progress = 0
                        if progress > 1: progress = 1

                        st.progress(progress)
                        st.info(f"Saved: {user_data.get('currency', '$')} {total_saved:.2f} / {user_data.get('currency', '$')} {goal['price']:.2f}")
                        st.write(f"Target Date: {goal['target_date']}")
                        st.write(f"Monthly Saving Needed: {user_data.get('currency', '$')} {goal['monthly_saving']:.2f}")
                        if st.button("Delete Goal", key=f"del_goal_{goal['id']}", type="secondary"):
                            db.collection('savings_goals').document(goal['id']).delete()
                            st.rerun()
                        st.markdown("--- ")
                else:
                    st.info("You haven't set any savings goals yet.")

    elif page == "🤖 AI Financial Advisor":
        st.markdown("<h1 style='color: var(--text-color);'>🤖 AI Financial Advisor</h1>", unsafe_allow_html=True)
        st.markdown("--- ")

        with st.container(border=True):
            st.markdown("<h3 style='color: var(--text-color);'>Chat with your AI Advisor</h3>", unsafe_allow_html=True)
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # React to user input
            if prompt := st.chat_input("Ask me anything about your finances..."):
                # Display user message in chat message container
                st.chat_message("user").markdown(prompt)
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.spinner("Thinking..."):
                    # Classify the user's query
                    classification_prompt = f"Is the following query general or specific to the user\'s financial data? Respond with only one word: \'general\' or \'specific\'.\n\nQuery: {prompt}"
                    classification_completion = groq_client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": classification_prompt,
                            }
                        ],
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                    )
                    classification = classification_completion.choices[0].message.content.strip().lower()

                    # Generate AI response based on classification
                    system_prompt = "You are a friendly and helpful financial advisor. Your goal is to provide insightful and actionable advice. Be encouraging and supportive."
                    
                    if "specific" in classification:
                        # Get financial context
                        incomes_ref = db.collection('incomes').where('user_id', '==', user_id).stream()
                        expenses_ref = db.collection('expenses').where('user_id', '==', user_id).stream()
                        goals_ref = db.collection('savings_goals').where('user_id', '==', user_id).stream()

                        incomes = [income.to_dict() for income in incomes_ref]
                        expenses = [expense.to_dict() for expense in expenses_ref]
                        goals = [goal.to_dict() for goal in goals_ref]

                        financial_context = f"Here is the user's financial data:\n- Incomes: {incomes}\n- Expenses: {expenses}\n- Savings Goals: {goals}"
                        full_prompt = f"{system_prompt}\n\n{financial_context}\n\nUser question: {prompt}"
                    else:
                        full_prompt = f"{system_prompt}\n\nUser question: {prompt}"

                    chat_completion = groq_client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": full_prompt,
                            }
                        ],
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                    )
                    response = chat_completion.choices[0].message.content

                    # Display assistant response in chat message container
                    with st.chat_message("assistant"):
                        st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    elif page == "⚙️ Settings":
        st.markdown("<h1 style='color: var(--text-color);'>⚙️ Settings</h1>", unsafe_allow_html=True)
        st.markdown("--- ")

        with st.container(border=True):
            st.markdown("<h3 style='color: var(--text-color);'>User Profile</h3>", unsafe_allow_html=True)
            with st.form("settings_form"):
                name = st.text_input("Name", value=user_data.get('name', ''), placeholder="Enter your name")
                currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR"], index=["USD", "EUR", "GBP", "INR"].index(user_data.get('currency', 'USD')))
                theme = st.selectbox("Theme", ["Light", "Dark"], index=["Light", "Dark"].index(user_data.get('theme', 'Light')))
                submitted = st.form_submit_button("Save Settings", type="primary")

                if submitted:
                    user_ref.update({
                        "name": name,
                        "currency": currency,
                        "theme": theme
                    })
                    st.success("Settings updated successfully!")
                    st.rerun()
if __name__ == '__main__':
    main()
