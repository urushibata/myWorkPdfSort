import sys
import os
from PIL import Image
from logging import getLogger
from natsort import natsorted

logger = getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'WARNING'))


def main():
    """
    画像をソートしてPDFを作成する。

    Parameters
    ----------
        argv[1] : string
            画像ファイルディレクトリ
        argv[2] : string
            出力PDFファイルパス
    """
    logger.info(sys.argv)
    img_dir = sys.argv[1]
    pdf_output_path = sys.argv[2]

    image_files = get_image_files(img_dir)

    images = list(map(lambda image: Image.open(
        os.path.join(img_dir, image)).convert("RGB"), image_files))
    top_image = images.pop(0)

    top_image.save(pdf_output_path, save_all=True, append_images=images)


def get_image_files(img_dir):
    """
    PDFに変換する画像を取得する。

    Parameters
    ----------
        img_dir : string
            変換対象の画像ディレクトリパス

    Returns
    -------
        list[string]
            変換対象の画像ファイルのリスト
    """
    return natsorted(os.listdir(img_dir))


if __name__ == '__main__':
    main()
