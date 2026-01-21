"""
Web interface for Twitter Content Generator - VERCEL OPTIMIZED
Clean, zen, black and white design
"""
from flask import Flask, render_template_string, jsonify, send_file, request
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from twitter_content_generator_vercel import TwitterContentGenerator
import glob

load_dotenv()

app = Flask(__name__)

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
                <h2>Generated Files</h2>
                <div class="files-list" id="filesList">
                    <div class="empty-state">
                        No files yet
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
                    loadFiles();
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

        function loadFiles() {
            fetch('/files')
            .then(response => response.json())
            .then(data => {
                const filesList = document.getElementById('filesList');

                if (data.files.length === 0) {
                    filesList.innerHTML = '<div class="empty-state">No files yet</div>';
                    return;
                }

                filesList.innerHTML = '';
                data.files.forEach(file => {
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.innerHTML = `
                        <div class="file-info">
                            <div class="file-name">${file.name}</div>
                            <div class="file-date">${file.date}</div>
                        </div>
                        <div class="file-actions">
                            <button class="btn-small" onclick="viewPosts('${file.txt_path}')">View</button>
                            <button class="btn-small" onclick="downloadFile('${file.pdf_path}')">Download</button>
                        </div>
                    `;
                    filesList.appendChild(fileItem);
                });
            });
        }

        function viewPosts(txtPath) {
            fetch(`/view/${txtPath}`)
            .then(response => response.json())
            .then(data => {
                const modal = document.getElementById('postsModal');
                const container = document.getElementById('postsContainer');

                container.innerHTML = '';
                data.posts.forEach((post, index) => {
                    const postItem = document.createElement('div');
                    postItem.className = 'post-item';
                    postItem.innerHTML = `
                        <div class="post-number">Post ${index + 1}</div>
                        <div class="post-content">${post}</div>
                        <button class="copy-btn" onclick="copyToClipboard(\`${post.replace(/`/g, '\\`')}\`)">Copy</button>
                    `;
                    container.appendChild(postItem);
                });

                modal.classList.add('active');
            });
        }

        function closeModal() {
            document.getElementById('postsModal').classList.remove('active');
        }

        function downloadFile(pdfPath) {
            window.location.href = `/download/${pdfPath}`;
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('Copied');
            });
        }

        setInterval(loadFiles, 10000);
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
        success = generator.run_daily_generation()

        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/files')
def list_files():
    output_folder = Path('Output')
    if not output_folder.exists():
        return jsonify({'files': []})

    pdf_files = sorted(output_folder.glob('Twitter_Posts_*.pdf'), reverse=True)

    files = []
    for pdf_file in pdf_files:
        txt_file = pdf_file.with_suffix('.txt')
        date_str = pdf_file.stem.split('_')[-1]

        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
        except:
            formatted_date = date_str

        files.append({
            'name': pdf_file.name,
            'date': formatted_date,
            'pdf_path': pdf_file.name,
            'txt_path': txt_file.name if txt_file.exists() else None
        })

    return jsonify({'files': files})

@app.route('/view/<filename>')
def view_file(filename):
    try:
        filepath = Path('Output') / filename
        if not filepath.exists():
            return jsonify({'error': 'File not found'}), 404

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        posts = []
        lines = content.split('\n')
        current_post = []

        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                if current_post:
                    posts.append('\n'.join(current_post).strip())
                current_post = [line.split('.', 1)[1].strip() if '.' in line else line]
            elif line.strip() == '-' * 60:
                if current_post:
                    posts.append('\n'.join(current_post).strip())
                    current_post = []
            elif line.strip() and not line.startswith('=') and 'Daily Twitter' not in line and 'Date:' not in line and 'Time:' not in line:
                current_post.append(line)

        if current_post:
            posts.append('\n'.join(current_post).strip())

        return jsonify({'posts': posts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    filepath = Path('Output') / filename
    if not filepath.exists():
        return "File not found", 404

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Twitter Content Generator - Vercel Optimized")
    print("="*60)
    print("\nStarting server at http://localhost:5000")
    print("="*60 + "\n")

    app.run(debug=False, host='0.0.0.0', port=5000)
