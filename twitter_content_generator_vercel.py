# Twitter Trading Content Generator - VERCEL OPTIMIZED (5 Posts)
# This version generates 5 posts instead of 10 to fit within Vercel's 10-second timeout
import os
import schedule
import time
import json
from datetime import datetime
from pathlib import Path
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TwitterContentGenerator:
    def __init__(self, api_key=None):
        """Initialize Twitter Trading Content Generator"""
        # Set DeepSeek API key
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Please set DEEPSEEK_API_KEY in .env file or pass api_key parameter")

        # Create Output folder
        self.output_folder = Path("Output")
        self.output_folder.mkdir(exist_ok=True)

        # VERCEL OPTIMIZED: Only 5 prompts (best performing formats)
        # This keeps generation under 10 seconds for Vercel free tier
        self.prompts = [
            # FORMAT 1: Trading Psychology - Short & Profound (Trading Composure style - 2.8K-6.5K views)
            "Create a short philosophical post about trading psychology. Format: '[Bold statement about trading]. [Elaboration in 1-2 sentences]. [Ending that drives it home].' Example style: 'Trading is the hardest skill in the world. Not because of the charts... But because it forces you to master yourself. Discipline, Patience, Emotional control. Most people can't handle it.' Keep it under 50 words. Make it profound about the mental game of trading.",

            # FORMAT 2: Process vs Results (Trading Composure - 5.4K views)
            "Write a post contrasting what traders want vs what they need. Format: 'Most traders want [X], but not [Y]. And that is why they fail.' Example: 'Most traders want the results, but not the process.' Keep it SHORT - 2 lines maximum, under 20 words total.",

            # FORMAT 3: Market Commentary with Specific Numbers (Peter Schiff style - 17K-658K views)
            "Write a bold market commentary post with SPECIFIC numbers and timeframes. Pick a trending asset (Bitcoin, Gold, stocks, etc) and make a prediction or observation with exact prices, percentages, or dollar amounts. Compare past vs present pace of moves. Example: 'Gold is up $250 this week. I remember when moves like this took months. Now it happens in days.' Use real market dynamics. Keep under 80 words.",

            # FORMAT 4: The Market Is Not Your Enemy (Trading Composure - 4.4K views)
            "Create a post about the real enemy in trading. Start with: 'The market is not your enemy. It doesn't know you exist.' Then list 3 things that ARE the opponent (habits, blind reactions, unexamined beliefs, etc). Use line breaks. Keep under 50 words.",

            # FORMAT 5: Educational Trading List (TSDR Trading style - 3.8K views)
            "Create an educational post with 5 trading tips in bullet point format. Start with a bold opening statement, then list 5 specific trading strategies or principles. Example structure: 'Embrace the gap down. Look for strength and reversals. Use stories and themes for stock selection. Use multiple timeframes.' Keep each bullet SHORT. End with a memorable closer like 'Shred.exe' or similar. Total under 100 words."
        ]

        # Setup PDF styles
        self.setup_styles()

    def setup_styles(self):
        """Setup PDF styling"""
        self.styles = getSampleStyleSheet()

        # Header style
        self.styles.add(ParagraphStyle(
            name='Header',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.black,
            spaceAfter=20,
            alignment=TA_LEFT
        ))

        # Content style
        self.styles.add(ParagraphStyle(
            name='Content',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.darkblue,
            spaceAfter=15,
            alignment=TA_LEFT
        ))

        # Timestamp style
        self.styles.add(ParagraphStyle(
            name='TimeStamp',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            spaceAfter=30,
            alignment=TA_LEFT
        ))

    def call_deepseek_api(self, prompt):
        """Call DeepSeek API to generate content"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # System prompt optimized for TWITTER TRADING content based on viral examples
            system_prompt = """You are a viral TWITTER trading content creator. Your posts get 2K-658K views. You focus on TRADING PSYCHOLOGY, MARKET COMMENTARY, and PRACTICAL TRADING ADVICE.

Your proven viral formats on Twitter:

