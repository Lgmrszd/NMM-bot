from PIL import Image
import ImageCutter

def main():
    img = Image.open('test-images/6.jpg')
    img.show()
    ImageCutter.SplitTwitterMemeImage(img)
    #ImageCutter.TestImage(img)
    # img = img.resize((600, 600), Image.BICUBIC) - ресайз
    # img.getcolors() - подсчёт цветов
    # r, g, b, a = img.split() - это смена слоёв
    # img = Image.merge("RGBA", (b, g, r, a))
    # img.crop(img.getbbox()).show() - это автокадрирование

main()