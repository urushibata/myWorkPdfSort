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

sort_index=${2}

# S3からPDFをダウンロード
echo "PDF Douloading From S3 ..."
aws s3 cp ${s3_pdf_url} ${pdf_path}

# 画像に変換する。
echo "PDF Convert Image."
python3 /opt/app/pdfToImage.py ${pdf_path} ${img_temp_dir}

# 画像解析してソート順を決定する。
echo "Image Rekognition."
python3 /opt/app/sortImages.py ${img_temp_dir} ${sort_index}

# 画像をPDFに変換する。
echo "Image merge PDF."
python3 /opt/app/imageToPdf.py ${img_temp_dir} ${pdf_sorted_path}

# PDFをS3にアップロード
echo "PDF Uploading To S3 ..."
aws s3 cp ${pdf_sorted_path} ${s3_sorted_pdf_url}