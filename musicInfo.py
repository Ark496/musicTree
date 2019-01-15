# coding: utf-8

# 楽曲再生
#楽曲情報取得

import vlc
import os
import time
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import cv2
import io
from PIL import Image
import numpy as np


# 節
class musInfo:
	def __init__(self, path):
		mp3 = MP3(path)
		#曲の属性集
		info = mp3.info
		#曲の情報
		tags = mp3.tags
		artworks = tags.getall('APIC')

		self.title = tags.get('TIT2', 'No title')
		self.album = tags.get('TALB', 'No album title')
		self.artist = tags.get('TPE1', 'No artist name')
		self.track = tags.get('TRAK', 'No track number')
		self.length = info.length
		self.channels = info.channels
		self.bitrate = info.bitrate
		self.sample_rate = info.sample_rate
		self.path = path

		for artwork in artworks:
			#どれが使えるのかわからないから全部出してるけど.dataでいけると思う
			#print("ARTWORK     : {}, {}bytes".format(artwork.mime, len(artwork.data)))
			#cv2.imshow("Read Image",artwork.data)
			self.img_binary = artwork.data
			self.img_binarystream = io.BytesIO(self.img_binary)

			#PILイメージ <- バイナリーストリーム
			self.img_pil = Image.open(self.img_binarystream)
			#print(img_pil.mode) #この段階だとRGBA

			#numpy配列(RGBA) <- PILイメージ
			self.img_numpy = np.asarray(self.img_pil)

			#numpy配列(BGR) <- numpy配列(RGBA)
			self.img_numpy_bgr = cv2.cvtColor(self.img_numpy, cv2.COLOR_RGBA2BGR)

	def play(self,rate = -1,msec = -1):
		p = vlc.MediaPlayer()
		print(self.path)
		p.set_mrl(self.path)
		p.play()
		print("type(self.length): {}".format(type(self.length)))
		if rate >= 0:
			#lengthからの割合
			p.set_time(int(self.length * rate * 1000))
			rest = self.length * (1-rate)	
		elif msec >= 0:
			#msecから再生
			p.set_time(msec) #ms
			rest = self.length - msec/1000
		else:
			rest = self.length
		#残り時間を返す
		return rest+1

if __name__ == '__main__':
	#とりあえず再生
	path = r"/Users/arc/Music/iTunes/iTunes Media/Music/Toby Fox/DELTARUNE Chapter 1 OST/33 THE WORLD REVOLVING.mp3"
	test = musInfo(path)
	print(test.length)
	rest = test.play(msec = 95000)
	print("{}秒間再生".format(rest))
	time.sleep(rest)