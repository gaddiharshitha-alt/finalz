from flask import Flask, request, jsonify, send_from_directory
from googletrans import Translator
from gtts import gTTS
import base64
import os
import io

app = Flask(__name__, static_folder='.')

translator = Translator()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'en')
        target_lang = data.get('target_lang', 'hi')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Translate the text
        result = translator.translate(text, src=source_lang, dest=target_lang)
        translated_text = result.text

        # Generate audio using gTTS
        tts = gTTS(text=translated_text, lang=target_lang, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

        return jsonify({
            'translated_text': translated_text,
            'audio': audio_base64
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("  VoiceTranslate Pro - Flask Server")
    print("  Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
