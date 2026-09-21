from database.db_manager import DBManager
class BotModel:
    def __init__(self): self.db = DBManager()

    def get_bot_settings(self):
        # 0: fb_page, 1: fb_verify, 2: ig_page, 3: ig_verify
        return self.db._execute(
            "SELECT fb_page_token, fb_verify_token, ig_page_token, ig_verify_token FROM bot_settings WHERE id=1",
            fetch=True, fetch_one=True)
