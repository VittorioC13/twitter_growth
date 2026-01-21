# Twitter Trading Content Generator

AI-powered Twitter content generator that creates 10 viral-style trading posts daily using DeepSeek API. Based on proven formats that get 2K-658K views on Twitter.

## Features

- **10 Proven Viral Formats** - Trading psychology, market commentary, educational lists
- **Based on Real Viral Posts** - Trained on tweets with 2.8K-658K views from top trading accounts
- **Automated Daily Generation** - Set it and forget it with Windows Task Scheduler
- **Multiple Output Formats** - PDF (formatted) and TXT (backup)
- **Web Interface** - Easy-to-use dashboard for your client
- **Twitter-Optimized** - Short, punchy posts perfect for Twitter's format

## Content Formats

The generator creates diverse content based on viral Twitter trading posts:

### 1. Trading Psychology (Trading Composure style - 2K-6K views)
Short, profound statements about the mental game:
- "Trading is the hardest skill in the world..."
- "'All in' is stupid. Trading is thousands of small decisions..."
- "The market is not your enemy. Your habits are."

### 2. Process vs Results Theme (3K-5K views)
- "Most traders want the results, but not the process."
- "Good trading isn't about seeing further. It's about reacting better."

### 3. Market Commentary (Peter Schiff style - 17K-658K views)
Specific numbers, prices, and bold predictions:
- Gold/Bitcoin/stock price movements with exact figures
- Comparisons of historical vs current market pace

### 4. Educational Lists (TSDR Trading style - 3.8K views)
Bullet points with actionable trading strategies:
- Support/resistance levels
- Multi-timeframe analysis
- Risk management rules

## Installation

### Prerequisites

- Python 3.7+
- DeepSeek API key (get one at [https://platform.deepseek.com](https://platform.deepseek.com))

### Setup Steps

1. **Navigate to the project folder:**
```bash
cd C:\Users\rotciv\Desktop\twitter_growth
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create `.env` file:**
```bash
copy .env.example .env
```

4. **Add your API key to `.env`:**
```env
DEEPSEEK_API_KEY=sk-your-actual-key-here
```

5. **Test the generator:**
```bash
python run_twitter_generation.py
```

## Usage

### Option 1: Web Interface (Recommended for Client)

Start the web dashboard:
```bash
python web_interface.py
```

Then open your browser to: `http://localhost:5000`

The web interface allows you to:
- Generate content with one click
- View all generated posts
- Download PDFs
- Check API status
- Adjust generation time

### Option 2: Manual Run

Generate content immediately:
```bash
python run_twitter_generation.py
```

### Option 3: Automated Daily Generation

Setup Windows Task Scheduler to run automatically:

**Method 1: GUI Setup**
1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click "Create Basic Task"
3. Name: "Twitter Content Generator"
4. Trigger: Daily at 17:00 (or your preferred time)
5. Action: Start a program
6. Program: `python`
7. Arguments: `run_twitter_generation.py`
8. Start in: `C:\Users\rotciv\Desktop\twitter_growth`
9. Check "Run whether user is logged on or not"

**Method 2: PowerShell (Admin)**
```powershell
$action = New-ScheduledTaskAction -Execute "python" -Argument "run_twitter_generation.py" -WorkingDirectory "C:\Users\rotciv\Desktop\twitter_growth"
$trigger = New-ScheduledTaskTrigger -Daily -At "17:00"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "TwitterContentGenerator" -Action $action -Trigger $trigger -Settings $settings
```

## Output

Generated files are saved in the `Output/` folder:

- `Twitter_Posts_YYYYMMDD.pdf` - Formatted PDF with all 10 posts (one per page)
- `Twitter_Posts_YYYYMMDD.txt` - Plain text backup

### Example Output

```
1. Trading is the hardest skill in the world.

Not because of the charts...
But because it forces you to master yourself.

Discipline. Patience. Emotional control.
Most people can't handle it.

Do you agree?

---

2. 'All in' is stupid.

Trading is not one trade.

Trading is thousands of small, boring, disciplined, positive EV decisions stacked quietly on top of each other.

---

3. The market is not your enemy.
It doesn't know you exist.

Your habits are the opponent.
Your blind reactions are the opponent.
Your unexamined beliefs are the opponent.
```

## Configuration

### Change Generation Time

Edit `run_twitter_generation.py` or use the web interface to adjust timing.

### Customize Prompts

To adjust content styles, edit the `self.prompts` array in `twitter_content_generator.py` (lines 35-110).

### API Settings

Adjust creativity in `call_deepseek_api()` method:
```python
"temperature": 1.0,  # Creativity (0.0-2.0)
"max_tokens": 300,   # Response length
```

## Project Structure

```
twitter_growth/
├── twitter_content_generator.py    # Main generator class
├── run_twitter_generation.py       # Task scheduler entry point
├── web_interface.py                # Web dashboard (optional)
├── requirements.txt                # Python dependencies
├── .env                           # API keys (not tracked in git)
├── .env.example                   # Template for .env
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
└── Output/                        # Generated content folder
    ├── Twitter_Posts_YYYYMMDD.pdf
    └── Twitter_Posts_YYYYMMDD.txt
```

## For Your Client

### Quick Start Guide for Non-Technical Users

1. **Double-click** `START_GENERATOR.bat` to generate content instantly
2. **Open** the `Output` folder to see your generated posts
3. **Copy** posts from the PDF or TXT file to Twitter
4. **Schedule** it to run daily (we can set this up for you)

### Web Dashboard

The easiest way for clients to use this:
1. Run `START_WEB.bat`
2. Browser opens automatically
3. Click "Generate Posts" button
4. View and copy posts from the dashboard

## Troubleshooting

### API Error 401
- Check your API key in `.env`
- Verify key has sufficient credits at DeepSeek platform

### Script Not Running
- Verify Python is installed: `python --version`
- Check Task Scheduler logs
- Run manually first to test

### No Output Files
- Check `Output/` folder exists
- Verify write permissions
- Check console output for errors

## Security

- API keys are stored in `.env` (not committed to git)
- `.gitignore` prevents accidental key exposure
- Never commit your `.env` file to version control

## License

MIT License - Use and modify as needed for your client

## Credits

Built with DeepSeek AI API
Optimized for viral Twitter trading content
Based on proven formats from top trading accounts

---

**For support or customization, contact the developer.**
