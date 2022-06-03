import matplotlib
from phishintention.phishintention_main import test

matplotlib.use('Agg')
import time

import matplotlib.pyplot as plt
from phishintention.phishintention_config import load_config

from demo.crawler import *


class PhishIntentionDemo:
    def __init__(self, args=None, cfg_path=None, demo_path=None):

        # Crawler initialzation
        self.crawler = Crawler()
        self.cpu = args.cpu

        # PhishIntention initialzation (Use full model)
        self.cfg_path = None # None means use default config.yaml
        self.AWL_MODEL, self.CRP_CLASSIFIER, self.CRP_LOCATOR_MODEL, self.SIAMESE_MODEL, self.OCR_MODEL, self.SIAMESE_THRE, self.LOGO_FEATS, self.LOGO_FILES, self.DOMAIN_MAP_PATH = load_config(self.cfg_path, cpu=self.cpu, reload_targetlist=True)
    
    def detect(self, url):
        """
        :param url 
        :return: 
        """
        start_time = time.time()
        # Step 1: Crawl screenshot/html code on-the-fly
        crawl_result = self.crawler.crawl(url)
        if crawl_result is None:
            return
        url_folder_path = crawl_result["url_folder_path"]
        screenshot_path = crawl_result["screenshot_path"]
        # Step 1 ends

        # Step 2: PhishIntention inference
        phish_category, pred_target, plotvis, siamese_conf, dynamic, _, pred_boxes, pred_classes = test(url, screenshot_path,
                                                                      self.AWL_MODEL, self.CRP_CLASSIFIER, self.CRP_LOCATOR_MODEL, self.SIAMESE_MODEL, self.OCR_MODEL, self.SIAMESE_THRE, self.LOGO_FEATS, self.LOGO_FILES, self.DOMAIN_MAP_PATH)

        # print('Phishing (1) or Benign (0) ?', phish_category)
        # print('What is its targeted brand if it is a phishing ?', pred_target)
        # print('What is the siamese matching confidence ?', siamese_conf)
        # print('Where are the predicted bounding boxes (in [x_min, y_min, x_max, y_max])?', pred_boxes)
        plt.imshow(plotvis[:, :, ::-1])
        plt.title("Predicted screenshot with annotations")
        # plt.show()
        # Step 2 ends

        # plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        object_detection_img_path = os.path.join(url_folder_path, "object_detection.png")
        plt.savefig(object_detection_img_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
        
        end_time = time.time()

        return {
            "is_phishing": bool(phish_category), 
            "target_brand": pred_target, 
            "object_detection_img_path": object_detection_img_path,
            "siamese_conf": siamese_conf,
            "detection_time": end_time - start_time
        }
