"""
Setup Guide for Google Cloud Storage Integration

This script outlines the necessary configurations and settings required to use Google Cloud Storage (GCS) with the brand_builder_agency project.

### Required GCP Settings

1. **Service Account Configuration**:
   - Create a service account in the Google Cloud Console.
   - Assign the following roles to the service account:
     - **Storage Admin**: This role allows the service account to manage storage resources, including creating and deleting buckets and objects.
     - **Service Account User**: This role allows the service account to act on behalf of other service accounts.

2. **Bucket Permissions**:
   - Navigate to the Cloud Storage section in the Google Cloud Console.
   - Select the bucket you will be using (e.g., `vrsen-staging-public`).
   - Assign the following permissions:
     - **allUsers**: Grant the role of **Storage Object Viewer** to allow public access to the objects in the bucket.

### Cost Management

- **Storage Costs**: Be aware that using Google Cloud Storage incurs costs based on the amount of data stored and the number of operations performed. 
- **Lifecycle Policy**: To avoid unexpected charges, set a lifecycle policy on your bucket to automatically delete objects after a specified period (e.g., 1 day). This can be configured in the bucket settings under "Lifecycle Management".

### Example Lifecycle Policy Configuration

1. Go to the bucket in the Google Cloud Console.
2. Click on the "Lifecycle" tab.
3. Click "Add a lifecycle rule".
4. Set the rule to delete objects older than 1 day.

Or, to ensure that test uploads are deleted after successful tests, you can modify the test script to delete the test files after successful run.
"""

from google.cloud import storage
import os
from dotenv import load_dotenv
import logging
import datetime
import uuid
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Define paths using pathlib for cross-platform compatibility
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
CACHE_DIR = ASSETS_DIR / "__pycache__"
DOWNLOADS_DIR = ASSETS_DIR / "downloads"

def get_public_url(bucket_name, blob_name):
    """Generate public URL for a blob"""
    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"

def ensure_directories():
    """Ensure all required directories exist"""
    for directory in [ASSETS_DIR, CACHE_DIR, DOWNLOADS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ensured: {directory}")
    return True

def test_gcp_connection():
    """Test basic connection to GCP bucket"""
    try:
        storage_client = storage.Client()
        bucket_name = os.getenv('GCP_BUCKET_NAME')
        bucket = storage_client.bucket(bucket_name)
        
        if bucket.exists():
            logger.info(f"Successfully connected to bucket: {bucket_name}")
            return True
        else:
            logger.error(f"Bucket {bucket_name} does not exist")
            return False
    except Exception as e:
        logger.error(f"Failed to connect to GCP bucket: {str(e)}")
        return False

def test_write_operation():
    """Test writing a test file to the bucket"""
    try:
        storage_client = storage.Client()
        bucket_name = os.getenv('GCP_BUCKET_NAME')
        bucket = storage_client.bucket(bucket_name)
        
        # Create a test file with timestamp
        test_content = f"Test content generated at {datetime.datetime.now()}"
        test_file_name = f"test_file_{uuid.uuid4()}.txt"
        
        # Create local test file first
        test_file_path = ASSETS_DIR / test_file_name
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        
        # Upload the test file
        blob_name = f"test/{test_file_name}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(test_file_path))
        
        public_url = get_public_url(bucket_name, blob_name)
        logger.info(f"Successfully wrote test file: {test_file_name}")
        logger.info(f"Public URL: {public_url}")
        return blob_name
    except Exception as e:
        logger.error(f"Failed to write to bucket: {str(e)}")
        return None

def test_image_upload():
    """Test uploading an image file from assets"""
    try:
        storage_client = storage.Client()
        bucket_name = os.getenv('GCP_BUCKET_NAME')
        bucket = storage_client.bucket(bucket_name)
        
        # Use specific image file
        test_image = "CyberSOAR  Logo-13.png"
        image_path = CACHE_DIR / test_image
        
        if not image_path.exists():
            logger.error(f"Image file not found at: {image_path}")
            logger.info(f"Available files in cache dir: {list(CACHE_DIR.glob('*'))}")
            return None
            
        # Upload to a designs folder to simulate design generator output
        blob_name = f"designs/{test_image}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(image_path))
        
        public_url = get_public_url(bucket_name, blob_name)
        logger.info(f"Successfully uploaded image: {test_image}")
        logger.info(f"Public URL: {public_url}")
        return blob_name
    except Exception as e:
        logger.error(f"Failed to upload image: {str(e)}")
        return None

def test_image_download(blob_name):
    """Test downloading an image file"""
    try:
        storage_client = storage.Client()
        bucket_name = os.getenv('GCP_BUCKET_NAME')
        bucket = storage_client.bucket(bucket_name)
        
        blob = bucket.blob(blob_name)
        download_path = DOWNLOADS_DIR / os.path.basename(blob_name)
        blob.download_to_filename(str(download_path))
        
        public_url = get_public_url(bucket_name, blob_name)
        logger.info(f"Successfully downloaded image to: {download_path}")
        logger.info(f"Public URL: {public_url}")
        return str(download_path)
    except Exception as e:
        logger.error(f"Failed to download image: {str(e)}")
        return None

def run_all_tests():
    """Run all tests in sequence"""
    logger.info("Starting GCP Storage tests...")
    
    # Ensure directories exist
    ensure_directories()
    
    # Test 1: Connection
    if not test_gcp_connection():
        logger.error("Connection test failed. Stopping further tests.")
        return
    
    # Test 2: Write Operation
    test_file = test_write_operation()
    if not test_file:
        logger.error("Write operation failed. Stopping further tests.")
        return
    
    # Test 3: Image Upload
    image_blob_name = test_image_upload()
    if image_blob_name:
        # Test 4: Image Download
        downloaded_path = test_image_download(image_blob_name)
        if downloaded_path:
            logger.info(f"Image download test successful: {downloaded_path}")
    
    logger.info("All tests completed.")

if __name__ == "__main__":
    run_all_tests() 