1. TRADING PSYCHOLOGY (Trading Composure - consistently 2K-6K views):
   - Short, profound statements about the mental game
   - "Trading is the hardest skill in the world. Not because of the charts... But because it forces you to master yourself."
   - "'All in' is stupid. Trading is not one trade. Trading is thousands of small, boring, disciplined, positive EV decisions stacked quietly on top of each other."
   - "The market is not your enemy. It doesn't know you exist. Your habits are the opponent. Your blind reactions are the opponent."

2. PROCESS VS RESULTS THEME (Trading Composure - 3K-5K views):
   - "Most traders want the results, but not the process. And that is why they fail."
   - "Good trading isn't about seeing further. It's about reacting better."

3. MARKET COMMENTARY (Peter Schiff - 17K-658K views):
   - Use SPECIFIC numbers, prices, and timeframes
   - "Gold is up over $75, trading above $4,838. Gold is up almost $250 so far this week..."
   - Compare historical pace vs current pace of market moves

4. EDUCATIONAL LISTS (TSDR Trading - 3.8K views):
   - Bullet points with specific trading strategies
   - "Embrace the gap down. Look for strength and reversals. Use multiple timeframes."
   - End with memorable closer

TWITTER STYLE RULES:
- Keep it SHORT - Twitter rewards brevity (20-80 words ideal)
- Use line breaks for emphasis and readability
- Be bold and direct - no fluff
- Focus on TRADING/MARKETS only (psychology, strategy, market commentary)
- Use specific trading terms (EV, position sizing, timeframes, support/resistance)
- Make it quotable and shareable
- End strong - last line should hit hard

AVOID:
- Long paragraphs (break them up)
- Generic advice
- Investment advice for beginners
- Non-trading topics

