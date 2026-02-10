import streamlit as st
import pandas as pd
from datetime import datetime
import os

HISTORY_FILE = "user_history.csv"

class DataManager:
    """
    Manages user data and training history using a CSV file.
    This allows data to be shared across different sessions (e.g. Admin sending vs Victim clicking).
    Note: In Streamlit Cloud, this file is ephemeral and will reset on app reboot.
    For permanent storage, use a database like Supabase or Google Sheets.
    """
    def __init__(self):
        # Initialize file if not exists
        if not os.path.exists(HISTORY_FILE):
            df = pd.DataFrame(columns=[
                'timestamp', 'email', 'interest', 'scenario_type', 'status', 'tracking_id'
            ])
            df.to_csv(HISTORY_FILE, index=False)
            
    def _load_data(self):
        try:
            return pd.read_csv(HISTORY_FILE)
        except Exception:
            return pd.DataFrame(columns=[
                'timestamp', 'email', 'interest', 'scenario_type', 'status', 'tracking_id'
            ])

    def _save_data(self, df):
        df.to_csv(HISTORY_FILE, index=False)

    def log_training(self, email, interest, scenario_type, tracking_id):
        """
        Logs a new training scenario dispatch.
        """
        df = self._load_data()
        new_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'email': email,
            'interest': interest,
            'scenario_type': scenario_type,
            'status': 'Sent',
            'tracking_id': tracking_id
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        self._save_data(df)

    def log_click(self, tracking_id):
        """
        Updates the status of a training scenario to 'Clicked' if detected.
        """
        df = self._load_data()
        if not df.empty and tracking_id in df['tracking_id'].values:
            idx = df[df['tracking_id'] == tracking_id].index[0]
            # Only update if not already clicked to preserve first click time if we processed time
            if df.at[idx, 'status'] != 'Clicked':
                df.at[idx, 'status'] = 'Clicked'
                self._save_data(df)
                return True
        return False

    def get_history(self, email=None):
        """
        Returns the training history DataFrame, optionally filtered by email.
        """
        df = self._load_data()
        if email and not df.empty:
            # Simple string matching for now
            return df[df['email'] == email]
        return df

    def get_report(self):
        """
        Returns the vulnerability report dictionary (aggregated from CSV).
        """
        df = self._load_data()
        if df.empty:
            return {}
        # Count clicks by scenario type
        clicked = df[df['status'] == 'Clicked']
        if clicked.empty:
            return {}
        return clicked['scenario_type'].value_counts().to_dict()
