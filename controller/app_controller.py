from schemas import ResumeInput
from view.ingest_screen import ingest_screen, preview_screen


class AppController:
    def __init__(self):
        self.current_screen = "ingest"
    
    def handle_ingest_screen(self):
        ingest_screen()
    
    def handle_preview_screen(self):
        preview_screen()