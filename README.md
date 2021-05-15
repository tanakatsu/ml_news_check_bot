# ml_news_checker_bot

### What is this?

This is a script that fetchs ML-News (https://www.machine-learning.news/list/general)'s latest articles and notifies them to your slack channel.

### Required packages
- feedbarser
- slacker

You can install these packages by `pip install -r requirements.txt`.

### How to use

1. Set environment variables
    - Edit `setenv.sample.sh`
      - your SLACK_TOKEN and the channel name which you want to send messages
    - Run `source setenv.sample.sh`
1. Just run `python ml_news_bot.py`

That's it. No sweat.
