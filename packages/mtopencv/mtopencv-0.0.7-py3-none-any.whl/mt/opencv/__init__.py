from mt.base import logger

try:
    import cv2
except ImportError:
    logger.error("IMPORT: OpenCV for Python is not detected. Please install a version of OpenCV for Python.")
    raise
