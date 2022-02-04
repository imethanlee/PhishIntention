# Global configuration
from src.OCR_aided_siamese import *
from src.AWL_detector import *
from src.crp_classifier import *
from src.util.chrome import *
from src.crp_locator import *
import helium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

def driver_loader():
    '''
    load chrome driver
    :return:
    '''

    options = initialize_chrome_settings(lang_txt='./src/util/lang.txt')
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
    capabilities["unexpectedAlertBehaviour"] = "dismiss"  # handle alert
    capabilities["pageLoadStrategy"] = "eager"  # eager mode #FIXME: set eager mode, may load partial webpage

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                              desired_capabilities=capabilities,
                              chrome_options=options)
    driver.set_page_load_timeout(60)  # set timeout to avoid wasting time
    driver.set_script_timeout(60)  # set timeout to avoid wasting time
    helium.set_driver(driver)
    return driver

# element recognition model
ele_cfg, ele_model = element_config(rcnn_weights_path = './src/AWL_detector_utils/output/website_lr0.001/model_final.pth',
                                    rcnn_cfg_path='./src/AWL_detector_utils/configs/faster_rcnn_web.yaml')

cls_model = credential_config(checkpoint='./src/crp_classifier_utils/output/Increase_resolution_lr0.005/BiT-M-R50x1V2_0.005.pth.tar',model_type='mixed')

login_cfg, login_model = login_config(
    rcnn_weights_path='./src/crp_locator_utils/login_finder/output/lr0.001_finetune/model_final.pth',
    rcnn_cfg_path='./src/crp_locator_utils/login_finder/configs/faster_rcnn_login_lr0.001_finetune.yaml')

# siamese model
print('Load protected logo list')
pedia_model, ocr_model, logo_feat_list, file_name_list = phishpedia_config_OCR(num_classes=277,
                                                weights_path='./src/OCR_siamese_utils/output/targetlist_lr0.01/bit.pth.tar',
                                                ocr_weights_path='./src/OCR_siamese_utils/demo_downgrade.pth.tar',
                                                targetlist_path='./src/phishpedia_siamese/expand_targetlist/')
print('Finish loading protected logo list')

siamese_ts = 0.87 # FIXME: threshold is 0.87 in phish-discovery?

# brand-domain dictionary
domain_map_path = './src/phishpedia_siamese/domain_map.pkl'

