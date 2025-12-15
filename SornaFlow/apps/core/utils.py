# Handles dynamic file upload paths with UUID-based filenames

import os
from uuid import uuid4


class FileUpload:
    def __init__(self, dir, prefix):
        self.dir = dir              # Base directory for file storage
        self.prefix = prefix        # Subfolder or category name

    def upload_to(self, instance, filename):
        filename, ext = os.path.splitext(filename)  # Extract file extension
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'  # Generate unique file path
