from demo.phishintention_demo import *
import time
import argparse
from demo.typosquatting import *


parser = argparse.ArgumentParser()
parser.add_argument('--cpu', action="store_true", default=True)
args = parser.parse_args()


ts = TypoSquatting()
demo = PhishIntentionDemo(args=args)


# Dynamic Analysis:
domain = None # TODO: user input
url_list = ts.get_typosquatting_domains(domain)

for url in url_list:
    try:
        # Phishing Detection
        result = demo.detect(url)
        
        # Result
        is_accessible = True
        is_phishing = result["is_phishing"]
        time_cost = result["detection_time"]
        target_brand = result["target_brand"]
        object_detection_img_path = result["object_detection_img_path"]

    except Exception as e:
        is_accessible = False
        is_phishing = False
        time_cost = 0
        target_brand = None
        object_detection_img_path = None

    # TODO: use the result in your way














# Phishing URLs
# url = "http://freedirtyshow.com/"
# url = "http://pagerepairservice2022.gq/"
# url = "https://dbs.applerewardsstore.com/#/"
# url = "http://casaelizabeth.com/neon/Webmail/index.html"
# url = "http://secure-support-dhl.com/"
url = "https://23.234.209.237/"
# url = "https://id.facebookbusiness.me/59401920/u.php"
# url = "http://badgeusaxa.com/royalmail/auth/"

# Benign URLs
# url = "https://bhooi.github.io/"
# url = "https://www.google.com/"
# url = "http://dbc.com.sg/"
# url = "http://www.dsb.com.sg"
# url = "http://dbr.com.sg"



# Case 1
# try:
#     # Phishing Detection
#     result = demo.detect(url)
    
#     # Result
#     print(
#         "\nPhishIntention Result for '{}':".format(url),
#         "\nPhishing? {}".format(result["is_phishing"]),
#         "\nTime Cost: {}s".format(result["detection_time"]),
#         "\nTarget Brand: {}\n".format(result["target_brand"]))

# except Exception as e:
#     print(e)


# Case 2
# while True:
#     print()
#     url = input("Input URL: ")
#     try:
#         # Phishing Detection
#         result = demo.detect(url)
        
#         # Result
#         print(
#             "\nPhishIntention Result for '{}':".format(url),
#             "\nPhishing? {}".format(result["is_phishing"]),
#             "\nTime Cost: {}s".format(result["detection_time"]),
#             "\nTarget Brand: {}\n".format(result["target_brand"]))

#     except Exception as e:
#         print(e)


# Case 3

# ts = TypoSquatting()
# js = ts.read_from_json()

# for key in js.keys():
#     for i, item in enumerate(js[key]):
#         url = "https://" + item['domain']
#         try:
#             # Phishing Detection
#             result = demo.detect(url)

#             # Result
#             is_accessible = True
#             is_phishing = result["is_phishing"]
#             time_cost = result["detection_time"]
#             target_brand = result["target_brand"]
#             object_detection_img_path = result["object_detection_img_path"]

#         except Exception as e:
#             is_accessible = False
#             is_phishing = False
#             time_cost = 0
#             target_brand = None
#             object_detection_img_path = None
        
#         js[key][i]['is_accessible'] = is_accessible
#         js[key][i]['is_phishing'] = is_phishing
#         js[key][i]['time_cost'] = time_cost
#         js[key][i]['target_brand'] = target_brand
#         js[key][i]['object_detection_img_path'] = object_detection_img_path

#         print(url, "Done")

# with open(os.path.join(ts.main_path, "typo_squatting_with_results.json"), 'w') as f:
#     json.dump(js, f, indent=4)
