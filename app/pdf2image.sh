#!/bin/bash

cd $(cd $(dirname $0) && pwd)

source ./variable

# S3からPDFをダウンロード
aws s3 cp ${s3_pdf_url} ${pdf_path}

# 先頭の1ページのみ変換する。
python3 /opt/app/pdfToImage.py ${pdf_path} ${img_temp_dir} 1

# S3へ画像をアップロード
s3_img_url=s3://${s3_bucket}/${s3_prefix}/${pdf_basename}/
aws s3 cp ${img_temp_dir} ${s3_img_url} --recursive