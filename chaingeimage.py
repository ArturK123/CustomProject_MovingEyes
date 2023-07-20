from PIL import Image

def change_non_black_pixels_to_transparent(image_path):
    # Load the image
    image = Image.open(image_path).convert("RGBA")

    # Get the pixel data
    pixel_data = image.load()

    # Iterate through each pixel
    width, height = image.size
    for x in range(width):
        for y in range(height):
            # Check if the pixel is not black
            if pixel_data[x, y] != (0, 0, 0, 255):
                # Change the pixel to transparent
                pixel_data[x, y] = (0, 0, 0, 0)

    # Save the modified image
    image.save("modified_image2.png")

# Usage example
image_path = "upper.png"
change_non_black_pixels_to_transparent(image_path)