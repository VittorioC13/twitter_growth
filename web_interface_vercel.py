"""
Web interface for Twitter Content Generator - VERCEL OPTIMIZED
Generates 5 posts instead of 10 to fit within Vercel's 10-second timeout
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

# HTML Template - Same as before but updated for 5 posts
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twitter Content Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #1DA1F2 0%, #14171A 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 { color: #1DA1F2; font-size: 2.5em; margin-bottom: 10px; }
        .header p { color: #657786; font-size: 1.1em; }
        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            margin-top: 10px;
        }
        .status-ready { background: #17BF63; color: white; }
        .main-content { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }
        @media (max-width: 768px) { .main-content { grid-template-columns: 1fr; } }
        .card {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .card h2 { color: #14171A; margin-bottom: 20px; font-size: 1.5em; }
        .generate-btn {
            width: 100%;
            padding: 18px;
            background: #1DA1F2;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 15px;
        }
        .generate-btn:hover {
            background: #1A91DA;
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(29, 161, 242, 0.4);
        }
        .generate-btn:disabled { background: #AAB8C2; cursor: not-allowed; transform: none; }
        .loading { display: none; text-align: center; padding: 20px; color: #657786; }
        .loading.active { display: block; }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #1DA1F2;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .files-list { max-height: 400px; overflow-y: auto; }
        .file-item {
            padding: 15px;
            border: 1px solid #E1E8ED;
            border-radius: 10px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }
        .file-item:hover { background: #F7F9FA; border-color: #1DA1F2; }
        .file-info { flex: 1; }
        .file-name { font-weight: 600; color: #14171A; margin-bottom: 5px; }
        .file-date { font-size: 0.9em; color: #657786; }
        .file-actions { display: flex; gap: 10px; }
        .btn-small {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 600;
            transition: all 0.2s;
        }
        .btn-view { background: #1DA1F2; color: white; }
        .btn-view:hover { background: #1A91DA; }
        .btn-download { background: #17BF63; color: white; }
        .btn-download:hover { background: #12A356; }
        .success-message {
            display: none;
            padding: 15px;
            background: #E8F5E9;
            color: #2E7D32;
            border-radius: 10px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        .success-message.active { display: block; }
        .info-box {
            background: #F7F9FA;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }
        .info-box h3 { color: #14171A; margin-bottom: 10px; font-size: 1.1em; }
        .info-box ul { list-style: none; padding: 0; }
        .info-box li {
            padding: 8px 0;
            color: #657786;
            border-bottom: 1px solid #E1E8ED;
        }
        .info-box li:last-child { border-bottom: none; }
        .info-box strong { color: #14171A; }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
        }
        .modal.active { display: flex; justify-content: center; align-items: center; }
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 20px;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
            width: 90%;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .modal-close {
            background: #E0245E;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }
        .post-item {
            padding: 20px;
            border: 1px solid #E1E8ED;
            border-radius: 10px;
            margin-bottom: 15px;
            background: #F7F9FA;
        }
        .post-number {
            color: #1DA1F2;
            font-weight: 700;
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        .post-content {
            color: #14171A;
            line-height: 1.6;
            white-space: pre-wrap;
            margin-bottom: 10px;
        }
        .copy-btn {
            background: #1DA1F2;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9em;
        }
        .copy-btn:hover { background: #1A91DA; }
        .vercel-badge {
            background: #FFE5E5;
            color: #E0245E;
            padding: 10px 15px;
            border-radius: 10px;
            font-size: 0.9em;
            margin-bottom: 15px;
            border-left: 4px solid #E0245E;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐦 Twitter Content Generator</h1>
            <p>AI-Powered Viral Trading Content for Twitter (Vercel Optimized)</p>
            <div class="status-badge status-ready">✓ Ready to Generate</div>
        </div>

        <div class="main-content">
            <div class="card">
                <h2>Generate Content</h2>
                <div class="vercel-badge">
                    ⚡ Vercel-Optimized: Generates 5 posts in ~7-10 seconds
                </div>
                <div class="success-message" id="successMessage">
                    ✓ Content generated successfully!
                </div>
                <button class="generate-btn" id="generateBtn" onclick="generateContent()">
                    🚀 Generate 5 Posts Now
                </button>
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Generating viral trading content...</p>
                    <p style="font-size: 0.9em;">This takes about 7-10 seconds</p>
                </div>

                <div class="info-box">
                    <h3>What Gets Generated:</h3>
                    <ul>
                        <li><strong>5 Unique Posts</strong> - Ready for Twitter</li>
                        <li><strong>Viral Formats</strong> - Based on 2K-658K view posts</li>
                        <li><strong>Trading Focus</strong> - Psychology, strategy, markets</li>
                        <li><strong>PDF + Text</strong> - Easy to copy & paste</li>
                    </ul>
                </div>
            </div>

            <div class="card">
                <h2>Generated Files</h2>
                <div class="files-list" id="filesList">
                    <p style="color: #657786; text-align: center; padding: 40px;">
                        No files yet. Generate your first batch!
                    </p>
                </div>
            </div>
        </div>
    </div>

    <div class="modal" id="postsModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Generated Posts</h2>
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
                    setTimeout(() => successMsg.classList.remove('active'), 5000);
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                btn.disabled = false;
                loading.classList.remove('active');
                alert('Error generating content: ' + error);
            });
        }

        function loadFiles() {
            fetch('/files')
            .then(response => response.json())
            .then(data => {
                const filesList = document.getElementById('filesList');

                if (data.files.length === 0) {
                    filesList.innerHTML = '<p style="color: #657786; text-align: center; padding: 40px;">No files yet. Generate your first batch!</p>';
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
                            <button class="btn-small btn-view" onclick="viewPosts('${file.txt_path}')">View Posts</button>
                            <button class="btn-small btn-download" onclick="downloadFile('${file.pdf_path}')">Download PDF</button>
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
                        <button class="copy-btn" onclick="copyToClipboard(\`${post.replace(/`/g, '\\`')}\`)">📋 Copy to Clipboard</button>
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
                alert('✓ Copied to clipboard!');
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
    print("Generates 5 posts in ~7-10 seconds")
    print("="*60)
    print("\nStarting web server...")
    print("Open your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")

    app.run(debug=False, host='0.0.0.0', port=5000)
