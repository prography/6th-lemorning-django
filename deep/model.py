import warnings
from .musicnn import models
from .musicnn import configuration as config
import tensorflow as tf
import numpy as np
import librosa
from pydub import AudioSegment
import time
import os
import sys
from io import BytesIO

sys.path.append('deep')

warnings.filterwarnings('ignore')


class DeepModel():
    def __init__(self):
        self.path_model = 'deep/musicnn/MTT_musicnn/'
        self.n_frame_seconds = 3
        self.duration_load_audio = 6
        self.n_frames = librosa.time_to_frames(
            self.n_frame_seconds, sr=config.SR, n_fft=config.FFT_SIZE, hop_length=config.FFT_HOP) + 1

        self.load_model()

    def load_model(self):
        self.labels = np.array(config.MTT_LABELS)
        num_classes = len(self.labels)

        tf.compat.v1.reset_default_graph()

        with tf.name_scope('model'):
            self.x = tf.compat.v1.placeholder(
                tf.float32, [None, self.n_frames, config.N_MELS])
            self.is_training = tf.compat.v1.placeholder(tf.bool)
            y, _, _, _, _, _, _, _, self.feature = models.define_model(
                self.x, self.is_training, 'MTT_musicnn', num_classes)
            self.normalized_y = tf.nn.sigmoid(y)

        self.sess = tf.compat.v1.Session()
        self.sess.run(tf.compat.v1.global_variables_initializer())
        saver = tf.compat.v1.train.Saver()
        saver.restore(self.sess, self.path_model)

    def load_audio_rep(self, audio_file, format='mp3'):

        if isinstance(audio_file, BytesIO):
            assert format == 'wav' or format == 'mp3', '[ERROR] format를 잘못 입력했습니다. 오직 wav, mp3만 가능합니다.'

            audioSegment = AudioSegment.from_file(audio_file, format=format)
            audioSegment = audioSegment.set_channels(1).set_frame_rate(config.SR)
            audio = audioSegment.get_array_of_samples()
            audio = np.array(audio) / (2 ** 15)
        
        if isinstance(audio_file, str):
            assert audio_file.endswith('wav') or audio_file.endswith('mp3'), '[ERROR] wav 혹은 mp3 파일만 가능합니다.'
            audio, sr = librosa.load(audio_file, sr=config.SR, duration=self.duration_load_audio)

        audio_rep = librosa.feature.melspectrogram(y=audio,
                                                   sr=config.SR,
                                                   hop_length=config.FFT_HOP,
                                                   n_fft=config.FFT_SIZE,
                                                   n_mels=config.N_MELS).T
        audio_rep = audio_rep.astype(np.float16)
        audio_rep = np.log10(10000 * audio_rep + 1)

        return audio_rep

    def extract_info(self, audio_file, mode="both", topN=5):

        audio_rep = self.load_audio_rep(audio_file)

        batch = self.batch_data(audio_rep)

        feats = []
        ys = []
        for i in range(batch.shape[0]):
            feat, y = self.sess.run([self.feature, self.normalized_y], feed_dict={
                                    self.x: batch[i:i+1], self.is_training: False})
            feats.append(feat)
            ys.append(y)

        feats = np.concatenate(feats, 0)
        ys = np.concatenate(ys, 0)

        # postprocess
        feats = np.mean(feats, 0)
        mag = np.sqrt(np.sum(feats ** 2))
        feats = feats / mag

        if mode == 'feature':
            return feats

        tags_likelihood_mean = np.mean(ys, axis=0)
        sort_idx = tags_likelihood_mean.argsort()[::-1]
        tags = self.labels[sort_idx][:topN]

        if mode == 'tag':
            return tags

        if mode == 'both':
            return feats, tags

    def batch_data(self, audio_rep):

        # batch it for an efficient computing
        first = True
        # +1 is to include the last frame that range would not include
        last_frame = audio_rep.shape[0]

        for idx, time_stamp in enumerate(range(0, last_frame, self.n_frames)):

            if idx > 4 or time_stamp + self.n_frames > last_frame:
                break

            patch = np.expand_dims(
                audio_rep[time_stamp: time_stamp + self.n_frames, :], axis=0)
            if first:
                batch = patch
                first = False
            else:
                batch = np.concatenate((batch, patch), axis=0)

        return batch
