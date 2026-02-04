# A simple script to calculate BMI
import pywebio
from pywebio.input import file_upload, select, input_group
from pywebio.output import put_image, put_markdown, put_html, put_button, style, put_text, put_buttons

import glob
from PIL import Image
from pywebio.session import download
from scipy import spatial
import numpy as np
import os
'''
def put_file(name, content, label=None, scope=None) -> Output:

    if label is None:
        label = name
    output = put_buttons(buttons=[name], 
                         onclick=[lambda: download(name, content)],
                         scope=scope, position=position)
    return output
'''

def emojify(main_photo_path, size):
    tile_photos_path = "tiles/*"
    #size = 10
    tile_size = (size, size)
    output_path = "more_" + str(size) + ".jpg"

    # Get all tiles
    tile_paths = []
    for file in glob.glob(tile_photos_path):
        tile_paths.append(file)
    #print(len(tile_paths))

    # Import and resize all tiles   (I can save the resized images)
    tiles = []
    # i = 1
    for path in tile_paths:
        tile = Image.open(path)
        tile = tile.convert("RGB")  ###### I added this to not get an error in "closest = tree.query(pixel)"
        tile = tile.resize(tile_size)
        tiles.append(tile)
        # print(i, "/", "3577")
        # i += 1
    #print(len(tiles))

    # Calculate dominant color or each emoji     (I can save this)
    colors = []
    for tile in tiles:
        mean_color = np.array(tile).mean(axis=0).mean(axis=0)
        colors.append(mean_color)

    # Pixelate (resize) main photo
    main_photo = Image.open(main_photo_path)

    width = int(np.round(main_photo.size[0] / tile_size[0]))
    height = int(np.round(main_photo.size[1] / tile_size[1]))

    resized_photo = main_photo.resize((width, height))

    # Find closest tile photo for every pixel
    # Create a KDTree
    tree = spatial.KDTree(colors)

    # Empty integer array to store indices of tiles
    closest_tiles = np.zeros((width, height), dtype=np.uint32)
    for i in range(width):
        for j in range(height):
            pixel = resized_photo.getpixel((i, j))  # Get the pixel color at (i, j)
            closest = tree.query(pixel)  # Returns (distance, index)
            #print(pixel)
            closest_tiles[i, j] = closest[1]  # We only need the index
    #print(closest_tiles)
    print("************ Reached here 3")
    # Create an output image
    output = Image.new('RGB', main_photo.size)
    # Draw tiles
    for i in range(width):
        for j in range(height):
            # Offset of tile
            x, y = i * tile_size[0], j * tile_size[1]
            # Index of tile
            index = closest_tiles[i, j]
            # Draw tile
            output.paste(tiles[index], (x, y))
    # Save output
    output.save(output_path)

    put_markdown('<br><hr><br>')
    put_image(open(output_path, 'rb').read())
    content = open(output_path, 'rb').read()
    put_markdown('<br><br>')
    #p = put_file('emojified.jpg', content, 'download me').style('background-color: #f44336; color: white; padding: 14px 25px; text-align: center; text-decoration: none; display: inline-block;')

    put_button('Click to download\nthe emojified image', lambda: download('emojified.jpg', content)).style( 'display: block; margin-left: auto; margin-right: auto;')
    #.style('background-color: #f44336; color: white; padding: 14px 25px; text-align: center; text-decoration: none; display: inline-block;')

    put_markdown('<br><br>')

def bmi():

    title = '''<!-- HTML Codes by Quackit.com -->
    <!DOCTYPE html>
    <title>Text Example</title>
    <style>
    div.container {
    background-color: #ffffff;
    }
    div.container p {
    text-align: center;
    font-family: Cursive;
    font-size: 48px;
    font-style: normal;
    font-weight: bold;
    text-decoration: none;
    text-transform: none;
    color: #fce94f;
    background-color: #ffffff;
    }
    </style>

    <div class="container">
    <p>😀❤️🕵️🧠🍆   Emojifier    🍔🐙👍🏼🤬☠️</p>
    </div>'''
    put_html(title)

    put_html('<br><hr><br>')

    img = file_upload("Select a picture that you want to emojify:", accept="image/*")

    dropdown_list = [("Extra Small", 5), ("Small", 10), ("Medium", 20), ("Large", 50)]
    size = pywebio.input.select(label="Select the size of the Emojis", options=dropdown_list)
    put_image(img['content'])  # display image on webpage
    open('userImage/' + img['filename'], 'wb').write(img['content'])   # put image inside userImage file

    imagePath = 'userImage/' + img['filename']
    print(imagePath)

    emojify(imagePath, size)   ##### create a function that takes the location of the user's image, emojifies it, prints it on the screen and let's the user download


if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        pywebio.start_server(bmi, port=port)












'''
    dropdown_list = [("Extra Small", 5), ("Small", 10), ("Medium", 20), ("Large", 50)]
    info = input_group("User info", [
        file_upload("Select a picture that you want to emojify:", accept="image/*", name="img"),
        select(label="Select the size/granularity of the emojis:", options=dropdown_list, name="size")
    ])

    put_image(info['img']['content'])  # display image on webpage
    open('userImage/' + info['img']['filename'], 'wb').write(info['img']['content'])   # put image inside userImage file
    imagePath = 'userImage/' + info['img']['filename']

    size = info['size']

    emojify(imagePath, size)   ##### create a function that takes the location of the user's image, emojifies it, prints it on the screen and let's the user download

'''