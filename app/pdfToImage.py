import sys
import os
import pathlib
from pdf2image import convert_from_path
from logging import getLogger

logger = getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'WARNING'))

def main():
    logger.info(sys.argv)
    pdf_path = sys.argv[1]
    img_dir = sys.argv[2]

    pdf_file = pathlib.Path(pdf_path)
    last_page = None if len(sys.argv) < 4 else sys.argv[3]

    images = convert_from_path(pdf_file, last_page=last_page)
    for i, image in enumerate(images):
        image.save(img_dir/pathlib.Path(pdf_file.stem + '-{}.jpeg'.format(i + 1)), 'JPEG')

if __name__ == '__main__':
    main()
