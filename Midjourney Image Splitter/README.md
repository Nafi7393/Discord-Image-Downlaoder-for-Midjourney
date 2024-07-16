# MidJourney Image Quadrant Splitter

This is a simple script to split MidJourney images into four quadrants. The script can process images from a local folder or fetch an image from a URL and split it into four equal parts.

## Features

- Split any image into four quadrants and save each quadrant as a separate file.
- Process multiple images in a folder.
- Fetch and process an image from a URL.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `requests`
  - `Pillow`



## Usage

### Split Images in a Folder

1. **Prepare your input folder**:
   - Place all the images you want to process in a folder named `input`.

2. **Run the script**:
   ```bash
   python main.py
   ```

3. **Output**:
   - The quadrants of each image will be saved in a folder named `output`.

### Fetch and Split an Image from a URL

1. **Run the function manually**:
   - Open `main.py`.
   - Call the `fetch_and_split_image` function with the desired URL and output folder.
   - Example:
     ```python
     fetch_and_split_image("https://example.com/path/to/your/image.jpg", "output")
     ```

2. **Run the script**:
   ```bash
   python main.py
   ```

## Detailed Description

### Functions

- **split_image_into_quadrants(image, output_prefix)**
  - Splits a given image into four quadrants.
  - Saves each quadrant as a separate file with the specified prefix.

- **process_images_in_folder(input_folder, output_folder)**
  - Processes all images in the specified input folder.
  - Splits each image into four quadrants and saves them in the output folder.

- **fetch_and_split_image(url, output_folder)**
  - Fetches an image from the specified URL.
  - Splits the fetched image into four quadrants.
  - Saves the quadrants in the output folder.

### Example Workflow

1. **Input Image**:
   - Original image placed in the `input` folder.

2. **Output Images**:
   - Four quadrants of the original image saved in the `output` folder:
     - `output/image_quadrant_1.png`
     - `output/image_quadrant_2.png`
     - `output/image_quadrant_3.png`
     - `output/image_quadrant_4.png`
3. **EXAMPLE**:
<table>
  <thead>
    <tr>
      <th>Original Image</th>
      <th>Quadrant Images</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="5"><img src="input/1.png" alt="Original Image"></td>
    </tr>
    <tr>
      <td><img src="output/1_quadrant_1.png" alt="Quadrant 1"></td>
    </tr>
    <tr>
      <td><img src="output/1_quadrant_2.png" alt="Quadrant 2"></td>
    </tr>
    <tr>
      <td><img src="output/1_quadrant_3.png" alt="Quadrant 3"></td>
    </tr>
    <tr>
      <td><img src="output/1_quadrant_4.png" alt="Quadrant 4"></td>
    </tr>
  </tbody>
</table>


## Error Handling

- The script includes error handling to catch and print any issues that occur during processing, such as file not found errors or issues with fetching an image from a URL.
