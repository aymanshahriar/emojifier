import glob
import os
from PIL import Image
from scipy import spatial
import numpy as np



class Emojifier:
    # There are 3 class variables:
    # 1) emojis_path: the path of the directory containing all the emojis
    # 2) emojis: a list containing all emojis as Image objects (or rather, the list stores references to the Image objects)
    # 3) tree: a k-dimentional tree loaded with the mean color of each emoji
    def __init__(self, emojis_path: str = 'emojis'):
        self.emojis_path = emojis_path

        # Store all emojis in-memory as a list of Image objects
        self.emojis = []
        for emoji_path in glob.glob(f'{emojis_path}/*.png'):
            emoji = Image.open(emoji_path)
            emoji = emoji.convert("RGB")  ###### I added this to not get an error in "closest = tree.query(pixel)"
            #emoji = emoji.resize(emoji_size)
            self.emojis.append(emoji)

        # Calculate dominant color of each emoji     (I can save this)
        emoji_mean_colors = []
        for emoji in self.emojis:
            mean_color = np.array(emoji).mean(axis=0).mean(axis=0)
            emoji_mean_colors.append(mean_color)

        # Create a KDTree consisting of all the mean colors
        self.tree = spatial.KDTree(emoji_mean_colors)

    def emojify(self, image: Image, size = 10) -> Image:
        # Sources and settings
        emoji_size = (size, size)

        # Resize emojis
        resized_emojis = [emoji.resize(emoji_size) for emoji in self.emojis]

        # Pixelate (resize) main photo
        width = round(image.size[0] / emoji_size[0])
        height = round(image.size[1] / emoji_size[1])
        resized_photo = image.resize((width, height))

        # For every pixel, use the kdtree to find the emoji that is the most similar in color
        closest_emojis = [[0 for _ in range(width)] for _ in range(height)]   # this is an empty numpy array

        for w in range(width):
            for h in range(height):
                pixel = resized_photo.getpixel((w, h))  # Get the pixel color at (x-axis, y-axis) starting from top left corner
                closest_distance, closest_index = self.tree.query(pixel)             # tree.query returns (distance, index)
                closest_emojis[h][w] = resized_emojis[closest_index]

        # Create an "empty" image
        emojified_image = Image.new('RGB', image.size)
        emojified_image.filename = 'emojified_' + str(size) + '_' + os.path.basename(image.filename)

        # Paste emojis on that "empty" image
        for w in range(width):
            for h in range(height):
                # Offset of tile
                x, y = w*emoji_size[0], h*emoji_size[1]
                # Draw tile
                emoji = closest_emojis[h][w]
                emojified_image.paste(emoji, (x, y))

        # Return this emojified image
        return emojified_image

    def emojify_image_path(self, image_path: str = "images/pink.jpg", size: int = 10) -> Image:
        image = Image.open(image_path)
        emojified_image = self.emojify(image, size)
        return emojified_image

if __name__ == '__main__':
    emojifier = Emojifier()
    emojified_image: Image = emojifier.emojify_image_path()

    # Save output
    emojified_image.save('results/' + emojified_image.filename)
