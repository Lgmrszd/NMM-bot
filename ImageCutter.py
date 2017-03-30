from PIL import Image

debug = 0

def PurifyNoiseSimple(img):
    return Image.eval(img, lambda x: 0 if x < 50 else 255 if x > 200 else x)


def IsPixWhite(pix):
    if len(pix) == 3:
        r, g, b = tuple(255 - x for x in pix)
    else:
        r, g, b, _ = tuple(255 - x for x in pix)
    return (r + 1) * (g + 1) * (b + 1) < 30


def IsPixBlack(pix):
    if len(pix) == 3:
        r, g, b = pix
    else:
        r, g, b, _ = pix
    return (r + 1) * (g + 1) * (b + 1) < 30


def IsPixGray(pix):
    if len(pix) == 3:
        r, g, b = pix
    else:
        r, g, b, _ = pix
    return (max(r, g, b) - min(r, g, b) < 30) and not (IsPixWhite(pix)) and not (IsPixBlack(pix))


def IsPixColored(pix):
   return not(IsPixBlack(pix) or IsPixWhite(pix) or IsPixGray(pix))

def TestImage(img):
    w, h = img.size
    for x in range(w):
        for y in range(h):
            pix = img.getpixel((x, y))
            if IsPixWhite(pix):
                img.putpixel((x, y), (255, 255, 255, 255))
            elif IsPixGray(pix):
                img.putpixel((x, y), (122, 122, 122, 255))
            elif IsPixBlack(pix):
                img.putpixel((x, y), (0, 0, 0, 255))
            else:
                img.putpixel((x, y), (255, 0, 0, 255))
    img.show()


def SplitTwitterMemeImage(img) -> (Image.Image, Image.Image):
    ysplit = -1
    w, h = img.size
    # img.crop((0,0,2,2)).show()
    #img_purified = PurifyNoiseSimple(img)
    av_lines = []
    for y in range(h):
        img_line = img.crop((0, y, w, y + 1))
        img_line_data = img_line.getdata()
        # print(img_line.size)
        r, g, b = 0, 0, 0
        for pix in img_line_data:
            r += pix[0]
            g += pix[1]
            b += pix[2]
        r, g, b = r // w, g // w, b // w
        av_pix = (r, g, b, 255)
        av_lines.append(av_pix)
        #print(av_pix)
        if debug == 1:
            for x in range(w):
                if IsPixWhite(av_pix):
                    img.putpixel((x, y), (255, 255, 255, 255))
                elif IsPixGray(av_pix):
                    img.putpixel((x, y), (122, 122, 122, 255))
                elif IsPixBlack(av_pix):
                    img.putpixel((x, y), (0, 0, 0, 255))
                else:
                    img.putpixel((x, y), (255, 0, 0, 255))
        elif debug == 2:
            for x in range(w):
                img.putpixel((x, y), av_pix)
    img.show()
    #img.save('test-images/out.png', 'PNG')
    colored = False
    for y in range(y-1,-1,-1):
        if IsPixColored(av_lines[y]):
            colored = True
        elif IsPixWhite(av_lines[y]) and colored:
            ysplit = y
            break
    print(ysplit)
    if ysplit > 0:
        img1 = img.crop((0, 0, w, ysplit))
        img2 = img.crop((0, ysplit, w, h))
        return img1, img2
    else:
        raise Warning('No border to split')
