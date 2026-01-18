from flask import Flask, render_template, request, jsonify
from utils.bedrock_client import BedrockClient
from utils.config import Config

app = Flask(__name__)

# Initialize Bedrock Client
try:
    bedrock_client = BedrockClient()
except Exception as e:
    print(f"Failed to initialize Bedrock Client: {e}")
    bedrock_client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    if not bedrock_client:
        return jsonify({"error": "Service not available - Bedrock Client failed to initialize"}), 503

    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400

    query = data['query']

    try:
        answer = bedrock_client.retrieve_and_generate(query)
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    if not bedrock_client:
        return jsonify({"status": "unhealthy", "error": "Bedrock Client not initialized"}), 503

    if bedrock_client.check_health():
        return jsonify({"status": "healthy", "message": "System is operational"})
    else:
        return jsonify({"status": "unhealthy", "error": "Cannot reach Knowledge Base"}), 503

@app.route('/upload', methods=['POST'])
def upload_file():
    if not bedrock_client:
        return jsonify({"error": "Service not available"}), 503

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read file bytes
        file_bytes = file.read()
        bedrock_client.ingest_document(file.filename, file_bytes)
        return jsonify({"message": f"Successfully ingested {file.filename} into Knowledge Base."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
