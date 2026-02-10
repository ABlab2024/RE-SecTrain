import streamlit as st
import pandas as pd
from datetime import datetime

class DataManager:
    """
    Manages user data and training history using Streamlit's session state.
    Since no database is used, data persists only for the session duration.
    """
    def __init__(self):
        if 'user_history' not in st.session_state:
            st.session_state['user_history'] = pd.DataFrame(columns=[
                'timestamp', 'email', 'interest', 'scenario_type', 'status', 'tracking_id'
            ])
        
        if 'vulnerability_report' not in st.session_state:
            st.session_state['vulnerability_report'] = {}

    def log_training(self, email, interest, scenario_type, tracking_id):
        """
        Logs a new training scenario dispatch.
        """
        new_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'email': email,
            'interest': interest,
            'scenario_type': scenario_type,
            'status': 'Sent',
            'tracking_id': tracking_id
        }
        user_history = st.session_state['user_history']
        st.session_state['user_history'] = pd.concat([user_history, pd.DataFrame([new_entry])], ignore_index=True)

    def log_click(self, tracking_id):
        """
        Updates the status of a training scenario to 'Clicked' if detected.
        """
        if 'user_history' in st.session_state:
            df = st.session_state['user_history']
            if not df.empty and tracking_id in df['tracking_id'].values:
                idx = df[df['tracking_id'] == tracking_id].index[0]
                st.session_state['user_history'].at[idx, 'status'] = 'Clicked'
                
                # Update vulnerability report
                scenario_type = df.at[idx, 'scenario_type']
                self._update_vulnerability_report(scenario_type)
                return True
        return False

    def _update_vulnerability_report(self, scenario_type):
        """
        Updates the count of clicked scenarios by type.
        """
        report = st.session_state['vulnerability_report']
        if scenario_type in report:
            report[scenario_type] += 1
        else:
            report[scenario_type] = 1
        st.session_state['vulnerability_report'] = report

    def get_history(self, email=None):
        """
        Returns the training history DataFrame, optionally filtered by email.
        """
        df = st.session_state.get('user_history', pd.DataFrame())
        if email and not df.empty:
            return df[df['email'] == email]
        return df

    def get_report(self):
        """
        Returns the vulnerability report dictionary.
        """
        return st.session_state.get('vulnerability_report', {})
