from memory_profiler import profile
import boto3
import uuid
import json

sc = boto3.client('s3')
bucket_name = 'xxxxxxxx'

@profile()
def upload():
    # key = f'tests/{datetime.datetime.now().isoformat()}'
    key = f'tests/{uuid.uuid4().hex[10:]}'
    session = boto3.Session()
    sc = session.client('s3')

    tc = boto3.s3.transfer.TransferConfig()
    t = boto3.s3.transfer.S3Transfer(client=sc, config=tc)
    t.upload_file('hoge.txt', bucket_name, key)

if __name__ == '__main__':
    upload()
