from pyspark import SparkContext
import cv2
import numpy as np

# Initialize a Spark context
sc = SparkContext(appName="ImageProcessing")

# Input and output directories
input_dir = "hdfs:///path/to/input/directory"
output_dir_clear = "hdfs:///path/to/output/directory/clear"
output_dir_obstructed = "hdfs:///path/to/output/directory/obstructed"

def brighten_image(image_path):
    # Read image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Calculate mean brightness
    mean_brightness = gray.mean()

    # Brighten if image is dark
    if mean_brightness < 100:
        alpha = 1.5
        beta = 50
        brightened = cv2.addWeighted(img, alpha, np.zeros(img.shape, img.dtype), 0, beta)

        return (image_path, brightened)

    else:
        print("L'image n'est pas sombre.")
        return (image_path, img)


def detect_obstruction(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection algorithm
    canny = cv2.Canny(gray, 30, 150)

    # Check if image is obstructed
    if cv2.countNonZero(canny) > 0:
        return (image[0], image[1], "obstructed")
    else:
        return (image[0], image[1], "clear")

# Create RDD of file paths
images = sc.binaryFiles(input_dir).map(lambda x: x[0])

# Apply brightening to images
brightened_images = images.map(brighten_image).filter(lambda x: x is not None)

# Detect obstruction in images
obstruction_detection = brightened_images.map(lambda x: detect_obstruction(x))

# Separate obstructed and clear images
clear_images = obstruction_detection.filter(lambda x: x[2] == "clear")
obstructed_images = obstruction_detection.filter(lambda x: x[2] == "obstructed")

# Save clear images to output directory
clear_images.foreach(lambda x: cv2.imwrite(output_dir_clear + "/" + os.path.basename(x[0]), x[1]))

# Save obstructed images to output directory
obstructed_images.foreach(lambda x: cv2.imwrite(output_dir_obstructed + "/" + os.path.basename(x[0]), x[1]))

# Stop Spark context
sc.stop()
