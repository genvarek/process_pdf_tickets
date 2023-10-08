import re
import cv2
import coordinates


def mask_values(img_path: str) -> None:
    image = cv2.imread(img_path)
    sectors = coordinates.coordinates.keys()

    for sector in sectors:
        x1, y1, x2, y2 = coordinates.coordinates[sector]
        image[y1:y2, x1:x2] = [255, 255, 255]

    cv2.imwrite('files/comparable_masked_image.jpg', image)


def extract_key_value(line: str) -> tuple:
    key, value = line.split(":", 1)
    key = sanitize_string(key)
    value = sanitize_string(value)
    return key, value or None


def sanitize_string(s: str) -> str:
    return re.sub("[\\n\n]", "", s).strip()
