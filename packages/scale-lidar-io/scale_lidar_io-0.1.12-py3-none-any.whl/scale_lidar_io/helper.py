import os

import boto3
import hashlib
import ujson
import numpy as np
from io import BytesIO
from scaleapi import ScaleClient

s3 = boto3.client('s3')

## Format/ Parsing helpers

def format_lidar_point(p):
    return dict(zip(('x', 'y', 'z', 'i', 'd'), p))

def format_point(p):
    return dict(zip(('x', 'y', 'z'), p))

def format_quaternion(q):
    return dict(zip(['w', 'x', 'y', 'z'], q))

def parse_xyz(obj):
    return np.array([obj['x'], obj['y'], obj['z']])

def parse_cuboid_frame(frame):
    return np.array([parse_xyz(p) for p in [c['position'] for c in frame['cuboids']]])

def read_cuboid_points(filename):
    # Read from result file
    with open(filename, 'r') as json_file:
        return np.array([parse_cuboid_frame(frame) for frame in ujson.load(json_file)])

## Task creation helpers

def get_api_client() -> ScaleClient:
    assert os.getenv('SCALE_API_KEY'), 'No API key, please set SCALE_API_KEY environment variable'
    return ScaleClient(os.getenv('SCALE_API_KEY'))

def get_default_template():
    return {
        'task_id': None,
        'callback_url': 'http://example.com',
        'instruction': 'Please label all objects',
        'labels': [
            'Object'
        ],
        'meters_per_unit': 1,
        'max_distance_meters': 20
    }


## S3 helpers

def fp_md5(fp: BytesIO):
    fp.seek(0)
    md5 = hashlib.md5()
    buf = fp.read(2 ** 20)
    while buf:
        md5.update(buf)
        buf = fp.read(2 ** 20)
    fp.seek(0)
    return md5.hexdigest()


def get_s3_etag(bucket, key):
    try:
        return s3.head_object(Bucket=bucket, Key=key)['ETag'].strip('"')
    except Exception:
        pass

def get_signed_url(bucket: str, path: str) -> str:
    signed_url = s3.generate_presigned_url('get_object', Params={
        'Bucket': bucket,
        'Key': f'{path}/scene.json'
    })
    return signed_url

def s3_smart_upload(bucket, key, fileobj, content_type):
    s3_hash = get_s3_etag(bucket, key)
    local_hash = fp_md5(fileobj)

    if s3_hash == local_hash:
        print(f'File exists: {bucket}/{key}')
        return

    print(f'Uploading {bucket}/{key}...')
    s3.upload_fileobj(
        Fileobj=fileobj,
        Bucket=bucket,
        Key=key,
        ExtraArgs={'ContentType': content_type}
    )
