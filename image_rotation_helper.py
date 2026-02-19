#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Image rotation helper with EXIF preservation
Extracts EXIF before rotation and reattaches it after
"""

from PIL import Image


class ImageRotationHelper:
    """Helper class for rotating images while preserving EXIF data"""

    @staticmethod
    def rotate_with_exif(image_path, rotate_degrees=180):
        """
        Rotate an image while preserving EXIF data.

        Process:
        1. Extract EXIF binary data from image
        2. Rotate image using PIL
        3. Reattach EXIF to rotated image

        Args:
            image_path (str): Path to image file
            rotate_degrees (int): Rotation angle (default: 180)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Step 1: Extract EXIF before rotation
            exif_data = None
            with Image.open(image_path) as img:
                exif_data = img.info.get('exif')

            # Step 2: Rotate image
            with Image.open(image_path) as img:
                rotated = img.rotate(rotate_degrees, expand=False)
                rotated.save(image_path, quality=95)

            # Step 3: Reattach EXIF if it existed
            if exif_data:
                with Image.open(image_path) as img:
                    img.save(image_path, quality=95, exif=exif_data)

            return True

        except Exception as e:
            print(f"Image rotation failed: {e}")
            return False
