# -*- coding: utf-8 -*-

import os,sys
#import eyed3 as eyeD3
import wave
import pygame.mixer
import time
import myRBtree02 as rb
import json
import csv
import random
# 終端
#null = None

# 色
BLACK = 0
RED = 1

def getFilename(TARGETDIR):
	pathlist=[];
	#TARGETDIR以下のフォルダとファイルを列挙
	for root,dirs,files in os.walk(TARGETDIR):
		a=0
		#各フォルダのファイルを列挙
		for file in files:
			#ファイルの絶対パス取得
			path = os.path.join(root,file)
			#mp3かm4aのファイルを取得
			#if path.endswith(".mp3") | path.endswith("m4a"):
			if path.endswith(".mp3"):
				pathlist.append(path);
				a=a+1
	return pathlist

#change allpath -> lastname
def getmusicname(path):
	#print path
	temp="";
	for i in path:
		#print i

		if i == "\\":
			temp = "";
		else:
			try:
				sys.stdout.write(i+"\b\b")
				temp = temp+i
			except:
				temp = temp+'_'
	temp = temp.rstrip(".mp3")
	temp = temp.rstrip(".m4a")

	temp = temp.lstrip("0")
	for i in range(1,3):
		temp = temp.lstrip(str(i)+"-")
	temp = temp.lstrip("0")
	for i in range(1,30):
		temp = temp.lstrip(str(i))
	temp = temp.lstrip(" ")
	return temp;

# os check
def checkOS():
	return sys.platform

def playMusic(x):
	#print x["path"]
	print(x["music"])
	#windows:pygame
	if checkOS() == "win32":
		pygame.mixer.init()
		try:
			pygame.mixer.music.load(x["path"].encode("utf-8"))
			pygame.mixer.music.play(0,10)
		except:
			print("Maybe [%s] cannot be played on this OS"%x["music"])
	else:
		#速度変更とかできるけどどうする
		#print(type(x["path"]))
		command = "afplay "+x["path"].replace(" ","\\ ")
		print(command)
		#os.system(command)

# user decision
def dicision(node, x):
	#print node
	#print x
	print(u'(0):%s\n(1):%s'%(node.data["music"],x["music"]))
	print(u'(2):再生(0)\n(3):再生(1)\n(4):一時停止\n(5):一時停止解除')
	while(True):
		inputstr= input()
		if(inputstr== "0"):
			return False
		elif(inputstr== "1"):
			return True
		elif(inputstr== "2"):
			#音楽再生
			playMusic(node.data)
			pass
		elif(inputstr== "3"):
			playMusic(x)
			pass
		elif(inputstr== "4"):
			pygame.mixer.music.pause();
		elif(inputstr== "5"):
			pygame.mixer.music.unpause();
		else:
			pass	

# 挿入
def musicinsert(node, x, func):
	if node is rb.null: 
		return rb.Node(x), False
	if func(node,x):
		node.left,flag = musicinsert(node.left,x,func)
		return rb.balance_insert_left(node, flag)
	else:
		node.right, flag = musicinsert(node.right, x,func)
		return rb.balance_insert_right(node, flag)
	return node, True
# 木の表示
def print_node_music(node, n):
	color = ('B', 'R')
	if node is not rb.null:
		print_node_music(node.left, n + 1)
		print('    ' * n, color[node.color],node.data["music"])
		print_node_music(node.right, n + 1)

