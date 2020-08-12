"""
JXAが使えないのでglobで再帰的に曲情報取得
"""

import glob
import os
import re
import pygame
import myRBtree02 as rbtree
import random
import json

def insert_music(node, x):
    if node is rbtree.null:
        return rbtree.Node(x), False
    #nodeの方が好きなら0を返し、そうでないなら1を返す
    evaluate = controller(node,x)
    if evaluate == 1:
        node.left, flag = insert_music(node.left, x)
        if node.left is not rbtree.null:
            node.left.parent = node
        return rbtree.balance_insert_left(node, flag)
    elif evaluate == 0:
        node.right, flag = insert_music(node.right, x)
        if node.right is not rbtree.null:
            node.right.parent = node
        return rbtree.balance_insert_right(node, flag)
    elif evaluate == 999:
        #最下位にする
        node.left, flag = insert_music_auto(node, x)
        if node.left is not rbtree.null:
            node.left.parent = node
        return rbtree.balance_insert_left(node, flag)
    return node, True

def insert_music_auto(node,x):
    """
    好き=小さいとする。
    xは常にnode.dataよりも大きいとして挿入
    """
    if node is rbtree.null:
        return rbtree.Node(x), False
    node.right, flag = insert_music_auto(node.right, x)
    if node.right is not rbtree.null:
        node.right.parent = node
    return rbtree.balance_insert_right(node, flag)

def music_name(musicfilename,num):
    """
    musicfilename: フルパス。最後に曲名。最後から2番目にアルバム名
    num: -1なら曲名。-2ならアルバム名
    """
    return musicfilename.split("/")[num].replace(".wav","")

def controller(node,x):
    """
    入力されたアルファベットによって評価を変える
    f:leftに移動=現在の曲が好きではない
    j:rightに移動=現在の曲が好き
    r:leftを再生
    u:rightを再生
    p:現在の木の状況を表示
    q:停止
    fとj以外はループする
    fall:最下位にする#未実装
    """
    ret = 1
    #状況を表示
    while(1):
        print("{}({}) vs\n\t{}({})".format(music_name(node.data,-1),music_name(node.data,-2),music_name(x,-1),music_name(x,-2)))
        print("f vs j")
        a = input("操作 --->")
        if a == 'f' :
            ret = 0  # 0を返す
            break
        elif a == 'j':
            ret = 1 #1を返す
            break
        elif a == 'r':
            print("{} play".format(node.data.split("/")[-1]))
            play(node.data)
        elif a == 'u':
            print("{} play".format(node.data.split("/")[-1]))
            play(x)
        elif a == 'q':
            pygame.mixer.music.stop() # 再生の終了
        elif a == 'p':
            rbtree.print_node(node, 2)
        elif a == 'fall':
            ret = 999
            break
    return ret
def play(filename):
    print("再生->{}".format(filename.split("/")[-1]))
    pygame.mixer.music.stop()               # 再生の終了
    pygame.mixer.music.load(filename)     # 音楽ファイルの読み込み
    pygame.mixer.music.play(1)

def music_save(node,filename):
    """
    オートセーブ
    """
    now = node.min()
    sortingMusicList = []
    while now is not rbtree.null:
        try:
            #print("{}".format(music_name(now.data)))
            sortingMusicList.append(now.data)
            now = now.next()
        except:
            break
    with open(filename, mode='w') as f:
        f.write('\n'.join(sortingMusicList))
    return len(sortingMusicList)

def music_save_json(node,janl,filename,musDict):
    """
    jsonとしてオートセーブ
    """
    now = node.min()
    sortingMusicList = []
    #好きな順に曲をリストに入れる
    while now is not rbtree.null:
        try:
            #print("{}".format(music_name(now.data)))
            sortingMusicList.append(now.data)
            now = now.next()
        except:
            break
    musDict[janl]["sorted_music"] = sortingMusicList
    with open(filename,"w") as f:
        json.dump(musDict,f,indent = 4, ensure_ascii=False)
    return musDict,len(musDict[janl]["sorted_music"])
    
    


def sortMusics_fromTxt():
    outputfld = "./output/"
    try:
        os.mkdir(outputfld)
    except:
        pass
    #既存曲順位リスト取得
    #ソート済曲リストファイル名
    sortedMusicsTxt = "sortedMusics.txt"
    #もし存在してたらロード
    if os.path.exists(outputfld+sortedMusicsTxt):
        with open(outputfld+sortedMusicsTxt) as f:
            sortedMusics = f.read().splitlines()
    else:
        sortedMusics = []
    #listから木を構成
    root = rbtree.make_null()
    for f in sortedMusics:
        root,_ = insert_music_auto(root,f);
        root.color = rbtree.BLACK
        rbtree.check_rbtree(root)
        #rbtree.print_node(root,1)
        #print("---------")
    #globで曲を取得
    musicFld = "/Users/arc/Music/iTunes/iTunes Media/Music/"
    fileList = glob.glob(musicFld+"**/*.wav",recursive=True)
    random.shuffle(fileList)
    #プレイヤーを初期化
    pygame.mixer.init(frequency=44100)    # 初期設定
    #1曲ずつ評価
    for i,f in enumerate(fileList):
        if f in sortedMusics:
            print("{}はsort済".format(f.split("/")[-1]))
            continue
        #とりあえず再生
        play(f)
        #曲を挿入
        root,_ = insert_music(root,f)
        root.color = rbtree.BLACK
        rbtree.check_rbtree(root)
        num = music_save(root,outputfld+sortedMusicsTxt)
        print("{0}/{1}終了({2:.3f}%)".format(num, len(fileList), num/len(fileList)*100))
        print("---------------------")
        #a = input("終わりますか?(何か入力で終了) -->")
        #if len(a):
            #break
    #全てをプリント
    rbtree.print_node(root,2)
    #全てをリストとして取得

