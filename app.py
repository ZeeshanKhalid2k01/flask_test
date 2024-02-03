from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

import os
import pyttsx3

app = Flask(__name__)
CORS(app, resources={r"/generate_audio": {"origins": "*"}})

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    data = request.get_json()

    if 'text' not in data or 'voice' not in data:
        return jsonify({'error': 'Invalid request. Required parameters are missing.'}), 400

    text = data['text']
    voice_preference = int(data['voice'])

    # Generate audio using pyttsx3
    engine = pyttsx3.init()

    # Change voice based on user preference
    voices = engine.getProperty('voices')

    if voice_preference < 0 or voice_preference >= len(voices):
        return jsonify({'error': 'Invalid voice preference.'}), 400

    selected_voice = voices[voice_preference].id
    engine.setProperty('voice', selected_voice)

    # Set other properties
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)

    # Save generated audio to file
    engine.save_to_file(text, 'generated_audio.mp3')
    engine.runAndWait()

    # Return the generated audio file as a response
    return send_file('generated_audio.mp3', as_attachment=True)
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
