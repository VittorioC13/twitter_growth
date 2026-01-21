"""
Web interface for Twitter Content Generator - VERCEL SERVERLESS
Clean, zen, black and white design
No file I/O - works in read-only serverless environment
"""
from flask import Flask, render_template_string, jsonify, request
import os
from datetime import datetime
from dotenv import load_dotenv
from twitter_content_generator_serverless import TwitterContentGenerator

load_dotenv()

app = Flask(__name__)

# In-memory storage for generated posts (lost on restart, but that's ok for serverless)
posts_cache = []

# HTML Template - Clean Black & White Zen Design
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twitter Content Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0a0a;
            color: #e8e8e8;
            min-height: 100vh;
            padding: 40px 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 60px;
            padding-bottom: 30px;
            border-bottom: 1px solid #2a2a2a;
        }

        .header h1 {
            font-size: 2.5em;
            font-weight: 300;
            letter-spacing: -1px;
            margin-bottom: 10px;
            color: #ffffff;
        }

        .header p {
            color: #999;
            font-size: 1em;
            font-weight: 300;
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 40px;
        }

        @media (max-width: 968px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background: #141414;
            border: 1px solid #2a2a2a;
            padding: 40px;
            transition: border-color 0.3s;
        }

        .card:hover {
            border-color: #3a3a3a;
        }

        .card h2 {
            font-size: 1.3em;
            font-weight: 400;
            margin-bottom: 30px;
            color: #ffffff;
            letter-spacing: -0.5px;
        }

        .generate-btn {
            width: 100%;
            padding: 20px;
            background: #ffffff;
            color: #000000;
            border: none;
            font-size: 1em;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            letter-spacing: 0.5px;
            margin-bottom: 20px;
        }

        .generate-btn:hover {
            background: #f5f5f5;
            transform: translateY(-1px);
        }

        .generate-btn:disabled {
            background: #333;
            color: #666;
            cursor: not-allowed;
            transform: none;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 30px;
            color: #666;
        }

        .loading.active {
            display: block;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 2px solid #222;
            border-top: 2px solid #fff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .success-message {
            display: none;
            padding: 15px;
            background: #1a2a1a;
            border: 1px solid #2a4a2a;
            color: #8fce8f;
            margin-bottom: 20px;
            font-size: 0.9em;
        }

        .success-message.active {
            display: block;
        }

        .info-box {
            background: #0f0f0f;
            border: 1px solid #2a2a2a;
            padding: 20px;
            margin-top: 20px;
        }

        .info-box h3 {
            font-size: 0.9em;
            font-weight: 500;
            margin-bottom: 15px;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .info-list {
            list-style: none;
        }

        .info-list li {
            padding: 10px 0;
            color: #aaa;
            font-size: 0.9em;
            border-bottom: 1px solid #222;
        }

        .info-list li:last-child {
            border-bottom: none;
        }

        .files-list {
            max-height: 500px;
            overflow-y: auto;
        }

        .files-list::-webkit-scrollbar {
            width: 6px;
        }

        .files-list::-webkit-scrollbar-track {
            background: #0f0f0f;
        }

        .files-list::-webkit-scrollbar-thumb {
            background: #3a3a3a;
        }

        .file-item {
            padding: 20px;
            border: 1px solid #2a2a2a;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
            background: #0f0f0f;
        }

        .file-item:hover {
            border-color: #3a3a3a;
            background: #1a1a1a;
        }

        .file-info {
            flex: 1;
        }

        .file-name {
            font-weight: 400;
            color: #ffffff;
            margin-bottom: 5px;
            font-size: 0.95em;
        }

        .file-date {
            font-size: 0.85em;
            color: #888;
        }

        .file-actions {
            display: flex;
            gap: 10px;
        }

        .btn-small {
            padding: 10px 20px;
            border: 1px solid #3a3a3a;
            background: #1a1a1a;
            color: #e8e8e8;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s;
            font-weight: 400;
        }

        .btn-small:hover {
            background: #ffffff;
            color: #0a0a0a;
            border-color: #ffffff;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.95);
            backdrop-filter: blur(10px);
        }

        .modal.active {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .modal-content {
            background: #141414;
            border: 1px solid #2a2a2a;
            padding: 40px;
            max-width: 900px;
            max-height: 90vh;
            overflow-y: auto;
            width: 100%;
        }

        .modal-content::-webkit-scrollbar {
            width: 6px;
        }

        .modal-content::-webkit-scrollbar-track {
            background: #0f0f0f;
        }

        .modal-content::-webkit-scrollbar-thumb {
            background: #3a3a3a;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #2a2a2a;
        }

        .modal-header h2 {
            font-size: 1.3em;
            font-weight: 400;
            color: #ffffff;
        }

        .modal-close {
            background: #1a1a1a;
            color: #aaa;
            border: 1px solid #3a3a3a;
            padding: 8px 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.2s;
        }

        .modal-close:hover {
            background: #ffffff;
            color: #0a0a0a;
            border-color: #ffffff;
        }

        .post-item {
            padding: 25px;
            border: 1px solid #2a2a2a;
            margin-bottom: 20px;
            background: #0f0f0f;
        }

        .post-number {
            color: #888;
            font-weight: 400;
            font-size: 0.85em;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .post-content {
            color: #e8e8e8;
            line-height: 1.8;
            white-space: pre-wrap;
            margin-bottom: 20px;
            font-size: 0.95em;
        }

        .copy-btn {
            background: #1a1a1a;
            color: #e8e8e8;
            border: 1px solid #3a3a3a;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s;
        }

        .copy-btn:hover {
            background: #ffffff;
            color: #0a0a0a;
            border-color: #ffffff;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #666;
            font-size: 0.9em;
        }

        .status-line {
            text-align: center;
            padding: 15px;
            background: #0f0f0f;
            border: 1px solid #2a2a2a;
            margin-bottom: 20px;
            font-size: 0.85em;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Twitter Content Generator</h1>
            <p>AI-powered trading content for Twitter</p>
        </div>

        <div class="main-grid">
            <div class="card">
                <h2>Generate</h2>

                <div class="status-line">
                    Optimized for 5 posts / ~8 second generation
                </div>

                <div class="success-message" id="successMessage">
                    Generation complete
                </div>

                <button class="generate-btn" id="generateBtn" onclick="generateContent()">
                    Generate 5 Posts
                </button>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Generating content...</p>
                </div>

                <div class="info-box">
                    <h3>Output</h3>
                    <ul class="info-list">
                        <li>5 unique posts</li>
                        <li>Trading psychology</li>
                        <li>Market commentary</li>
                        <li>Educational content</li>
                        <li>PDF + text format</li>
                    </ul>
                </div>
            </div>

            <div class="card">
                <h2>Generated Posts</h2>
                <div class="files-list" id="filesList">
                    <div class="empty-state">
                        Generate posts to see them here
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="modal" id="postsModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Posts</h2>
                <button class="modal-close" onclick="closeModal()">Close</button>
            </div>
            <div id="postsContainer"></div>
        </div>
    </div>

    <script>
        loadFiles();

        function generateContent() {
            const btn = document.getElementById('generateBtn');
            const loading = document.getElementById('loading');
            const successMsg = document.getElementById('successMessage');

            btn.disabled = true;
            loading.classList.add('active');
            successMsg.classList.remove('active');

            fetch('/generate', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                btn.disabled = false;
                loading.classList.remove('active');

                if (data.success) {
                    successMsg.classList.add('active');
                    displayPosts(data.posts);
                    setTimeout(() => successMsg.classList.remove('active'), 3000);
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                btn.disabled = false;
                loading.classList.remove('active');
                alert('Error: ' + error);
            });
        }

        function displayPosts(posts) {
            const filesList = document.getElementById('filesList');

            if (!posts || posts.length === 0) {
                filesList.innerHTML = '<div class="empty-state">No posts generated</div>';
                return;
            }

            filesList.innerHTML = '';
            posts.forEach((post, index) => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.innerHTML = `
                    <div class="file-info">
                        <div class="file-name">Post ${post.number}</div>
                        <div class="file-date">${post.content.substring(0, 60)}...</div>
                    </div>
                    <div class="file-actions">
                        <button class="btn-small" onclick='viewPost(${JSON.stringify(post.content)})'>View</button>
                        <button class="btn-small" onclick='copyToClipboard(\`${post.content.replace(/`/g, '\\`')}\`)'>Copy</button>
                    </div>
                `;
                filesList.appendChild(fileItem);
            });
        }

        function viewPost(content) {
            const modal = document.getElementById('postsModal');
            const container = document.getElementById('postsContainer');

            container.innerHTML = '';
            const postItem = document.createElement('div');
            postItem.className = 'post-item';
            postItem.innerHTML = `
                <div class="post-content">${content}</div>
                <button class="copy-btn" onclick='copyToClipboard(\`${content.replace(/`/g, '\\`')}\`)'>Copy</button>
            `;
            container.appendChild(postItem);
            modal.classList.add('active');
        }

        function loadPosts() {
            fetch('/posts')
            .then(response => response.json())
            .then(data => {
                if (data.posts && data.posts.length > 0) {
                    displayPosts(data.posts);
                }
            });
        }

        loadPosts();

        function closeModal() {
            document.getElementById('postsModal').classList.remove('active');
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('Copied');
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return jsonify({'success': False, 'error': 'API key not configured'})

        generator = TwitterContentGenerator(api_key)
        posts = generator.generate_posts()

        # Store in memory cache
        global posts_cache
        posts_cache = posts

        # Return posts directly
        return jsonify({
            'success': True,
            'posts': posts,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/posts')
def get_posts():
    """Return cached posts"""
    global posts_cache
    if not posts_cache:
        return jsonify({'posts': [], 'message': 'No posts generated yet'})

    return jsonify({'posts': posts_cache})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Twitter Content Generator - Vercel Optimized")
    print("="*60)
    print("\nStarting server at http://localhost:5000")
    print("="*60 + "\n")

    app.run(debug=False, host='0.0.0.0', port=5000)
