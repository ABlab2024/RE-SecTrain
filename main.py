import streamlit as st
import time
from utils.data_manager import DataManager
from utils.llm_client import LLMClient
from utils.email_sender import send_email
import uuid

# Page Config
st.set_page_config(
    page_title="Security Vibe - AI Security Training",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Data Manager
dm = DataManager()

# --- 1. Click Detection Logic (Must be at the top) ---
# Check if the user arrived via a phishing link
query_params = st.query_params
if "clicked" in query_params and query_params["clicked"] == "true":
    st.error("🚨 Security Alert! You clicked a simulated phishing link.")
    
    # Log the click if tracking_id is present
    tracking_id = query_params.get("tracking_id", None)
    if tracking_id:
        if dm.log_click(tracking_id):
            st.toast("Click recorded in your training history.", icon="📝")
    
    st.markdown("""
    ### 🛑 This was a simulation.
    If this were a real attack, your device could have been compromised.
    
    **What to look for:**
    - Check the sender's email address carefully.
    - Hover over links before clicking to see the actual URL.
    - Be wary of urgent or threatening language.
    """)
    
    if st.button("Return to Dashboard"):
        st.query_params.clear()
        st.rerun()
    
    st.image("assets/warning_image.png", caption="Phishing Warning") 
    st.stop() # Stop execution of the main app

# --- 2. Sidebar & Configuration ---
with st.sidebar:
    st.title("🛡️ Security Vibe")
    
    # User Login (Simple)
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = ""
    
    email_input = st.text_input("Login (Email)", value=st.session_state["user_email"])
    if email_input:
        st.session_state["user_email"] = email_input
    
    st.divider()
    
    # LLM Settings
    st.subheader("⚙️ AI Settings")
    llm_provider = st.selectbox("LLM Provider", ["google", "openai", "anthropic"])
    api_key = st.text_input("API Key", type="password")
    
    st.divider()
    st.info(f"Logged in as: {st.session_state['user_email']}" if st.session_state['user_email'] else "Please login first.")

# --- 3. Main Dashboard ---

if not st.session_state["user_email"]:
    st.warning("Please enter your email in the sidebar to access the dashboard.")
    st.stop()

if not api_key:
    st.warning("Please enter a valid API Key for the selected provider.")
    # Allow proceeding for demo purposes if needed, but core features wont work
else:
    # Initialize LLM Client
    try:
        llm_client = LLMClient(provider=llm_provider, api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize LLM: {str(e)}")
        st.stop()

# Layout
st.title(f"Welcome, {st.session_state['user_email'].split('@')[0]} 👋")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🚀 New Simulation", "📜 History"])

# --- Tab 1: Dashboard (News & Reports) ---
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📰 Daily Security Briefing")
        if st.button("Refresh News"):
            with st.spinner("Searching for latest threats..."):
                # Using 'General Security' as default interest for news
                news_summary = llm_client.search_security_issues("General Security Trends")
                st.session_state['news_cache'] = news_summary
        
        if 'news_cache' in st.session_state:
            st.success("Analysis Complete")
            st.markdown(st.session_state['news_cache'])
        else:
            st.info("Click 'Refresh News' to see the latest security updates.")

    with col2:
        st.subheader("🛡️ Vulnerability Report")
        report = dm.get_report()
        if not report:
            st.write("No vulnerability data yet. Good job!")
        else:
            st.write("⚠️ Areas for improvement:")
            st.json(report)
            st.metric("Total Clicks", sum(report.values()))

# --- Tab 2: New Simulation ---
with tab2:
    st.subheader("Launch Phishing Simulation")
    
    with st.form("simulation_form"):
        interest = st.selectbox("Select Target Interest/Topic", 
                                ["Shopping", "Finance", "Internal Announcement", "Travel", "Government"])
        target_email = st.text_input("Target Email", value=st.session_state["user_email"])
        
        submitted = st.form_submit_button("Generate & Send")
        
        if submitted:
            if not target_email:
                st.error("Target email is required.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Search relevant info
                status_text.text("🔍 Searching for relevant threat vectors...")
                threat_info = llm_client.search_security_issues(interest)
                progress_bar.progress(30)
                
                # Step 2: Generate Content
                status_text.text("🤖 Generating phishing scenario...")
                scenario = llm_client.generate_phishing_scenario(threat_info) 
                # Expecting scenario to be a dict/json
                progress_bar.progress(60)
                
                if isinstance(scenario, dict) and "subject" in scenario and "body" in scenario:
                    # Step 3: Send Email
                    status_text.text("📧 Sending email...")
                    tracking_id = str(uuid.uuid4())
                    
                    # Construct tracking link - configurable via secrets.toml for deployment
                    # In Streamlit Cloud, add BASE_URL = "https://your-app.streamlit.app" to secrets
                    base_url = "http://localhost:8501"
                    if "BASE_URL" in st.secrets:
                        base_url = st.secrets["BASE_URL"]
                    
                    tracking_link = f"{base_url}/?clicked=true&tracking_id={tracking_id}"
                    
                    success, msg = send_email(target_email, scenario['subject'], scenario['body'], tracking_link)
                    
                    if success:
                        dm.log_training(target_email, interest, interest, tracking_id)
                        progress_bar.progress(100)
                        status_text.text("✅ Simulation Sent!")
                        st.success(f"Email sent to {target_email}")
                        st.expander("Show Generated Content (Debug)").json(scenario)
                    else:
                        st.error(f"Failed to send email: {msg}")
                else:
                    st.error("Failed to generate valid scenario content.")
                    st.write(scenario) # Debug output

# --- Tab 3: History ---
with tab3:
    st.subheader("Training History")
    history_df = dm.get_history(st.session_state["user_email"])
    
    if history_df.empty:
        st.info("No training history found.")
    else:
        st.dataframe(
            history_df,
            column_config={
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Sent", "Clicked"],
                    disabled=True,
                )
            },
            hide_index=True,
            use_container_width=True
        )
