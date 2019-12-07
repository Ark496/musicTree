import pandas as pd
import os
import math
import re
"""
day : 20191020
purpose: jsで取得したjsonから作成したcsvをもとに楽曲を再生できるのか
"""
"""
必要な要素
Compilationsかそうでないか] artist?albumArtist?
"Unknown Artist"かどうか artistが空欄？
何枚目のCDか: discNumberとdiscCount(2以上だと上に着く)
CDの中で何番目の曲か: trackNumber(trackCountが2以上とか必要？)
タイトル: name
アルバム名: album
拡張子: ?
"""
def fileCheck(Ser,musicfld = "/Users/arc/Music/iTunes/iTunes Media/Music/"):
	#歌詞が読み込まれてる時があるから変だったら除く
	temp = Ser.copy()
	#print(temp)
	#print(temp["name"])
	if "AACオーディオファイル" in temp["kind"]:
		tail = "m4a"
	elif "MPEGオーディオファイル" in temp["kind"]:
		tail = "mp3"
	elif "Apple Losslessオーディオファイル" in temp["kind"]:
		tail = "m4a"
	else:
		tail = "?"
		print(temp["kind"])
	#先頭にtrackNoが入る
	if math.isnan(temp["discCount"]):
		return False,""
	elif temp["discCount"] > 1:
		trackName = "%d-" %(temp["discNumber"])
	elif temp["discCount"] <= 1: 
		trackName = ""
	else:
		return False,""
	#trackNumber0だったらつけない？
	if math.isnan(temp["trackNumber"]):
		return False,""
	else:
		#print(temp["trackNumber"])
		if temp["trackNumber"] > 0:
			trackName = trackName + "%02d"%(temp["trackNumber"]) +" "
		else:
			pass
	#使用できない文字
	title = temp["name"].replace(":","_").replace('"','_').replace("’",'_').replace("/","_").replace("?","_").replace("“","_").replace("”","_")
	if len(temp["album"]) > 0:
		albumtitle = temp["album"].replace(":","_").replace('"','_').replace("’",'_').replace("/","_").replace("?","_").replace("“","_").replace("”","_")
		#末尾のドットは置換
		albumtitle = re.sub(r'\.$',"_",albumtitle)
	else:
		albumtitle = "Unknown Album"
	#artistはalbumartistが優先される
	if len(temp["albumArtist"])>0:
		#アルバムアーティストに何らかの文字がある
		if temp["albumArtist"] == temp["artist"]:
			#アルバムアーティストとアーティスト名が同じ場合はどちらでもいい
			artistName = temp["artist"]
		elif temp["albumArtist"] in ["V.A.","Various Artists"]:
			#variousArtistだったらcompilationsに
			artistName = "Compilations"
		else:
			#名義が違ったらalbumArtistになる
			artistName = temp["albumArtist"]
	else:
		if len(temp["artist"]) > 0:
			artistName = temp["artist"]
		else:
			artistName = "Unknown Artist"
	artistName = artistName.replace(":","_").replace('"','_').replace("’",'_').replace("/","_").replace("?","_")

	path = "%s%s/%s/%s%s.%s"% (musicfld,artistName,albumtitle,trackName,title,tail)
	compilations_path = "%s%s/%s/%s%s.%s"% (musicfld,"Compilations",albumtitle,trackName,title,tail)
	pathFlag = os.path.exists(path)
	compPathFlag = os.path.exists(compilations_path)
	if not (pathFlag or compPathFlag):
		print("path = {}".format(path))
		return False,[path,compilations_path]
	else:
		if pathFlag:
			print("loaded: {}".format(path))
			return True,path
		else:
			print("loaded: {}".format(compilations_path))
			return True,compilations_path
	pass

def fileChecks(file = "tracks.json"):
	#df = pd.read_csv("./AllTracks.csv")
	#1回CSVにすると歌詞がうざいことになるのでjsonのまま読み込むのが良い
	with open('./_getiTunesInfo/tracks.json',"r") as f:
		df = pd.read_json(f).set_index("id").reset_index(drop = True)
	musicfld = "/Users/arc/Music/iTunes/iTunes Media/Music/"
	count = 0
	getCount = 0
	for i in range(len(df)):
		res,path = fileCheck(df.loc[i,:],musicfld)
		if res:
			count += 1
			getCount += 1
		else:
			count += 1
	print("%d回ミス"% (count))
	print("%d曲中%d曲成功"%(i+1,getCount))
	#print(df.loc[df.album == "洞窟物語",["albumArtist","artist"]])

if __name__ == "__main__":
	fileChecks()
	pass

