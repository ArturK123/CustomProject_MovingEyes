from PIL import Image

def combine_images(image1_path, image2_path, output_path):
    # Open the images
    image1 = Image.open(image1_path).convert("RGBA")
    image2 = Image.open(image2_path).convert("RGBA")

    # Create a new image with transparent background
    combined_image = Image.new("RGBA", image1.size)

    # Paste the first image onto the new image
    combined_image.paste(image1, (0, 0), image1)

    # Paste the second image onto the new image, respecting transparency
    combined_image.paste(image2, (0, 0), image2)

    # Save the combined image
    combined_image.save(output_path, "PNG")

# Example usage
image1_path = "modified_image.png"
image2_path = "modified_image2.png"
output_path = "combined_image.png"

combine_images(image1_path, image2_path, output_path)