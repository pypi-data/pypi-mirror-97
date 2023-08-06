#  Copyright 2021 Data Spree GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import io
from enum import Enum

import cv2
import numpy as np
from PIL import ExifTags, Image

from dlds.decoder.dlds_decoder import *


class ReadingMode(Enum):
    GRAYSCALE = 1
    RGB = 2
    RGBA = 3
    ANY = 4


class OpencvDecoder(DLDSDecoder):
    def __init__(self, reading_mode: ReadingMode = ReadingMode.ANY) -> None:
        super().__init__()

        self.reading_mode = reading_mode

        self.exif_orientation_tag = None
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                self.exif_orientation_tag = orientation
                break

    def __call__(self, image_bytes):
        buffer = np.asarray(bytearray(image_bytes), dtype=np.uint8)
        image = None

        if self.reading_mode == ReadingMode.GRAYSCALE:
            image = cv2.imdecode(buffer, cv2.IMREAD_GRAYSCALE)
            image = np.expand_dims(image, 2)
        if self.reading_mode == ReadingMode.RGB:
            image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        elif self.reading_mode == ReadingMode.ANY or self.reading_mode == ReadingMode.RGBA:
            # load the image as is (e.g., grayscale, RGB, RGBA and with any depth - 8-bit/16-bit/32-bit)
            image = cv2.imdecode(buffer, cv2.IMREAD_UNCHANGED)

            # rotate the image according to the exif orientation
            if self.exif_orientation_tag is not None:
                # unfortunately, opencv does not expose the exif flags, so that we open the image with pillow
                # fortunately, pillow opens images in a lazy fashion
                image_pil = Image.open(io.BytesIO(image_bytes))
                if hasattr(image_pil, '_getexif'):
                    exif = image_pil._getexif()
                    if exif is not None:
                        exif = dict(exif.items())
                        if exif[self.exif_orientation_tag] == 3:
                            image = cv2.rotate(image, cv2.ROTATE_180)
                        elif exif[self.exif_orientation_tag] == 6:
                            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                        elif exif[self.exif_orientation_tag] == 8:
                            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        if image is not None:
            if image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

        return image

    def __reduce__(self):
        return OpencvDecoder, (self.reading_mode,)

    @staticmethod
    def get_file_extensions() -> List[str]:
        return ['bmp', 'dib', 'jpeg', 'jpg', 'jpe', 'jp2', 'png', 'pdm', 'pgm', 'ppm', 'sr', 'ras', 'tiff', 'tif']
