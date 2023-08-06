_s3_client = None


# improves speed for connecting on subsequent calls
def _get_s3_client():
    global _s3_client
    import boto3
    _s3_client = boto3.session.Session().client('s3') if _s3_client is None else _s3_client
    return _s3_client


def _load_from_bucket(bucket: str, key: str):
    from botocore.exceptions import ClientError
    try:
        return _get_s3_client().get_object(Bucket=bucket, Key=key)['Body'].read()
    except ClientError:
        return None