def addCategory(categorystr,category,music,num):
	#numはカテゴリ数。0だといくつでも入れられる。ジャンルの場合は1つでよくね…?
	while True:
		#numがmusic[categorystr]以下だったら終了
		if not categorystr in music:
			music[categorystr]=[]
		if num == 0:
			pass
		elif num <= len(music[categorystr]):
			break

		#まだcategoryに入力可能
		#カテゴリ追加が以上であるか聞く
		#print len(music[categorystr])
		if len(music[categorystr])>=1:
			print(u"now [%s] have..."%music["music"])
			for i in music[categorystr]:
				print(category[i])
			#print u"Wat is [%s]'s "%(music["music"])+categorystr+u" ?"
			sys.stdout.write(u"append "+categorystr+u" is over?(何か入力したら終了):")
			if input()!= "":
				break
		while True:
			#既存カテゴリを表示
			for i in range(len(category)):
				print("("+str(i)+")",category[i])
			#追加する選択肢
			print(u"(999):other "+categorystr)
			inputstr = input()
			#print type(input)
			if inputstr == "":
				continue
			inputnumber = int(inputstr)
			if not inputnumber in range(len(category)):
				if inputstr== 999:
					#add janl
					sys.stdout.write (u'what is the '+categorystr+u" ?:")
					inputstr = input()
					#janlリストにジャンル追加
					if inputstr!= "":
						category.append(input)
				continue
			else:
				music[categorystr].append(input)
				music[categorystr]=list(set(music[categorystr]))
				break
				#print u"[%s]'s "+categorystr+u" is [%s]"%(music["music"],category[music[categorystr]])
	return music

# 終了かタグ及びジャンル追加
def addTags(music,janl,tag):
	print(u'next:%s'%(music["music"]))
	sys.stdout.write(u'何かを入力したら終了:')
	inputstr = input()
	if inputstr!= "":
		#終了フラグ
		return music,True
	music = addCategory("janl",janl,music,1)
	music = addCategory("tag",tag,music,0)
	#タグ追加,ジャンルを関数化して流用も視野
	return music,False

#入力ファイルソート用関数:辞書内の"rank"要素をもとにソート
def sortByRank(node,x):
	if node.data["rank"] > x["rank"]:
		return True
	else:
		return False

def loadfile(root):
	#ファイルをロードするか選択
	#sys.stdout.write(u)
	fn = input("ファイルをロードしますか(ロードする場合はファイル名を拡張子抜きで):")
	if fn != "":
		#(ロードするファイルは木構造のファイル、残りの楽曲ファイル、ジャンルファイル)
		#ロードする場合
		#ファイル名選択(3つのファイルは拡張子以外同じものとする)
		#木構造ファイル呼び出し
		with open(fn+'.json', 'r') as f:
			read_dic = json.load(f)
		#木に挿入 
		#root = rb.make_null();
		for i in read_dic:
			root, _ = musicinsert(root, i, sortByRank)
			root.color = BLACK
			rb.check_rbtree(root)		
		#list化(この時追加した番号はint型か疑問→str型でも比較したら同じ結果なのでは?->桁が違ったら比較できなかった。)
		#木に挿入。この場合前に追加した番号をもとに追加していく
		#残りの楽曲ファイルをロードし、Lとする
		with open(fn+'_lest.json', 'r') as f:
			L = json.load(f)
		#ジャンル読み込み
		with open(fn+'_jnl.json', 'r') as f:
			janl = json.load(f)
		#タグ読み込み
		with open(fn+'_tag.json', 'r') as f:
			tag = json.load(f)
		print_node_music(root,0)
	else:
		#ロードしない場合
		#L=getFilename(u"C:\\Users\\ark\\Music\\iTunes\\iTunes Media")
		#L = getFilename("~/Music/iTunes/iTunes Media")
		L = getFilename("/Users/arc/Music/iTunes/iTunes Media")
		#L=getFilename(u"~/Desktop/testmusic")
		janl = []
		tag = []
	return root,L,janl,tag,fn

