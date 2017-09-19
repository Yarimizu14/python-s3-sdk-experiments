from memory_profiler import profile
import boto3
import requests

bucket_name = 'xxxxxxxxxx'
key = 'tests/b64029b3c2a12851f564ac'

@profile()
def download_once():
    sc = boto3.client('s3')
    obj = sc.get_object(
        Bucket=bucket_name,
        Key=key
    )
    stm = obj['Body']
    content = stm.read()
    print(content)

@profile()
def download():
    sc = boto3.client('s3')
    url = sc.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': key
        }
    )
    r = requests.get(url, stream=True)

    for chunk in r.iter_content(chunk_size=1024 * 1024 * 5):
        if chunk:
            print(chunk)


if __name__ == '__main__':
    # download()
    download_once()
