from view import *
import streamlit as st


class AppController:
    def __init__(self, app_env: str):
        self.current_screen = "ingest"
        self.app_env = app_env
        self.title = f"Resume Builder - {self.app_env.capitalize()}" if self.app_env == "dev" else "Resume Builder"
        st.title(self.title)
    
    def handle_ingest_screen(self):
        ingest_screen(self.app_env)
    
    def handle_preview_screen(self):
        preview_screen(self.app_env)