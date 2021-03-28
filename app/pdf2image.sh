#!/bin/bash

set -eu

function catch() {
    error_code=$1
    line_num=$2

    echo "---------------------------"
    echo "Error Code : ${error_code}"
    echo "Line : ${line_num}"
    echo "---------------------------"

    exit ${error_code}
}

trap 'catch $? $LINENO' ERR

cd $(cd $(dirname $0) && pwd)

source ./variable

# S3からPDFをダウンロード
echo "PDF Douloading From S3 ..."
aws s3 cp ${s3_pdf_url} ${pdf_path}

# 先頭の1ページのみ変換する。
echo "PDF Convert Image."
python3 /opt/app/pdfToImage.py ${pdf_path} ${img_temp_dir} 1

# S3へ画像をアップロード
echo "Image Uploading To S3 ..."
aws s3 cp ${img_temp_dir} ${s3_img_url} --recursive

echo "Image Upload S3 Finished."