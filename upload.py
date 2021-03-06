from memory_profiler import profile
import boto3
import uuid
import json

sc = boto3.client('s3')
bucket_name = 'xxxxxxxx'
encoding = 'utf-8'

@profile()
def upload():
    key = f'tests/{uuid.uuid4().hex[10:]}'
    mpu = sc.create_multipart_upload(
        Bucket=bucket_name,
        ContentEncoding=encoding,
        ContentType=f'application/x-jsonlines; charset={encoding}',
        Key=key
    )

    upload_id = mpu['UploadId']

    end = 10
    parts = []

    for i in range(end):
        part_number = i + 1
        contnet = f'{json.dumps(j)}\n' * 1024 * 1024
        part = sc.upload_part(
            Bucket=bucket_name,
            Key=key,
            PartNumber=part_number,
            UploadId=upload_id,
            Body=contnet.encode(encoding)
        )
        parts.append({
            'PartNumber': part_number,
            'ETag': part['ETag']
        })

        if part_number == end:
            sc.complete_multipart_upload(
                Bucket=bucket_name,
                MultipartUpload={
                    'Parts': parts
                },
                Key=key,
                UploadId=upload_id
            )


if __name__ == '__main__':
    upload()
