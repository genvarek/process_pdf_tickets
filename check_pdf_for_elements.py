from pdf2image import convert_from_path
import cv2
import numpy as np
import helpers


def compare_images(img1_path: str, img2_path: str) -> bool:
    """Take paths to 2 images, return True if the images are identical"""
    img1 = cv2.imread(img1_path, 0)  # Load in grayscale
    img2 = cv2.imread(img2_path, 0)

    # Compute the absolute difference
    diff = cv2.absdiff(img1, img2)
    ret, thresholded = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # If no differences, the sum will be zero
    total_difference = np.sum(thresholded)
    return total_difference == 0


def convert_pdf_to_image(path: str, output_folder: str) -> None:
    convert_from_path(path, output_folder=output_folder, output_file="comparable", fmt="JPEG")


"""
Convert PDF to image first;
Then mask (blur) values to compare keys and their placement only;
And finally compare contents of your pdf to the reference: True if the pdf is correct, False if not.
"""
ref_pdf_path = "./files/reference.pdf"
comparable_pdf_path = "./files/comparable.pdf"

convert_pdf_to_image(
    comparable_pdf_path,
    "./files"
)

helpers.mask_values("files/comparable0001-1.jpg")

is_pdf_correct = compare_images("files/reference_masked_image.jpg",
               "files/comparable_masked_image.jpg")
print(is_pdf_correct)
