import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
import os


def split_image_into_quadrants(image, output_prefix):
    """
    Splits the given image into four quadrants and saves them.

    Args:
    - image (PIL.Image.Image): The image object to split.
    - output_prefix (str): The prefix for the output filenames.

    Returns:
    - None
    """
    try:
        # Get image dimensions
        width, height = image.size
        # Calculate the center points
        center_x, center_y = width // 2, height // 2
        # Define box coordinates for the four quadrants
        boxes = [
            (0, 0, center_x, center_y),  # Top-left
            (center_x, 0, width, center_y),  # Top-right
            (0, center_y, center_x, height),  # Bottom-left
            (center_x, center_y, width, height)  # Bottom-right
        ]

        # Crop and save each quadrant
        for i, box in enumerate(boxes):
            quadrant = image.crop(box)
            quadrant.save(f"{output_prefix}_quadrant_{i + 1}.png")

    except Exception as e:
        print(f"Error splitting image: {e}")


def process_images_in_folder(input_folder, output_folder):
    """
    Processes all images in the input folder, splits them into quadrants, and saves them in the output folder.

    Args:
    - input_folder (str): Path to the folder containing input images.
    - output_folder (str): Path to the folder where quadrants will be saved.

    Returns:
    - None
    """
    try:
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Loop through all files in the input folder
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                input_path = os.path.join(input_folder, filename)

                with Image.open(input_path) as img:
                    output_prefix = os.path.join(output_folder, os.path.splitext(filename)[0])
                    split_image_into_quadrants(img, output_prefix)

    except Exception as e:
        print(f"Error processing images in folder: {e}")


def fetch_and_split_image(url, output_folder):
    """
    Fetches an image from the given URL, splits it into quadrants, and saves them in the output folder.

    Args:
    - url (str): URL of the image to fetch.
    - output_folder (str): Path to the folder where quadrants will be saved.

    Returns:
    - None
    """
    try:
        # Fetch the image from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        filename = filename.split("_")[-1]  # Getting only file ID
        output_prefix = os.path.join(output_folder, os.path.splitext(filename)[0])

        # Open the image from the fetched content
        image = Image.open(BytesIO(response.content))

        # Split the image into quadrants and save
        split_image_into_quadrants(image, output_prefix)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")

    except Exception as e:
        print(f"Error processing image: {e}")


if __name__ == "__main__":
    process_images_in_folder("input", "output")


