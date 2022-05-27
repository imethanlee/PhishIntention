from demo.phishintention_demo import *
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--cpu', action="store_true", default=False)
args = parser.parse_args()

# Phishing URLs
url = "https://s3.eu-west-3.amazonaws.com/access.doc.microsoft/indexs.html"
# url = "http://azure.delamibrands.com/Office/new%20(1)/"
# url = "https://wx.eslvocabfox.com/clao/"
# url = "http://casaelizabeth.com/neon/Webmail/index.html"

# Benign URLs
# url = "https://bhooi.github.io/"
# url = "https://www.google.com/"

demo = PhishIntentionDemo(args=args)

try:
    # Detection
    start_time = time.time()
    is_phishing, target_brand, object_detection_img_path = demo.detect(url)
    end_time = time.time()
    # Result
    print(
        "\nPhishIntention Result for '{}':".format(url),
        "\nPhishing? {}".format(is_phishing),
        "\nTime Cost: {}s".format(end_time - start_time),
        "\nTarget Brand: {}\n".format(target_brand))
except Exception as e:
    ...
