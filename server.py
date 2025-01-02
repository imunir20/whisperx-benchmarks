from flask import Flask, request, jsonify
import whisperx
import gc
import torch

app = Flask(__name__)

# Load the Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"
model = whisperx.load_model("base", device=device, compute_type=compute_type)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        audio_path = f"/tmp/{audio_file.filename}"
        audio_file.save(audio_path)

        # Load audio and transcribe
        audio = whisperx.load_audio(audio_path)
        result = model.transcribe(audio, batch_size=1, language='ar')
        
        # Load alignment model and align
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device)

        # Clean up alignment model
        del model_a
        gc.collect()
        torch.cuda.empty_cache()

        return jsonify({'segments': result["segments"]})
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)