Write like the viral Twitter trading accounts: sharp, insightful, memorable."""

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nRespond with ONLY the post content. No explanations, no quotes, no meta-commentary. Just the raw tweet text."
                    }
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
                # Clean content: remove quotes and extra spaces
                content = content.replace('"', '').replace("'", '').strip()
                return content
            else:
                print(f"API Error: {response.status_code}")
                return None

        except Exception as e:
            print(f"API Exception: {e}")
            return None

    def generate_daily_posts(self):
        """Generate 5 daily Twitter posts (Vercel optimized)"""
        print(f"\n{'='*60}")
        print(f"Generating Content - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        posts = []

        for i, prompt in enumerate(self.prompts, 1):
            print(f"Generating post {i}/5...")

            content = self.call_deepseek_api(prompt)

            if content:
                # Twitter character limit is 280, but we want shorter, punchier posts
                word_count = len(content.split())
                max_words = 120  # Keep it concise for Twitter

                if word_count > max_words:
                    words = content.split()[:max_words]
                    content = ' '.join(words) + "..."

                post_item = {
                    'number': i,
                    'content': content,
                    'timestamp': datetime.now().strftime("%H:%M")
                }
                posts.append(post_item)
                try:
                    print(f"  [OK] {content[:50]}...")
                except UnicodeEncodeError:
                    print(f"  [OK] Content generated successfully (Post #{i})")
            else:
                # If API fails, use backup content
                backup_content = self.get_backup_content(i)
                post_item = {
                    'number': i,
                    'content': backup_content,
                    'timestamp': datetime.now().strftime("%H:%M"),
                    'backup': True
                }
                posts.append(post_item)
                try:
                    print(f"  [BACKUP] Using backup: {backup_content[:50]}...")
                except UnicodeEncodeError:
                    print(f"  [BACKUP] Using backup content (Post #{i})")

            time.sleep(0.5)  # Shorter delay for Vercel (but still avoid rate limits)

        print(f"\n[OK] Successfully generated {len(posts)} posts")
        return posts

    def get_backup_content(self, index):
        """Get backup content (used when API fails) - Based on PROVEN viral Twitter posts"""
        backup_contents = [
            # PROVEN: Trading Composure - Trading is hardest skill
            "Trading is the hardest skill in the world.\n\nNot because of the charts...\nBut because it forces you to master yourself.\n\nDiscipline. Patience. Emotional control.\nMost people can't handle it.\n\nDo you agree?",

            # PROVEN: Trading Composure - Process (5.4K views)
            "Most traders want the results, but not the process.\n\nAnd that is why they fail.",

            # PROVEN: Peter Schiff - Gold commentary (17K views)
            "Gold is up over $75, trading above $4,838. Gold is up almost $250 so far this week, and it's still only Tuesday in the U.S. I remember when it took gold months, sometimes years, to move up that much. Now it happens in just a few days. Soon it will happen in just one day!",

            # PROVEN: Trading Composure - Market not your enemy (4.4K views)
            "The market is not your enemy.\nIt doesn't know you exist.\n\nYour habits are the opponent.\nYour blind reactions are the opponent.\nYour unexamined beliefs are the opponent.\n\nMaster these, or they will master you.",

            # PROVEN: TSDR Trading - Educational list (3.8K views)
            "Most traders fail because they trade hope, not process.\n\n• Cut losses at -5%, not -50%\n• Only size up after 3 consecutive wins\n• Trade the 1H chart, confirm on the 15M\n• Let winners ride to the next major S/R level\n• No trades in the first 30 minutes\n\nExecution is everything. Shred.exe"
        ]
        return backup_contents[(index - 1) % len(backup_contents)]

    def create_pdf(self, posts):
        """Create PDF file"""
        # Generate filename
        date_str = datetime.now().strftime("%Y%m%d")
        filename = self.output_folder / f"Twitter_Posts_{date_str}.pdf"

        # Create PDF document
        doc = SimpleDocTemplate(str(filename), pagesize=letter)
        story = []

        # Add title
        title = f"Daily Twitter Trading Posts - {datetime.now().strftime('%B %d, %Y')}"
        story.append(Paragraph(title, self.styles['Header']))
        story.append(Paragraph(f"Generated at: {datetime.now().strftime('%H:%M:%S')}", self.styles['TimeStamp']))

        # Add content with page breaks between posts
        for i, post in enumerate(posts):
            content_text = f"<b>{post['number']}.</b> {post['content']}"
            story.append(Paragraph(content_text, self.styles['Content']))

            # Add page break if not last post
            if i < len(posts) - 1:
                story.append(PageBreak())

        # Build PDF
        doc.build(story)
        print(f"[OK] PDF saved: {filename}")
        return filename

    def save_as_text(self, posts):
        """Save as text file (backup)"""
        date_str = datetime.now().strftime("%Y%m%d")
        filename = self.output_folder / f"Twitter_Posts_{date_str}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Daily Twitter Trading Posts\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"Time: {datetime.now().strftime('%H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            for post in posts:
                f.write(f"{post['number']}. {post['content']}\n\n")
                f.write("-" * 60 + "\n\n")

        print(f"[OK] Text backup saved: {filename}")

    def run_daily_generation(self):
        """Run daily generation task"""
        try:
            # Generate content
            posts = self.generate_daily_posts()

            if posts:
                # Create PDF
                pdf_file = self.create_pdf(posts)

                # Save text backup
                self.save_as_text(posts)

                # Print summary
                print(f"\n{'='*60}")
                print("Content generation complete!")
                print(f"PDF file: {pdf_file}")
                print(f"Location: {self.output_folder.absolute()}")
                print(f"{'='*60}")

                return True
            else:
                print("[ERROR] Content generation failed")
                return False

        except Exception as e:
            print(f"[ERROR] Error during generation: {e}")
            return False

def main():
    """Main function"""
    print("="*60)
    print("Twitter Trading Content Generator v1.0 (Vercel Optimized)")
    print("Generates 5 posts optimized for Vercel deployment")
    print("="*60)

    # Load API key from environment variable
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        print("ERROR: DeepSeek API key required")
        print("Please set DEEPSEEK_API_KEY in .env file")
        print("Example: DEEPSEEK_API_KEY=sk-your-key-here")
        return

    # Create generator instance
    generator = TwitterContentGenerator(api_key)

    # Run generation
    generator.run_daily_generation()

if __name__ == "__main__":
    main()
