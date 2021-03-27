#!/bin/bash

cd $(cd $(dirname $0) && pwd)

source ./variable

sort_index=${3}

# S3からPDFをダウンロード
aws s3 cp ${s3_pdf_url} ${pdf_path}

# 画像に変換する。
python3 /opt/app/pdfToImage.py ${pdf_path} ${img_temp_dir}

# 画像解析してソート順を決定する。
python3 /opt/app/sortImages.py ${img_temp_dir} ${sort_index}

# 画像をPDFに変換する。
python3 /opt/app/imageToPdf.py ${img_temp_dir} ${pdf_sorted_path}
