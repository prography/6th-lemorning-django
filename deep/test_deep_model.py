import os
import time
import django

os.environ.setdefault('DJANGO_SETTING_MODULE', 'config.dev')
django.setup()

import numpy as np

from deep.model import DeepModel

if __name__ == '__main__':
    model = DeepModel()
    path_audio = 'data/audio/TRWJAZW128F42760DD_test.mp3'

    # 1. get info (features, tags)
    print('1. Extract info(feat, tag)')
    start_time = time.time()
    feats, tags = model.extract_info(path_audio, mode='both', topN=5)
    end_time = time.time()
    print(feats, tags)
    print('inference time : {}'.format(end_time - start_time))
    print()

    # 2. get info (features)
    print('2. Extract feature')
    feats = model.extract_info(path_audio, mode='feature')
    print(feats)
    print()

    # 3. get info (tags)
    print('3. Extact tags')
    tags = model.extract_info(path_audio, mode='tag', topN=5)
    print(tags)
