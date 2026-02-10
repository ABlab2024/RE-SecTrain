import streamlit as st
import time
from utils.data_manager import DataManager
from utils.llm_client import LLMClient
from utils.email_sender import send_email
import streamlit.components.v1 as components
import uuid
import os
import urllib.parse

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
    # Log the click if tracking_id is present
    print(f"DEBUG: Processing Click - Params: {query_params}")
    tracking_id = query_params.get("tracking_id", None)
    interest_param = query_params.get("interest", None)
    
    if tracking_id:
        if dm.log_click(tracking_id):
            st.toast("Click recorded in your training history.", icon="📝")

    # Load and display the static warning page
    try:
        with open("phishing_training_page/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        with open("phishing_training_page/style.css", "r", encoding="utf-8") as f:
            css_content = f.read()
            
        # Load the vulnerability report if available
        report_content = "<h3>Report Not Found</h3><p>Could not load or generate the vulnerability report.</p>"
        
        # Try to load from file first
        if tracking_id and os.path.exists(f"phishing_training_page/reports/{tracking_id}.html"):
            try:
                with open(f"phishing_training_page/reports/{tracking_id}.html", "r", encoding="utf-8") as f:
                    report_content = f.read()
            except Exception as e:
                print(f"Error reading report file: {e}")
        
        # Fallback: Generate report if interest/topic is available in params
        elif interest_param:
            try:
                # Need to initialize LLM client here if not already initialized (it is initialized later in the script) 
                # Since this block is at the top, we need to init LLM temporarily or refactor.
                # However, to keep it simple, we assume the user has logged in and API key is in session state or secrets.
                # But wait, LLM client initialization requires API key which is in sidebar.
                # The sidebar code runs AFTER this block. 
                # We need to move LLM initialization earlier or duplicate it.
                # Let's try to get API key from session state if available or proceed without report if not.
                
                # Check for API key in session state or secrets
                api_key = st.session_state.get("api_key") or st.secrets.get("GEMINI_API_KEY") 
                # Note: Currently API key is in a local variable in sidebar, so session_state might not have it yet on first load if not persisted.
                # However, for the fallback, we need the LLM client.
                
                # Simplest fix: Just display a message if we can't generate it yet, or try best effort.
                if api_key:
                     driver_map = {"GEMINI": "google", "GPT": "openai", "CLAUDE": "anthropic"}
                     # Default to google/gemini if not specified
                     llm_provider = st.session_state.get("llm_provider", "GEMINI")
                     temp_llm_client = LLMClient(provider=driver_map.get(llm_provider, "google"), api_key=api_key)
                     report_content = temp_llm_client.generate_vulnerability_report(urllib.parse.unquote(interest_param))
                else: 
                     report_content = f"<h3>Report Pending</h3><p>Please login to the main dashboard to view the full report on '{interest_param}'.</p>"
            except Exception as e:
                report_content = f"<p>Error generating report: {str(e)}</p>"

        # Inject report into HTML
        html_content = html_content.replace("{{THREAT_REPORT}}", report_content)

        # Combine HTML and CSS
        full_html = f"<style>{css_content}</style>{html_content}"
        
        # Render the static page
        # Using height=1000 to ensure it covers most screens, scrolling allowed
        st.components.v1.html(full_html, height=1000, scrolling=True)
        
    except FileNotFoundError:
        st.error("Training page files not found. Please check 'phishing_training_page' directory.")
        
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
    llm_provider = st.selectbox("LLM Provider", ["GEMINI", "GPT", "CLAUDE"])
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
    driver_map = {"GEMINI": "google", "GPT": "openai", "CLAUDE": "anthropic"}
    try:
        llm_client = LLMClient(provider=driver_map.get(llm_provider, "google"), api_key=api_key)
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
                    base_url = "https://simulwarning.netlify.app"
                    
                    encoded_interest = urllib.parse.quote(interest)
                    tracking_link = f"{base_url}/?clicked=true&tracking_id={tracking_id}&interest={encoded_interest}"
                    
                    # Generate and save vulnerability report
                    try:
                        status_text.text("📝 Generating vulnerability report...")
                        report_content = llm_client.generate_vulnerability_report(interest)
                        
                        # Ensure directory exists
                        os.makedirs("phishing_training_page/reports", exist_ok=True)
                        
                        with open(f"phishing_training_page/reports/{tracking_id}.html", "w", encoding="utf-8") as f:
                            f.write(report_content)
                            
                    except Exception as e:
                        st.warning(f"Failed to generate report: {e}")

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
