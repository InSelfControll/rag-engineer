import boto3
import os
import base64
import mimetypes
from botocore.exceptions import ClientError
from .config import Config

class BedrockClient:
    def __init__(self):
        Config.validate()
        
        # Common credentials
        kwargs = {}
        if Config.AWS_REGION:
            kwargs['region_name'] = Config.AWS_REGION
        if Config.AWS_ACCESS_KEY_ID and Config.AWS_SECRET_ACCESS_KEY:
            kwargs['aws_access_key_id'] = Config.AWS_ACCESS_KEY_ID
            kwargs['aws_secret_access_key'] = Config.AWS_SECRET_ACCESS_KEY

        print(f"Initializing Bedrock Client with region: {kwargs.get('region_name', 'default')}...")
        
        # Runtime client for querying
        self.runtime_client = boto3.client('bedrock-agent-runtime', **kwargs)
        
        # Agent client for direct ingestion
        self.agent_client = boto3.client('bedrock-agent', **kwargs)

        # S3 client for bucket operations
        self.s3_client = boto3.client('s3', **kwargs)

        # Auto-discover data source if not configured (to fix upload issues if env var is missing)
        if not Config.BEDROCK_DATA_SOURCE_ID:
            try:
                print("BEDROCK_DATA_SOURCE_ID not set, attempting to auto-discover...")
                response = self.agent_client.list_data_sources(
                    knowledgeBaseId=Config.BEDROCK_KB_ID,
                    maxResults=1
                )
                if response.get('dataSourceSummaries'):
                    ds_id = response['dataSourceSummaries'][0]['dataSourceId']
                    print(f"Auto-discovered Data Source ID: {ds_id}")
                    # Update Config in-memory so ingest_document works
                    Config.BEDROCK_DATA_SOURCE_ID = ds_id
                else:
                    print("No Data Source found for this Knowledge Base. Uploads may fail.")
            except Exception as e:
                print(f"Failed to auto-discover Data Source: {e}")

    def retrieve_and_generate(self, query):
        """
        Queries the Bedrock Knowledge Base and generates a response.
        """
        try:
            print(f"Querying Bedrock Knowledge Base ({Config.BEDROCK_KB_ID}) with model ({Config.BEDROCK_MODEL_ID})...")
            response = self.runtime_client.retrieve_and_generate(
                input={
                    'text': query
                },
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': Config.BEDROCK_KB_ID,
                        'modelArn': f'arn:aws:bedrock:{Config.AWS_REGION}::foundation-model/{Config.BEDROCK_MODEL_ID}'
                    }
                }
            )
            print("Bedrock response received successfully.")
            return response['output']['text']
        except ClientError as e:
            print(f"Error querying Bedrock: {e}")
            raise e

    def check_health(self):
        """
        Checks the health of the connection to Bedrock Knowledge Base.
        """
        try:
            self.agent_client.get_knowledge_base(knowledgeBaseId=Config.BEDROCK_KB_ID)
            return True
        except Exception as e:
            print(f"Health check failed: {e}")
            return False

    def ingest_document(self, filename, file_bytes):
        """
        Uploads a document to the S3 bucket associated with the data source
        and starts a synchronization job.
        """
        if not Config.BEDROCK_DATA_SOURCE_ID:
            raise ValueError("BEDROCK_DATA_SOURCE_ID not configured.")

        try:
            # 1. Get the Data Source configuration to find the S3 bucket
            ds_response = self.agent_client.get_data_source(
                knowledgeBaseId=Config.BEDROCK_KB_ID,
                dataSourceId=Config.BEDROCK_DATA_SOURCE_ID
            )

            ds_config = ds_response.get('dataSource', {}).get('dataSourceConfiguration', {})
            s3_config = ds_config.get('s3Configuration')

            if not s3_config:
                print("Data source is not S3-based. Falling back to direct ingestion (if supported).")
                # Fallback implementation (omitted for cleaner switch to S3)
                raise ValueError("The configured Data Source is not S3-based. Cannot upload to S3.")

            bucket_arn = s3_config.get('bucketArn')
            if not bucket_arn:
                raise ValueError("S3 Bucket ARN not found in Data Source configuration.")

            bucket_name = bucket_arn.split(':')[-1]
            print(f"Detected S3 Bucket: {bucket_name}")

            # 2. Upload file to S3
            print(f"Uploading {filename} to S3 bucket {bucket_name}...")
            # Detect mime type for S3 metadata (optional but good practice)
            mime_type, _ = mimetypes.guess_type(filename)
            extra_args = {'ContentType': mime_type} if mime_type else {}

            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=filename,
                Body=file_bytes,
                **extra_args
            )
            print("S3 upload successful.")

            # 3. Start Ingestion Job (Sync)
            print("Starting Knowledge Base ingestion job...")
            ingestion_response = self.agent_client.start_ingestion_job(
                knowledgeBaseId=Config.BEDROCK_KB_ID,
                dataSourceId=Config.BEDROCK_DATA_SOURCE_ID,
                description=f'Auto-sync for {filename}'
            )

            job_id = ingestion_response.get('ingestionJob', {}).get('ingestionJobId')
            print(f"Ingestion job started. Job ID: {job_id}")

            # Optionally, we could wait for it, but for a web request, returning success now is usually better
            # as sync can take time.
            return True

        except ClientError as e:
            print(f"Error during S3 upload or specific Bedrock call: {e}")
            raise e
        except Exception as e:
            print(f"Error processing ingestion: {e}")
            raise e
        except ClientError as e:
            print(f"Error ingesting document to Bedrock KB: {e}")
            raise e
