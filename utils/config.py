import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    BEDROCK_KB_ID = os.getenv('BEDROCK_KB_ID')
    BEDROCK_DATA_SOURCE_ID = os.getenv('BEDROCK_DATA_SOURCE_ID')
    _model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-v2')
    # Clean up potentially messy env var (quotes, comments from docker/env files)
    if _model_id:
        _model_id = _model_id.split('#')[0].strip().strip('"').strip("'")
    BEDROCK_MODEL_ID = _model_id
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    @staticmethod
    def validate():
        if not Config.BEDROCK_KB_ID:
            raise ValueError("BEDROCK_KB_ID must be set in environment variables.")
