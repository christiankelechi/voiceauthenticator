from flask import Flask, request, jsonify
import speech_recognition as sr

# Initialize Flask app
app = Flask(__name__)

# Initialize recognizer
recognizer = sr.Recognizer()

# Route for speech-to-text
@app.route('/speech-to-text', methods=['POST','GET'])
def speech_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    # Get the file from the request
    audio_file = request.files['file']
    
    # Use SpeechRecognition to process the audio file
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)
        
        try:
            # Use Google Web Speech API to recognize the speech
            text = recognizer.recognize_google(audio)
            return jsonify({"text": text}), 200
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand the audio"}), 400
        except sr.RequestError as e:
            return jsonify({"error": f"Speech recognition service failed: {e}"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
