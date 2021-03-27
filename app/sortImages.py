import sys
import os
import json
import re
import boto3
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(os.getenv('LOG_LEVEL', 'WARNING'))
logger.addHandler(handler)

client = boto3.client('rekognition')


def main():
    """
    画像を指定のキーでソートする。

    Parameters
    ----------
        argv[1] : string
            画像ファイルディレクトリ
        argv[2] : string
            ソートに使用するAWS Rekognitionの解析結果の項目のID
    """
    logger.info(sys.argv)
    img_dir = sys.argv[1]
    sort_key_id = int(sys.argv[2])

    image_files = list(map(lambda file: os.path.join(
        img_dir, file), os.listdir(img_dir)))
    sort_image(get_image_sortKey(image_files, sort_key_id))


def get_image_sortKey(image_files, sort_key_id):
    """
    画像のソートキーを取得する。

    Parameters
    ----------
        image_files: list[string]
            画像ファイルパス
        sort_key_id: int
            ソートに使用するAWS Rekognitionの解析結果の項目のID

    Returns
    -------
        list[dict[string, string]]
            [ファイルパス、ソートキー]のdictのlist
    """
    return list(map(lambda image_path: extract_key_id(sort_key_id, *(request_rekognition(image_path))), image_files))


def request_rekognition(image_file_path):
    """
    画像をAWS Rekognition(Text)で解析する。

    Parameters
    ----------
        image_file_path: string
            画像ファイルパス

    Returns
    -------
        image_file_path: string
            画像ファイルパス
        result: dict
            AWS Rekognition解析結果
    """
    with open(image_file_path, 'rb') as image:
        image_bytes = image.read()

    result = client.detect_text(
        Image={
            'Bytes': image_bytes
        }
    )

    return image_file_path, result


def extract_key_id(sort_key_id, image_file_path, rekognition_result):
    """
    AWS Rekognitionの解析結果からソートキーを抽出する。

    Parameters
    ----------
        image_file_path: string
            画像ファイルパス

    Returns
    -------
        dict[string, string]
            [ファイルパス、ソートキー]のdict
    """
    detections = rekognition_result['TextDetections']
    if(len(detections) > 0):
        filterd = list(filter(lambda d: d['Id'] == sort_key_id, detections))
        if (len(filterd) > 0):
            key = str(filterd[0]['DetectedText'])
        else:
            key = ""
    else:
        key = ""

    return dict(file=image_file_path, key=key)


def sort_image(image_files):
    """
    ファイル名の先頭にソートキーを付与しリネームする。

    Parameters
    ----------
        image_files: list[string, string]
            [ファイルパス、ソートキー]のdictのlist
    """
    for f in sorted(image_files, key=lambda f: f['key']):
        src = f['file']
        src_file_name = os.path.basename(src)
        dist = re.sub(src_file_name, f['key'] + '_' + src_file_name, src)
        os.rename(src, dist)


if __name__ == '__main__':
    main()
