import os
import streamlit as st
from view import *
from utils.airtable import initialize_airtable_client


class AppController:
    def __init__(self, app_env: str):
        self.current_screen = "ingest"
        self.app_env = app_env
        self.title = f"Resume Builder - {self.app_env.capitalize()}" if self.app_env == "dev" else "Resume Builder"
        st.title(self.title)
        
        # On Start, Depdency inject to relevant services
        self.api_key = os.getenv('AIRTABLE_API_KEY')
        self.airtable_client = initialize_airtable_client(self.api_key)
    
    def handle_ingest_screen(self):
        ingest_screen(self.app_env)
    
    def handle_preview_screen(self):
        preview_screen(self.app_env, self.airtable_client)