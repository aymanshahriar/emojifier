import glob
from PIL import Image
from scipy import spatial
import numpy as np
import os

# Sources and settings
main_photo_path = "pics/pink.jpg"
path_to_emojis = "emojis/*"
size = 10
emoji_size = (size, size)
output_path = "results/emojified_" + str(size) + "_" + os.path.basename(main_photo_path)

# Import and resize all emojis   (I can save the resized images)
emojis = []
for emoji_path in glob.glob(path_to_emojis):
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
main_photo = Image.open(main_photo_path)

width = int(np.round(main_photo.size[0] / emoji_size[0]))
height = int(np.round(main_photo.size[1] / emoji_size[1]))
resized_photo = main_photo.resize((width, height))

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

# Create an output image
output = Image.new('RGB', main_photo.size)

# Draw emojis
for i in range(width):
    for j in range(height):
        # Offset of tile
        x, y = i*emoji_size[0], j*emoji_size[1]
        # Index of tile
        index = closest_tiles[i, j]
        # Draw tile
        output.paste(emojis[index], (x, y))

# Save output
output.save(output_path)
