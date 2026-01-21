# Twitter Trading Content Generator - SERVERLESS VERSION
# No file I/O - generates posts in memory only
import os
import time
import json
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

class TwitterContentGenerator:
    def __init__(self, api_key=None):
        """Initialize Twitter Trading Content Generator for serverless"""
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Please set DEEPSEEK_API_KEY")

        # 5 prompts optimized for Vercel timeout
        self.prompts = [
            "Create a short philosophical post about trading psychology. Format: '[Bold statement about trading]. [Elaboration in 1-2 sentences]. [Ending that drives it home].' Keep it under 50 words. Make it profound about the mental game of trading.",

            "Write a post contrasting what traders want vs what they need. Format: 'Most traders want [X], but not [Y]. And that is why they fail.' Keep it SHORT - 2 lines maximum, under 20 words total.",

            "Write a bold market commentary post with SPECIFIC numbers and timeframes. Pick a trending asset (Bitcoin, Gold, stocks, etc) and make a prediction or observation with exact prices, percentages, or dollar amounts. Keep under 80 words.",

            "Create a post about the real enemy in trading. Start with: 'The market is not your enemy. It doesn't know you exist.' Then list 3 things that ARE the opponent. Use line breaks. Keep under 50 words.",

            "Create an educational post with 5 trading tips in bullet point format. Start with a bold opening statement, then list 5 specific trading strategies. Keep each bullet SHORT. End with a memorable closer. Total under 100 words."
        ]

    def call_deepseek_api(self, prompt):
        """Call DeepSeek API to generate content"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            system_prompt = """You are a viral TWITTER trading content creator. Your posts get 2K-658K views. Focus on TRADING PSYCHOLOGY, MARKET COMMENTARY, and PRACTICAL TRADING ADVICE.

TWITTER STYLE RULES:
- Keep it SHORT (20-80 words ideal)
- Use line breaks for emphasis
- Be bold and direct
- Focus on TRADING/MARKETS only
- Make it quotable and shareable
- End strong

Write like viral Twitter trading accounts: sharp, insightful, memorable."""

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{prompt}\n\nRespond with ONLY the post content. No explanations."}
                ],
                "temperature": 1.0,
                "max_tokens": 300,
                "stream": False
            }

            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                content = content.replace('"', '').replace("'", '').strip()
                return content
            else:
                return None

        except Exception as e:
            print(f"API Exception: {e}")
            return None

    def generate_posts(self):
        """Generate 5 posts and return as list (no file I/O)"""
        posts = []

        for i, prompt in enumerate(self.prompts, 1):
            content = self.call_deepseek_api(prompt)

            if content:
                word_count = len(content.split())
                max_words = 120

                if word_count > max_words:
                    words = content.split()[:max_words]
                    content = ' '.join(words) + "..."

                posts.append({
                    'number': i,
                    'content': content,
                    'timestamp': datetime.now().strftime("%H:%M")
                })
            else:
                # Backup content
                backup = self.get_backup_content(i)
                posts.append({
                    'number': i,
                    'content': backup,
                    'timestamp': datetime.now().strftime("%H:%M"),
                    'backup': True
                })

            time.sleep(0.5)

        return posts

    def get_backup_content(self, index):
        """Backup content if API fails"""
        backups = [
            "Trading is the hardest skill in the world.\n\nNot because of the charts...\nBut because it forces you to master yourself.\n\nDiscipline. Patience. Emotional control.\nMost people can't handle it.",
            "Most traders want the results, but not the process.\n\nAnd that is why they fail.",
            "Gold is up over $75, trading above $4,838. Gold is up almost $250 so far this week. I remember when moves like this took months. Now it happens in days.",
            "The market is not your enemy.\nIt doesn't know you exist.\n\nYour habits are the opponent.\nYour blind reactions are the opponent.\nYour unexamined beliefs are the opponent.",
            "Most traders fail because they trade hope, not process.\n\n• Cut losses at -5%\n• Only size up after 3 wins\n• Trade the 1H chart\n• Let winners ride\n• No trades in first 30 min\n\nExecution is everything."
        ]
        return backups[(index - 1) % len(backups)]