def savefile(root,L,lastpath,janl,tag,fn):
	if lastpath == "":
		#(deleteとか含めていくと考えること増える気がするけど暫定的にこれで)
		print(u"多分変更箇所がありません C U again!")
		return
	#出力ファイル名設定
	sys.stdout.write(u"出力ファイル名を入力(無入力だと入力ファイルと同様かsampleになります):")
	inputstr= input()
	if inputstr== "":
		if fn == "":
			fn = "sample"
	else:
		fn = input
	#木の要素一つ一つに番号追加
	ranking = rb.output_node(root)
	print(ranking)
	i = 0
	for j in ranking:
		j["rank"]=i
		i=i+1
	#json形式で木を出力
	#print(ranking)
	with open(fn+'.json', 'w') as f:
		json.dump(ranking, f, sort_keys=True, indent=4)
	#fileから未挿入なので別ファイルに出力。ここでjson形式にした方がいのか疑問。
	#まず配列から曲を削除
	for i in range(L.index(lastpath)):
		del L[0]
	#csvに保存
	with open(fn+'_lest.json', 'w') as f:
		json.dump(L, f, sort_keys=True, indent=4)
	#なぜかというと曲挿入をすべて行わないまま木構造内の曲を削除するときに
	#Lの末尾に挿入したいのだが、その時に形式が合わないと問題が生じる恐れがあるため
	#しかしpathだけをL末尾に追加し、再びジャンルやタグを入れなおせば問題ない感もある。修正もできるし
	#ジャンル書き込み
	with open(fn+'_jnl.json', 'w') as f:
		json.dump(janl, f, sort_keys=True, indent=4)
	with open(fn+'_tag.json', 'w') as f:
		json.dump(tag, f, sort_keys=True, indent=4)

def insertMusic(root,L,janl,tag):
	lastpath = ""
	for file in L:
		print("--------------------------------")
		temp={"path":file,"music":getmusicname(file)};
		#ここから挿入する音楽の再生
		playMusic(temp)
		#ジャンル選択or終了
		temp ,endflag = addTags(temp,janl,tag)
		if endflag:
			lastpath = temp["path"]
			break
		#木に楽曲挿入
		root, _ = musicinsert(root, temp, dicision)
		root.color = BLACK
		rb.check_rbtree(root)

	return root,L,janl,lastpath	

def searchMusic(root,L):
	#音楽を探す。正確には
	'''
	(0)rankをつける
	(1)検索カテゴリの設定
	(2)検索した結果をリスト保存(木のアドレスごと引っ張ってくるから削除も可能)
	(3)結果を表示し、その中から特定のものを
		1.一曲再生、
		2.削除、
			2-1.削除したものはL(未挿入曲リスト)の先頭にpathだけ挿入
			★原作のプログラムではnode.dataを検索していく方式だったからそのままだと使用不可能。
			rankをもとに検索し削除するという方式が現実的かな。新しく作らなきゃいけないけど…
			やろうと思えばmyRBtree02の検索し終わったやつのアドレスをぶっ紺でやれば可能だし短く済む気がする
			多分流用もできるだろう
		3.複数曲再生(曲再生終了したことが理解できるかどうか(macなら可能だった気がする))
			3-1.シャッフル再生、
			3-2.順に再生
		4.★評価表示(全体の曲数をもとに)
	★検索結果のリストはmainには返さない
	'''
	return
def Countmusic(L):
	mp3=0
	m4a=0
	for m in L:
		if "mp3" in m:
			mp3 = mp3+1
		elif "m4a" in m:
			m4a = m4a+1
		else:
			print("?")
	print("mp3:%d,m4a:%d,all:%d"%(mp3,m4a,mp3+m4a))

if __name__ == '__main__':
	#os.system("dir "+TARGETDIR)
	root = rb.make_null()
	#print root is rb.null
	while True:
		try:
			root,L,janl,tag,fn=loadfile(root)
			break
		except:
			print("ファイルの取得に失敗しました")
			continue
	lastpath = ""
	print(L)
	#曲を挿入するか検索するか評価で並べるかを選択させる
	while True:
		print("What would u like to do?")
		print("(0)Insert music")
		print("(01)Insert music(shuffle music)")
		print("(1)Delete music")
		print("(2)Search by Title Tag or Janl")
		print("(3)Print nodes of music")
		print("(4)Count mp3 or m4a")
		print("(999)save + exit")
		inputstr = input("")
		if inputstr == "0":
			#挿入させる場合
			root,L,janl,lastpath = insertMusic(root,L,janl,tag)
		elif inputstr =="01":
			random.shuffle(L)
			root,L,janl,lastpath = insertMusic(root,L,janl,tag)
		elif inputstr == "2":
			searchMusic(root)
		elif inputstr == "3":
			print_node_music(root,0)
		elif inputstr == "4":
			Countmusic(L)
		elif inputstr == "999":
			break

	savefile(root,L,lastpath,janl,tag,fn)
