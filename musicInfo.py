# coding: utf-8

# 楽曲再生
#楽曲情報取得

import os
import time
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import cv2
import io
from PIL import Image
import numpy as np
import subprocess
import sys
import pandas as pd
import fileExistCheck
import random
#import vlc
class musicJson(object):
	"""docstring for musicJson
	iTunesから取得したjsonから曲をDataFrameで取得し、1曲ずつmusInfo型で返す
	"""
	#それぞれのユーザーによってフォルダ名は変わる
	def __init__(self, path):
		self.musicfld = "/Users/ark/Music/iTunes/iTunes Media/Music/"
		"""
		iTunesから取得したjsonをロードする。
		ファイルがなければ作り、あればロードする。
		まずは取得から
		"""
		super(musicJson, self).__init__()
		self.arg = path
		if os.path.isfile("./{}.json".format(path)):
			print("{}.json は存在します".format(path))
		else:
			print("{}.json が存在しないので作成します".format(path))
			try:
				resultJson = subprocess.check_output(["osascript", "-l","JavaScript", "getAllTracks.js"])
			except:
				print("コマンド入力失敗")
				sys.exit()
			#取得できたら保存する
			with open("./"+path+".json", mode='bw') as f:
			    f.write(resultJson)

			if os.path.isfile("./{}.json".format(path)):
				print("{}.json作成成功".format(path))
			else:
				print("{}.json作成失敗".format(path))
				print("終了します")
				sys.exit()
		with open("./"+path+'.json',"r") as f:
			self.df = pd.read_json(f)#.set_index("id")
		#print(df.sample(5))
		#print(self.arg)

	def maxIndex(self):
		return max(self.df.index)

	def getMusicInfo(self,ind):
		"""
		indexに対応するpathを入手し、それをdfにぶちこみつつ
		musInfo型の曲を返す
		"""
		#musicFilePath列が存在し、
		#すでにdf["musicFilePath"]にパスが入っていたら
		if "musicFilePath" in self.df.columns:
			print("te")
			print(self.df.loc[ind,"musicFilePath"])
			print("te")
		else:
			print("?")
		if "musicFilePath" in self.df.columns and self.df.loc[ind,"musicFilePath"]:
			print("すでに取得できています")
			return musInfo(self.df.loc[ind,"musicFilePath"])
		else:
			gettable,path = fileExistCheck.fileCheck(self.df.loc[ind,:],self.musicfld)
			if gettable:
				#pathが入手できていたら
				self.df.loc[ind,"musicFilePath"] = path
				return musInfo(path)
			else:
				#楽曲が存在しない
				print("取得不可: {}".format(path[0]))
				return 0
		pass

		
# 節
class musInfo:
	def __init__(self, path):
		print(path)
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
			#pictureのpath保存
			#フォルダ作成
			try:
				os.mkdir("./pictures/")
			except FileExistsError:
				pass
			self.picpath = "./pictures/{0}.jpg".format(self.title)
			cv2.imwrite(self.picpath,self.img_numpy_bgr)
		#再生準備
		self.p = vlc.MediaPlayer()
		print(self.path)
		self.p.set_mrl(self.path)

	def play(self,rate = -1,msec = -1):
		if rate >= 0:
			#rateをもとに再生
			self.p.set_time(int(self.length * rate * 1000))
		elif msec >= 0:
			#msecから再生
			self.p.set_time(msec) #ms
		else:
			pass
		rest = self.length - self.p.get_time()	
		if self.p.is_playing():
			self.p.pause()
		else:
			self.p.play()

		#残り時間を返す
		return rest+1
	def pause(self):
		if self.p.is_playing():
			self.p.pause()

if __name__ == '__main__':
	test01 = musicJson("test")
	#曲の取得
	test = test01.getMusicInfo(random.randrange(0,test01.maxIndex()))
	#test = test01.getMusicInfo(2000)
	if test:
		print(test)
		rest = test.play(msec = 0)
		time.sleep(rest)
	else:
		print("取得不可")
	"""
	mp3以外のファイルであっても楽曲情報の取得ができて再生できないとだめじゃん
	"""
	"""
	print(test.length)
	rest = test.play(msec = 95000)
	print("{}秒間再生".format(rest))
	time.sleep(rest)
	"""
	#とりあえず再生
	"""
	path = r"/Users/arc/Music/iTunes/iTunes Media/Music/福山雅治/ガリレオ オリジナルサウンドトラック/06 KISSして ～epilogue～ (solo piano ver.).mp3"
	test = musInfo(path)
	print(test.length)
	rest = test.play(msec = 95000)
	print("{}秒間再生".format(rest))
	time.sleep(rest)
	"""
