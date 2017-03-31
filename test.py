from PIL import Image
import ImageCutter

def main():
    img = Image.open('test-images/101.jpg')
    img.show()
    ImageCutter.TestImage(img)
    try:
        img1, img2 = ImageCutter.SplitTwitterMemeImage(img)
    except Warning as err:
        print('Error: ', err)
    else:
        print(type(img1))
        img1.save('test-images/out-1.png', 'PNG')
        img2.save('test-images/out-2.png', 'PNG')
    # img = img.resize((600, 600), Image.BICUBIC) - ресайз
    # img.getcolors() - подсчёт цветов
    # r, g, b, a = img.split() - это смена слоёв
    # img = Image.merge("RGBA", (b, g, r, a))
    # img.crop(img.getbbox()).show() - это автокадрирование

main()