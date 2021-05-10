import os

# CATEGORIES = ["general", "japanese", "article", "twitter", "github", "arxiv", "kaggle", "slide", "video", "event"]
CATEGORIES = ["japanese", "article", "slide", "event"]
SEARCH_SCOPE = 2  # 何日前まで検索するか
HISTORY_FILE = "history_db.json"
N_ENTRIES_PER_POST = 8
EXPIRE_DAYS = 30
assert EXPIRE_DAYS >= SEARCH_SCOPE
SLACK_TOKEN = os.environ["ML_NEWS_CHECKER_SLACK_TOKEN"]
SLACK_CHANNEL = os.environ["ML_NEWS_CHECKER_SLACK_CHANNEL"]
SLACK_BOT_NAME = "ml_news_checker"
