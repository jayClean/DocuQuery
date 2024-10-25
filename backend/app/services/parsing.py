import mimetypes
import tempfile
import os
import boto3
import traceback
import inspect
from unstructured.partition.docx import partition_docx
from unstructured.partition.pdf import partition_pdf, partition_pdf_or_image
from unstructured.partition.doc import partition_doc
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.csv import partition_csv
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.auto import partition
from app.config import settings

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region
)

async def parse_document(s3_url: str):
    # Extract bucket name and file key from S3 URL
    bucket_name = s3_url.split('/')[2]
    file_key = "/".join(s3_url.split('/')[3:])

    try:
        # Step 1: Retrieve the content type of the S3 object
        content_type = get_content_type(bucket_name, file_key)
        if not content_type:
            return ""

        # Step 2: Stream the file directly from S3
        file_stream = get_s3_object_stream(bucket_name, file_key)
        if not file_stream:
            return ""

        # Step 3: Create a temporary file to write the contents from S3
        temp_file_path = create_temp_file(file_stream)
        if not temp_file_path:
            return ""

        # Step 4: Parse the document using the appropriate method
        parsed_content = parse_temp_file(temp_file_path, content_type, file_key)
        return parsed_content if parsed_content else ""

    except Exception as e:
        line_no = inspect.currentframe().f_lineno
        print(f"General error: {str(e)}\nLine: {line_no}")
        return ""

def get_content_type(bucket_name, file_key):
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=file_key)
        return response.get('ContentType', 'binary/octet-stream')
    except Exception as e:
        line_no = inspect.currentframe().f_lineno
        print(f"Error retrieving content type from S3: {str(e)}\nLine: {line_no}")
        return ""

def get_s3_object_stream(bucket_name, file_key):
    try:
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        return s3_object['Body']  # This is a streaming body
    except Exception as e:
        line_no = inspect.currentframe().f_lineno
        print(f"Error retrieving file from S3: {str(e)}\nLine: {line_no}")
        return None

def create_temp_file(file_stream):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_stream.read())
            return temp_file.name
    except Exception as e:
        line_no = inspect.currentframe().f_lineno
        print(f"Error creating temporary file: {str(e)}\nLine: {line_no}")
        return None

def parse_temp_file(temp_file_path, content_type, file_key):
    # Determine the file extension from the key
    file_extension = file_key.split('.')[-1].lower()

    # Map content types to partition functions
    partition_map = {
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': partition_docx,
        'application/pdf': partition_pdf_or_image,
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': partition_pptx,
        'text/csv': partition_csv,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': partition_xlsx,
        'application/msword': partition_doc
    }

    try:
        elements = None

        # Try to get the partition function based on the content type
        if content_type in partition_map:
            with open(temp_file_path, 'rb') as file:  # Open the file as a binary file
                elements = partition_map[content_type](file=file)  # Pass the file object
        else:
            # Use mimetypes to guess the content type based on file extension
            mime_type, _ = mimetypes.guess_type(file_key)
            if mime_type in partition_map:
                print(f"Guessed content type: {mime_type}")
                with open(temp_file_path, 'rb') as file:  # Open the file as a binary file
                    elements = partition_map[mime_type](file=file)  # Pass the file object
            else:
                line_no = inspect.currentframe().f_lineno
                print(f"Unsupported content type: {content_type}\nLine: {line_no}")
                return ""

        # Join the parsed elements into a single string
        parsed_content = "\n\n".join([str(el) for el in elements])
        print(f"Parsed content from S3 file:\n{parsed_content}")
        return parsed_content

    except Exception as e:
        line_no = traceback.extract_tb(e.__traceback__)[-1][1]
        print(f"Error parsing document: {str(e)}\nLine: {line_no}")
        tb = traceback.format_exc()
        print("Traceback (most recent call last):")
        print(tb)
        return ""

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
