import feedparser
import datetime
from slacker import Slacker
import json
import os
import settings
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('--dryrun', action='store_true', default=False)
args = parser.parse_args()


RSS_BASE_URL = "https://www.machine-learning.news/rss"

search_to = datetime.datetime.now()
search_from = datetime.datetime.now()
search_from = search_from.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=settings.SEARCH_SCOPE * -1)

print(search_from, '-', search_to)

# Read history
if os.path.exists(settings.HISTORY_FILE):
    history = json.load(open(settings.HISTORY_FILE, "r"))
else:
    history = []
history_links = [x[0] for x in history]
temp_links = []


# Fetch articles
latest_entries = []
for cat in settings.CATEGORIES:
    rss_url = f"{RSS_BASE_URL}?listName={cat}"
    d = feedparser.parse(rss_url)

    for entry in d.entries:
        published = datetime.datetime(*entry.published_parsed[:6])
        if entry.link in history_links or entry.link in temp_links:
            continue
        if published >= search_from and published < search_to:
            latest_entries.append(entry)
            history.append((entry.link, entry.published_parsed[:3]))
            temp_links.append(entry.link)

print(f'Found {len(latest_entries)} articles')


slack = Slacker(token=settings.SLACK_TOKEN)
for n in range(0, len(latest_entries), settings.N_ENTRIES_PER_POST):
    msg = ""
    for entry in latest_entries[n:n+settings.N_ENTRIES_PER_POST]:
        msg += "■■■■  "
        msg += f"{entry.title}"
        msg += "\n"
        msg += f"{entry.link}\n"
        if entry.summary:
            msg += f"{entry.summary}\n\n"
        else:
            msg += "\n"
    if args.dryrun:
        print(msg)
    else:
        slack.chat.post_message(channel=settings.SLACK_CHANNEL, username=settings.SLACK_BOT_NAME,
                               text="```" + msg + "```")

# Expire old items
history = [(link, date) for link,date in history if datetime.datetime(*date) + datetime.timedelta(days=settings.EXPIRE_DAYS) > search_to]

if not args.dryrun:
    # Update histories
    with open(settings.HISTORY_FILE, "w") as f:
        json.dump(history, f)

print(f'Finished: {len(latest_entries)} articles')

