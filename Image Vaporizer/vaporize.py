from PIL import Image

# color palette
COLORS = ((0,0,0), (64, 64, 64), (150, 150, 150), (255,255,255),
          (0,0,255,), (64, 128, 255), (0, 128, 0), (64, 255, 64),
          (0,128,128), (0, 255, 255), (255, 0, 0), (255, 128, 128),
          (128,0,128), (255,64,255), (128,64,0), (255, 255, 0))


def main():
    # get image from source
    im = Image.open('vaporwave.png')
    # convert RGB to 16 color palette
    for x in range(im.width):
        for y in range(im.height):
            c = im.getpixel((x,y))
            r,g,b = c[0], c[1], c[2]
            dists = []

            for color in COLORS:
                dists.append(((r-color[0])**2 + (g-color[1])**2 + (b-color[2])**2)**(1/2))
            
            r_new, g_new, b_new = COLORS[dists.index(min(dists))]

            # convert pixel to limited palette
            im.putpixel((x,y), (r_new, g_new, b_new))

            # calculate per-channel error
            r_error = r - r_new
            g_error = g - g_new
            b_error = b - b_new

            # distribute error
            if x + 1 < im.width:
                t = im.getpixel((x+1, y))
                im.putpixel((x+1, y), ((t[0] + 7*r_error//16), (t[1] + 7*g_error//16), (t[2] + 7*b_error//16)))
            if x - 1 > 0 and y + 1 < im.height:
                t = im.getpixel((x-1, y+1))
                im.putpixel((x-1, y+1), ((t[0] + 3*r_error//16), (t[1] + 3*g_error//16), (t[2] + 3*b_error//16)))
            if y + 1 < im.height:
                t = im.getpixel((x, y+1))
                im.putpixel((x, y+1), ((t[0] + 5*r_error//16), (t[1] + 5*g_error//16), (t[2] + 5*b_error//16)))
            if x + 1 < im.width and y + 1 < im.height:
                t = im.getpixel((x+1, y+1))
                im.putpixel((x+1, y+1), ((t[0] + 1*r_error//16), (t[1] + 1*g_error//16), (t[2] + 1*b_error//16)))
    im.show()


if __name__ == '__main__':
    main()