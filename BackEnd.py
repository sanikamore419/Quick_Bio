from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key.strip() == "":
    raise ValueError("GEMINI_API_KEY not found in .env file or is empty.")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Flask
app = Flask(__name__, template_folder='templates')
CORS(app)

# ✅ Serve the index.html from templates folder
@app.route('/')
def serve_frontend():
    return render_template('index.html')

# API route to generate bio
@app.route('/generate', methods=['POST'])
def generate_bio():
    try:
        data = request.get_json()
        hobbies = data.get('hobbies', '')
        profession = data.get('profession', '')
        tone = data.get('tone', '')
        platform = data.get('platform', '')
        subject = data.get('subject', '[Subject taught]')

        prompt = f"""
You are a professional social media bio generator.

Based on the following details, generate 4 bio options for a {platform} profile.

User Details:
- Profession: {profession}
- Subject: {subject}
- Hobbies: {hobbies}

Tones:
1. Formal & concise
2. Warm & inviting
3. Playful & engaging
4. Music-focused

Replace "[Subject taught]" with the actual subject: {subject}.
Keep each version short, with hashtags or emojis suitable for Instagram bios.
"""

        response = model.generate_content(prompt)
        bio_output = response.text.strip()

        return jsonify({'bio': bio_output})

    except Exception as e:
        return jsonify({'bio': f"❌ Error: {str(e)}"}), 500

# Run app
if __name__ == '__main__':
    app.run(debug=True)
