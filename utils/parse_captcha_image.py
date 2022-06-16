from PIL import Image
import pytesseract


def get_number_from_captcha_image():
    """parse numbers in captcha image to string"""
    try:
        captcha_img = Image.open('captcha_data/captcha.png')
        captcha_number = pytesseract.image_to_string(captcha_img, config='--psm 6')

        return str(int(captcha_number))
    except Exception as ex:
        print(f'could not parse captcha image, error: {ex}')
