import glob
from PIL import Image
from scipy import spatial
import numpy as np
import os


def emojify(image: Image, size = 10) -> Image:
    # Sources and settings
    emojis_path = "emojis/*"
    emoji_size = (size, size)

    # Import and resize all emojis   (I can save the resized images)
    emojis = []
    for emoji_path in glob.glob(emojis_path):
        emoji = Image.open(emoji_path)
        emoji = emoji.convert("RGB")  ###### I added this to not get an error in "closest = tree.query(pixel)"
        emoji = emoji.resize(emoji_size)
        emojis.append(emoji)

    # Calculate dominant color of each emoji     (I can save this)
    emoji_mean_colors = []
    for emoji in emojis:
        mean_color = np.array(emoji).mean(axis=0).mean(axis=0)
        emoji_mean_colors.append(mean_color)

    # Pixelate (resize) main photo
    width = int(np.round(image.size[0] / emoji_size[0]))
    height = int(np.round(image.size[1] / emoji_size[1]))
    resized_photo = image.resize((width, height))

    # For every pixel, find the emoji that is the most similar in color
    # Create a KDTree
    tree = spatial.KDTree(emoji_mean_colors)
    # Empty integer array to store indices of emojis
    closest_tiles = np.zeros((width, height), dtype=np.uint32)

    for i in range(width):
        for j in range(height):
            pixel = resized_photo.getpixel((i, j))  # Get the pixel color at (i, j)
            closest = tree.query(pixel)             # Returns (distance, index)
            closest_tiles[i, j] = closest[1]        # We only need the index

    # Create an "empty" image
    emojified_image = Image.new('RGB', image.size)
    emojified_image.filename = 'emojified_' + str(size) + '_' + os.path.basename(image.filename)

    # Paste emojis on that "empty" image
    for i in range(width):
        for j in range(height):
            # Offset of tile
            x, y = i*emoji_size[0], j*emoji_size[1]
            # Index of tile
            index = closest_tiles[i, j]
            # Draw tile
            emojified_image.paste(emojis[index], (x, y))

    # Return this emojified image
    return emojified_image

def emojify_image_path(image_path: str = "pics/pink.jpg", size: int = 10) -> Image:
    image = Image.open(image_path)
    emojified_image = emojify(image, size)
    return emojified_image

if __name__ == '__main__':
    emojified_image: Image = emojify_image_path()

    # Save output
    emojified_image.save('results/' + emojified_image.filename)
