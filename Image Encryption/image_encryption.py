from PIL import Image
from random import shuffle
from words import WORDS
from copy import deepcopy

# create a 1:1 mapping of RGB values
def random_color_map():
    r_random_map = list(range(256))
    shuffle(r_random_map)
    g_random_map = list(range(256))
    shuffle(g_random_map)
    b_random_map = list(range(256))
    shuffle(b_random_map)

    return r_random_map, g_random_map, b_random_map

# convert values from 0-255 to correspond with words
def word_map(r_map, g_map, b_map):
    words = []
    words.append(' '.join([WORDS[r] for r in r_map]))
    words.append(' '.join([WORDS[g] for g in g_map]))
    words.append(' '.join([WORDS[b] for b in b_map]))
    words = '\n'.join(words)
    return words

# encrypt an image (in place)
def encrypt(image):
    r_map, g_map, b_map = random_color_map()
    for i in range(3):
        for y in range(image.height):
            for x in range(image.width):
                # get color at (x, y)
                r, g, b = image.getpixel((x, y))

                # rotate color map
                r_map.append(r_map.pop(0))
                g_map.append(g_map.pop(0))
                b_map.append(b_map.pop(0))

                # map color
                r = r_map[r]
                g = g_map[g]
                b = b_map[b]

                # copy mapped color 
                image.putpixel((x, y), (r, g, b))
        image.rotate(90)

    words = word_map(r_map, g_map, b_map)
    with open("words.txt", 'w') as ofile:
                ofile.flush()
                ofile.write(words)


def decrypt(image):
    r_map = []
    g_map = []
    b_map = []

    # make words into color maps
    with open('words.txt') as ifile:
        lines = ifile.readlines()
        r_map = [WORDS.index(w) for w in lines[0].split()]
        g_map = [WORDS.index(w) for w in lines[1].split()]
        b_map = [WORDS.index(w) for w in lines[2].split()]
    for i in range(3):
        for y in range(image.height - 1, -1, -1):
            for x in range(image.width -1, -1, -1):
                # get color at (x, y)
                r, g, b = image.getpixel((x, y))
                
                # map colors
                r = r_map.index(r)
                g = g_map.index(g)
                b = b_map.index(b)

                # rotate color map
                r_map.insert(0, r_map.pop())
                g_map.insert(0, g_map.pop())
                b_map.insert(0, b_map.pop())

                image.putpixel((x, y), (r, g, b))
        image.rotate(270)

def main():
    im = Image.open("a.jpg")
    encrypt(im)
    im.save('b.jpg')
    decrypt(im)
    im.save('c.jpg')

if __name__ == '__main__':
    main()