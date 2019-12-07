# coding: utf-8
"""
20191207
方針
GUI抜きで動作するクラスを作る。GUIと合成するだけの状態にしておく
必要な要素
曲の読み込み: jsonでiTunesのファイルを読みだして、それぞれの曲のpath取得。多分pathはjsonに入れて新たに保存できたほうがいい
曲の再生
次の曲に行く
曲の情報提供
クラスは二つ必要?
曲情報が入ったjsonを保存しておく領域
実際に再生する曲のクラス
"""

class PlayingMusic(object):
	"""docstring for PlayingMusic"""
	def __init__(self, arg):
		"""
		コンストラクタにはjsonの曲情報を入れて曲のロードを行う
		"""
		super(PlayingMusic, self).__init__()
		self.arg = arg
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
	main()