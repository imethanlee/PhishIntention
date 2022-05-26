from demo.phishintention_demo import *
import time


demo = PhishIntentionDemo()

# Phishing URLs
phishing_url_list = [

]
# url = "https://s3.eu-west-3.amazonaws.com/access.doc.microsoft/indexs.html"
# url = "http://azure.delamibrands.com/Office/new%20(1)/"
# url = "https://wx.eslvocabfox.com/clao/"
url = "http://casaelizabeth.com/neon/Webmail/index.html"

# Benign URLs
# url = "https://bhooi.github.io/"

try:
    is_phishing, target_brand, object_detection_img_path = demo.detect(url)
    print(is_phishing, target_brand, object_detection_img_path)
except Exception as e:
    ...


# try:
#     s = time.time()
#     is_phishing, target_brand, object_detection_img_path = demo.detect("https://s3.eu-west-3.amazonaws.com/access.doc.microsoft/indexs.html")
#     print(time.time() - s, is_phishing, target_brand, object_detection_img_path)
    
#     s = time.time()
#     is_phishing, target_brand, object_detection_img_path = demo.detect("http://azure.delamibrands.com/Office/new%20(1)/")
#     print(time.time() - s, is_phishing, target_brand, object_detection_img_path)

# except Exception as e:
#     ...