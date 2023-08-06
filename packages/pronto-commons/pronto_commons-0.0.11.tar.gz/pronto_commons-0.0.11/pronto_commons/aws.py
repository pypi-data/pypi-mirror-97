import io

import boto3


def upload_file_to_s3(
    *, access_key: str, secret_key: str, bucket_name: str, key: str, file: io.BytesIO
):
    """Function to upload a file to an s3 bucket.

    :param str access_key: The AWS access key of the account.

    :param str secret_key: The AWS secret key of the account.

    :param str bucket_name: The name of the bucket where the file will be stored.

    :param str key: The key under the file will be stored.

    :param io.BytesIO file: The body content in bytes.

    :rtype: Object.

    :return: Returns an S3 Object, properties can be found here_.

    .. _here: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
    """
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    s3 = session.resource("s3")
    attachment_file = s3.Bucket(bucket_name).put_object(
        Key=key, Body=file, ACL="public-read"
    )
    return attachment_file
