# -*- coding:utf-8 -*-

import vlc
import os
import time
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import cv2
import io
from PIL import Image
import numpy as np
def show_id3_tags(file_path):
    tags = EasyID3(file_path)
    print(tags.pprint())


def getMP3info(path):
	mp3 = MP3(path)
	info = mp3.info
	print("LENGTH      : {}".format(info.length))
	print("CHANNELS    : {}".format(info.channels))
	print("BITRATE     : {}".format(info.bitrate))
	print("SAMPLE RATE : {}".format(info.sample_rate))

	tags = mp3.tags
	print("TITLE       : {}".format(tags.get('TIT2', 'No title')))
	print("ALBUM       : {}".format(tags.get('TALB', 'No album title')))
	print("ARTIST      : {}".format(tags.get('TPE1', 'No artist name')))
	print("TRACK       : {}".format(tags.get('TRAK', 'No track number')))

	artworks = tags.getall('APIC')
	for artwork in artworks:
		print("ARTWORK     : {}, {}bytes".format(artwork.mime, len(artwork.data)))
		#print(artwork.keys())
		#print(type(artwork.data))
		#cv2.imshow("Read Image",artwork.data)
		img_binary = artwork.data
		img_binarystream = io.BytesIO(img_binary)

		#PILイメージ <- バイナリーストリーム
		img_pil = Image.open(img_binarystream)
		print(img_pil.mode) #この段階だとRGBA

		#numpy配列(RGBA) <- PILイメージ
		img_numpy = np.asarray(img_pil)

		#numpy配列(BGR) <- numpy配列(RGBA)
		img_numpy_bgr = cv2.cvtColor(img_numpy, cv2.COLOR_RGBA2BGR)
		cv2.imwrite("./test.jpg",img_numpy_bgr)
		#表示確認
		#cv2.imshow('window title', img_numpy_bgr)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()

if __name__ == '__main__':
	#とりあえず再生
	#path = r"/Users/arc/Music/iTunes/iTunes Media/Music/Toby Fox/DELTARUNE Chapter 1 OST/33 THE WORLD REVOLVING.mp3"
	path = r"/Users/arc/Music/iTunes/iTunes Media/Music/Compilations/beatmania IIDX 20 tricoro ORIGINAL SOUNDTRACK Vol. 1 [Disc 1]/1-31 Breaking Dawn.m4a"
	#ファイルがあるか確認
	"""
	if os.path.exists(path):
		print("{0} はあります".format(path))
	else:
		print("{0} はありません".format(path))
	"""
	show_id3_tags(path)

	getMP3info(path)

	p = vlc.MediaPlayer()
	p.set_mrl(path)
	p.play()
	p.set_time(90000) #ms
	time.sleep(100)
