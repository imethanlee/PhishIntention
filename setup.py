from setuptools import setup, find_packages
from functools import reduce

version="0.0.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='phishintention',
      version="0.0.0",
      description='phishintention',
      long_description=long_description,
      author='Ruofan Liu',
      author_email='liu.ruofan16@u.nus.edu',
      url='https://github.com/lindsey98/PhishIntention',
      license='Apache License 2.0',
      python_requires='==3.7.*',
      packages=['phishintention', 'phishintention.src',
                'phishintention.src.adv_attack', 'phishintention.src.adv_attack.attack',
                'phishintention.src.AWL_detector_utils', 'phishintention.src.AWL_detector_utils.configs', 'phishintention.src.AWL_detector_utils.configs.bases',
                'phishintention.src.AWL_detector_utils.detectron2_1', 'phishintention.src.AWL_detector_utils.detectron2_1.configs', 'phishintention.src.AWL_detector_utils.detectron2_1.modelling',
                # 'phishintention.src.AWL_detector_utils.output.website_lr0.001',
                'phishintention.src.crp_classifier_utils', 'phishintention.src.crp_classifier_utils.bit_pytorch',
                'phishintention.src.crp_classifier_utils.HTML_heuristic', 'phishintention.src.crp_classifier_utils.output',
                # 'phishintention.src.crp_classifier_utils.output.Increase_resolution_lr0.005',
                'phishintention.src.crp_locator_utils', 'phishintention.src.crp_locator_utils.login_finder',
                'phishintention.src.crp_locator_utils.login_finder.configs', 'phishintention.src.crp_locator_utils.login_finder.configs.bases',
                'phishintention.src.crp_locator_utils.login_finder.detectron2_1',
                'phishintention.src.crp_locator_utils.login_finder.detectron2_1.configs',
                'phishintention.src.crp_locator_utils.login_finder.detectron2_1.modelling',
                # 'phishintention.src.crp_locator_utils.login_finder.output.lr0.001_fintune',
                'phishintention.src.OCR_siamese_utils', 'phishintention.src.OCR_siamese_utils.lib',
                'phishintention.src.OCR_siamese_utils.lib.datasets', 'phishintention.src.OCR_siamese_utils.lib.evaluation_metrics', 'phishintention.src.OCR_siamese_utils.lib.loss', 'phishintention.src.OCR_siamese_utils.lib.models', 'phishintention.src.OCR_siamese_utils.lib.tools', 'phishintention.src.OCR_siamese_utils.lib.utils',
                'phishintention.src.OCR_siamese_utils.output',
                # 'phishintention.src.OCR_siamese_utils.output.targetlist_lr0.01',
                'phishintention.src.OCR_siamese_utils.siamese_unified',  'phishintention.src.OCR_siamese_utils.siamese_unified.bit_pytorch',
                'phishintention.src.phishpedia_siamese.siamese_retrain',
                'phishintention.src.phishpedia_siamese.siamese_retrain.bit_pytorch',
                'phishintention.src.util',
                'phishintention.src.phishpedia_siamese',
                # 'phishintention.src.phishpedia_logo_detector', 'phishintention.src.phishpedia_logo_detector.configs', 'phishintention.src.phishpedia_logo_detector.configs.bases',
                # 'phishintention.src.phishpedia_logo_detector.detectron2_1', 'phishintention.src.phishpedia_logo_detector.output'
                ],
      install_requires=[
            'torchsummary',
            'scipy',
            'tldextract',
            'opencv-python',
            'selenium',
            'helium',
            'selenium-wire',
            'webdriver-manager',
            'pandas',
            'numpy',
            'tqdm',
            'Pillow',
            'pathlib',
            'fvcore',
            'pycocotools',
            'scikit-learn',
            'pyyaml',
            'editdistance'
      ],
      package_data={
            # If any package contains *.txt or *.rst files, include them:
            "": ["*.yaml", "*.pkl", "*.pth", "*.zip", "*.tar", "*.txt"],
      },
      include_package_data=True
      )