if __name__ == "__main__":
    outputfld = "./output/"
    try:
        os.mkdir(outputfld)
    except:
        pass
    #ソート済曲リストファイル名
    sortedMusicsfile = "janledMusics.json"
    #もし存在してたらロード
    if os.path.exists(outputfld+sortedMusicsfile):
        with open(outputfld+sortedMusicsfile) as f:
            musicDic = json.load(f)
    else:
        musicDic = {}
    #ジャンル名を取得
    janls = list(musicDic.keys())
    #初期状態だったら適当にジャンルを入力
    if not len(janls):
        janls = ["music_game","game","j-pop","classic","jazz","study","soundtrack","other"]
        for ja in janls:
            musicDic[ja] = {"folderPath":[],"musics":[],"sorted_musics":[]}
    print(janls)
    #全ジャンルについてフォルダを調べ、なくなっていたら除去
    for j in janls:
        for fld in reversed(musicDic[j]["folderPath"]):
            if not os.path.exists(fld):
                musicDic[j]["folderPath"].remove(fld)
    #曲の入っているフォルダを取得
    musicFld = "/Users/arc/Music/iTunes/iTunes Media/Music/"
    fileList = glob.glob(musicFld+"**/",recursive=True)
    album_list = []
    for f in fileList:
        #中に曲が入っているフォルダをalbum_listに追加
        musicFileList = os.listdir(f)
        flag = 0
        for ff in musicFileList:
            if ff.split(".")[-1] in ["wav","mp3","m4a"]:
                flag = 1
                break
        if not flag: continue
        album_list.append(f)

    #musicDicの全ジャンルの中にそのフォルダが入っていなければ分類
    for al in album_list:
        flag = 0 #どこにも入っていない場合0を示すフラグ
        for k in janls:
            if al in musicDic[k]["folderPath"]:
                flag = 1
                usekey = k
                break
        if flag: 
            """
            既に登録されている場合
            """
            a = janls.index(usekey)
        else:
            """
            新規登録アルバム
            """
            for i,ja in enumerate(janls):
                print("{}.{}".format(i,ja))
            a = int(input("{}\nはどれ->".format(al)))
            if a >= len(janls):
                janls.append(input("新ジャンルは->"))
                a = len(janls)-1
                musicDic[janls[a]] = {"folderPath":[],"musics":[],"sorted_musics":[]}
            musicDic[janls[a]]["folderPath"].append(al)
        for f in os.listdir(al):
            if not al + f in musicDic[janls[a]]["musics"]:
                """
                ジャンル名の中に入っていなかったら
                """
                if not al + f in musicDic[janls[a]]["sorted_musics"]:            
                    if ".wav" in f:
                        musicDic[janls[a]]["musics"].append(al+f)
        with open("./output/janledMusics.json","w") as f:
            json.dump(musicDic,f,indent = 4, ensure_ascii=False)    
    #どのジャンルをそーとするか選択
    for i,ja in enumerate(janls):
        print("{}.{}(ソート済{}/{})".format(i,ja,len(musicDic[ja]["sorted_musics"]),len(musicDic[ja]["musics"])))
    a = 1000
    while a >= len(janls):
        a = int(input("どのジャンルの曲をソートしますか->"))
    print("{}ジャンルをソートします".format(janls[a]))
    #ソート済曲リストと全曲リストを取得

    #選択したジャンルの全曲リスト全てにアクセスできるか確認
    for musicFile in reversed(musicDic[janls[a]]["musics"]):
        if not os.path.exists(musicFile):
            print("{}が見つからなかったので除去".format(musicFile))
            musicDic[janls[a]]["musics"].remove(musicFile)    
    #ソート済曲リストの内容が全曲リストに含まれているかを確認。全曲リストにないものは除去
    for musicFile in reversed(musicDic[janls[a]]["sorted_musics"]):
        if not musicFile in musicDic[janls[a]]["musics"]:
            print("{}が見つからなかったので除去".format(musicFile))
            musicDic[janls[a]]["sorted_musics"].remove(musicFile)
    #2つの配列を使ってソート開始。
    #listから木を構成
    root = rbtree.make_null()
    for f in musicDic[janls[a]]["sorted_musics"]:
        root,_ = insert_music_auto(root,f);
        root.color = rbtree.BLACK
        rbtree.check_rbtree(root)
    #プレイヤーを初期化
    pygame.mixer.init(frequency=44100)    # 初期設定
    #1曲ずつ評価
    for i,f in enumerate(musicDic[janls[a]]["musics"]):
        if f in musicDic[janls[a]]["sorted_musics"]:
            print("{}はsort済".format(f.split("/")[-1]))
            continue
        #とりあえず再生
        play(f)
        #曲を挿入
        root,_ = insert_music(root,f)
        root.color = rbtree.BLACK
        rbtree.check_rbtree(root)
        #1曲そーとし終わるごとにソート済曲リストを取得し、musicDicを更新してセーブ
        musicDic,num = music_save_json(root,janls[a],outputfld+sortedMusicsfile,musicDic)
        print("{0}/{1}終了({2:.3f}%)".format(num, len(musicDic[janls[a]]["musics"]), num/len(musicDic[janls[a]]["musics"])*100))
        print("---------------------")
    #全てをプリント
    rbtree.print_node(root,2)




    

