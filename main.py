import os
import streamlit as st
from streamlit import session_state as ss
from controller.app_controller import AppController
from dotenv import load_dotenv, find_dotenv


def main():
    load_dotenv(find_dotenv())
    st.set_page_config(page_title="AI Resume Builder", page_icon=":robot:", layout="wide")
    app_controller = AppController(app_env = os.getenv("APP_ENV"))
    if "resume_input" not in ss:
        app_controller.handle_ingest_screen()
    else:
        app_controller.handle_preview_screen()

if __name__ == "__main__":
    main()