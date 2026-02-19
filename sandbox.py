import os

counter = 0
for filename in os.listdir('emojis'):
    new_filename = str(counter) + '.png'
    os.rename('emojis/' + filename, 'emojis/' + new_filename)
    counter += 1
