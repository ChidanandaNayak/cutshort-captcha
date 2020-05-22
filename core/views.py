from django.shortcuts import render
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
from django.views import View
from django.http import HttpResponse
import random
import string
import json
# Create your views here.



class GenerateCaptcha:

    def __init__(self,text):
        self.text = text

    def generate_captcha_image(self):
        captcha_text = self.text
        img_captcha = ImageCaptcha()
        image = img_captcha.generate_image(captcha_text)
        img_captcha.create_noise_curve(image, image.getcolors())
        img_captcha.create_noise_dots(image, image.getcolors())
        image_file = "static/file/captcha_text" + ".png"
        img_captcha.write(captcha_text, image_file)
        return image_file

    def generate_captcha_audio(self):
        captcha_text = self.text
        audio_captcha = AudioCaptcha()
        audio_captcha.generate(captcha_text)
        # audio_file = "static/file/"+random.choice(string.digits) + '.wav'
        audio_file = "static/file/audio.wav"
        audio_captcha.write(captcha_text, audio_file)
        return audio_file

    @staticmethod
    def generate_digit():
        captcha_text = []
        for _ in range(10):
            captcha_text.append(random.choice(string.digits))
        return "".join(captcha_text)


class GenerateCaptchaView(View):

    def post(self,request):
        response = {}
        input_captcha = request.POST.get('captcha')
        if request.session['captcha_text'] == input_captcha:
            response.update({"status":200,"msg":"You have successfully solved the captcha, try another one"})
        else:
            response.update({"status": 400, "msg": "Wrong captcha! try again."})
        return HttpResponse(json.dumps(response))

    def get(self,request):
        captcha_text = GenerateCaptcha.generate_digit()
        request.session['captcha_text'] = captcha_text
        image = GenerateCaptcha(captcha_text).generate_captcha_image()
        audio = GenerateCaptcha(captcha_text).generate_captcha_audio()
        return render(request, 'captcha.html', context={"audio": audio, "image": image})







