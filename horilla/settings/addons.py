from .local_settings import *

if env("AWS_ACCESS_KEY_ID", default=None):
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")
    DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE", default="storages.backends.s3boto3.S3Boto3Storage")
    
    # S3-compatible storage endpoint (required for Railway, DigitalOcean Spaces, etc.)
    if env("AWS_S3_ENDPOINT_URL", default=None):
        AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
    
    # Optional: Addressing style for S3-compatible services (path or virtual)
    if env("AWS_S3_ADDRESSING_STYLE", default=None):
        AWS_S3_ADDRESSING_STYLE = env("AWS_S3_ADDRESSING_STYLE")
    
    # Optional: Use SSL (default True)
    AWS_S3_USE_SSL = env("AWS_S3_USE_SSL", default=True)
    
    # Optional: Verify SSL certificates (default True)
    AWS_S3_VERIFY = env("AWS_S3_VERIFY", default=True)

if env("AWS_ACCESS_KEY_ID", default=None) and "storages" not in INSTALLED_APPS:
    INSTALLED_APPS.append("storages")

if env("AWS_ACCESS_KEY_ID", default=None) and "storages" in INSTALLED_APPS:
    # Set MEDIA_URL - use custom URL if provided, otherwise construct from bucket
    if env("MEDIA_URL", default=None):
        MEDIA_URL = env("MEDIA_URL")
        if env("NAMESPACE", default=None):
            MEDIA_URL = f"{MEDIA_URL.rstrip('/')}/{env('NAMESPACE')}/"
    else:
        # Default: construct from bucket name
        bucket_name = env("AWS_STORAGE_BUCKET_NAME")
        if env("AWS_S3_ENDPOINT_URL", default=None):
            # For S3-compatible services, use the endpoint URL
            endpoint = env("AWS_S3_ENDPOINT_URL").rstrip('/')
            MEDIA_URL = f"{endpoint}/{bucket_name}/"
        else:
            # Standard AWS S3
            MEDIA_URL = f"https://{bucket_name}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/"
        
        if env("NAMESPACE", default=None):
            MEDIA_URL = f"{MEDIA_URL}{env('NAMESPACE')}/"
    
    MEDIA_ROOT = env("MEDIA_ROOT", default="")
