import streamlit as st
from streamlit import session_state as ss
from controller.app_controller import AppController

def main():
    st.title("Virtual Vocation Venture")
    app_controller = AppController()
    if "resume_input" not in ss:
        app_controller.handle_ingest_screen()
    else:
        app_controller.handle_preview_screen()

if __name__ == "__main__":
    main()