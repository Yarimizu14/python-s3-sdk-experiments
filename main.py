from memory_profiler import profile
import boto3
import datetime
import uuid


sc = boto3.client('s3')

bucket_name = 'xxxxxxxxxxx'


@profile()
def upload():
    # key = f'tests/{datetime.datetime.now().isoformat()}'
    key = f'tests/{uuid.uuid4().hex[10:]}'
    mpu = sc.create_multipart_upload(
        Bucket=bucket_name,
        # ContentEncoding='shift-jis',
        ContentType='text/csv',
        Key=key
    )

    upload_id = mpu['UploadId']

    end = 10
    parts = []

    for i in range(end):
        part_number = i + 1
        contnet = str(part_number) * 1024 * 1024 * 5
        part = sc.upload_part(
            Bucket=bucket_name,
            Key=key,
            PartNumber=part_number,
            UploadId=upload_id,
            Body=contnet.encode('utf-8')
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
