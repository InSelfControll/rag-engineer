# AWS Bedrock RAG Chatbot

A lightweight Retrieval-Augmented Generation (RAG) chatbot using AWS Bedrock Knowledge Bases.

## 2) Project Repository Structure

- `main.py`: Flask API server.
- `utils/`: Helper modules.
    - `bedrock_client.py`: Logic for querying the Knowledge Base.
    - `config.py`: Environment configuration management.
- `templates/`: Frontend user interface (HTML).
- `static/`: Static assets (CSS/JS).
- `.env`: Environment variables (not committed).
- `requirements.txt`: Python dependencies.

## 3) Environment Variables

Define the following variables in a `.env` file:

```bash
AWS_REGION=us-east-1
BEDROCK_KB_ID=your-knowledge-base-id
BEDROCK_MODEL_ID=anthropic.claude-v2
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_SESSION_TOKEN=optional-session-token
```

## 4) Dependencies

The project is intentionally lightweight, using:
- `Flask`: Web framework.
- `boto3`: AWS SDK for Python.
- `python-dotenv`: Management of environment variables.

Install them via:
```bash
pip install -r requirements.txt
```

## 5) Utilities

Located in `utils/`:
- **Bedrock Interaction**: Handles `retrieve_and_generate` API calls to AWS Bedrock.
- **Configuration**: Validates and loads environment variables.

## 6) Backend Logic

Endpoints implemented in `main.py`:
- `POST /ask`: Accepts JSON `{ "query": "..." }`, queries the Knowledge Base, and returns `{ "answer": "..." }`.
- `GET /health`: Returns system availability status (200 OK or 503 Service Unavailable).

## 7) User Interface

A minimal web interface at `/`:
- Clean input field for questions.
- Display of model answers.
- (Optional) Hidden support for document context display.

## 8) Optional Enhancements

- **Document Upload Portal**: (Code present in templates but disabled for lightweight deployment).
- **Context Transparency**: Frontend supports displaying context if backend provides it.

## 9) Running the Project

### Local Execution
1.  **Clone the repository**.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Setup AWS Credentials**:
    - Ensure your AWS user has permissions for `bedrock:RetrieveAndGenerate`.
    - Create a `.env` file with your credentials and Knowledge Base ID.
4.  **Run the application**:
    ```bash
    python main.py
    ```
5.  **Access**: Open `http://localhost:5000` in your browser.

### Deployment (EC2)
1.  Launch an EC2 instance (Amazon Linux 2 or Ubuntu).
2.  Install Python 3 and Git.
3.  Clone the project.
4.  Install dependencies.
5.  Set environment variables (or use IAM execution role for the instance instead of hardcoded keys).
6.  Run with a production server (e.g., `gunicorn -w 4 -b 0.0.0.0:5000 main:app`).
7.  Ensure Security Group allows inbound traffic on port 5000.

### Validation and Testing
- **Health Check**: Visit `/health` to verify the connection to Bedrock Client.
- **Functional Test**: Ask a question relevant to your Knowledge Base content and verify the answer accuracy.
# rag-engineer
