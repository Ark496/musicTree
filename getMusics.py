"""
JXAが使えないのでglobで再帰的に曲情報取得
"""

import glob
import os
import re
import pygame
import myRBtree02 as rbtree


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
        node.left, flag = rbtree.insert_music_auto(node, x)
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
    node.right, flag = rbtree.insert(node.right, x)
    if node.right is not rbtree.null:
        node.right.parent = node
    return rbtree.balance_insert_right(node, flag)

def music_name(musicfilename):
    return musicfilename.split("/")[-1]

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
    print("{} vs\n\t{}".format(music_name(node.data),music_name(x)))
    print("f vs j")
    while(1):
        a = input("操作 --->")
        if a is 'f' :
            ret = 0  # 0を返す
            break
        elif a is 'j':
            ret = 1 #1を返す
            break
        elif a is 'r':
            print("{} play".format(node.data.split("/")[-1]))
            play(node.data)
        elif a is 'u':
            print("{} play".format(node.data.split("/")[-1]))
            play(x)
        elif a is 'q':
            pygame.mixer.music.stop() # 再生の終了
        elif a is 'p':
            rbtree.print_node(node, 2)
        elif a is 'fall':
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
        
if __name__ == "__main__":
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
    #globで曲を取得
    musicFld = "/Users/ark/Music/iTunes/iTunes Media/Music/"
    fileList = glob.glob(musicFld+"**/*.mp3",recursive=True)
    
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
        print("{0}/{1}終了({2:.3f}%)".format(i, len(fileList), i/len(fileList)))
        music_save(root,outputfld+sortedMusicsTxt)
        print("---------------------")
        #a = input("終わりますか?(何か入力で終了) -->")
        #if len(a):
            #break
    #全てをプリント
    rbtree.print_node(root,2)
    #全てをリストとして取得


    

