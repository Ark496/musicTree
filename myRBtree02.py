# coding: utf-8
#
# rbnode.py : 赤黒木用操作関数 (2-3-4 木をベース)
#
#             Copyright (C) 2008 Makoto Hiroi
#
# RBtreeから改造したもの。treeのみの機能は確保してるからお好みで改造しよう
# parent機能追加したところは##ってつけてる
import sys
# 終端
null = None

# 色
BLACK = 0
RED = 1

# 節
class Node:
    def __init__(self, x, color = RED):
        #print("init!")
        self.data = x
        self.color = color
        self.left = null
        self.right = null
        self.parent = null ##

    def root(self):
        if self.parent is null:
            return self
        else:
            return self.parent.root()

    def min(self):
        if self.left is null:
            return self
        else:
            return self.left.min()
    def max(self):
        if self.right is null:
            return self
        else:
            return self.right.max()

    def next(self):
        if self.right is not null:
            return self.right.min()
        x = self
        y = x.parent
        while y is not null and x is y.right:
            x = y
            y = y.parent
        return y

    def previous(self):
        if self.left is not null:
            return self.left.max()
        x = self
        y = x.parent
        while y is not null and x is y.left:
            x = y
            y = y.parent 
        return y

# 終端の設定
def make_null():
    global null
    if null is None:
        null = Node(None, BLACK)
        null.left = None
        null.right = None
        null.parent = None ##
    return null

# 右回転
def rotate_right(node):
    lnode = node.left
    node.left = lnode.right
    lnode.right = node
    lnode.color = node.color
    node.color = RED
    lnode.parent = node.parent ##
    node.parent = lnode ##
    if node.left is not null: ##
        node.left.parent = node ##
    return lnode

# 左回転
def rotate_left(node):
    rnode = node.right
    node.right = rnode.left
    rnode.left = node
    rnode.color = node.color
    node.color = RED
    rnode.parent = node.parent ##
    node.parent = rnode ##
    if node.right is not null: ##
        node.right.parent = node ##
    return rnode

#
# データの探索
#
def search(node, x):
    while node is not null:
        if x == node.data: return True
        elif x < node.data:
            node = node.left
        else:
            node = node.right
    return False

#
# データの挿入
#

# 4node の分割
def split(node):
    node.color = RED
    node.left.color = BLACK
    node.right.color = BLACK

# 左部分木の修正
def balance_insert_left(node, flag):
    if flag: return node, flag
    if node.color == BLACK:
        flag = True
        # 左(赤)の子に赤があるか
        if node.left.right.color == RED:
            node.left = rotate_left(node.left)
        if node.left.left.color == RED:
            # 赤が 2 つ続く
            if node.right.color == RED:
                split(node)
                flag = False
            else:
                node = rotate_right(node)
    return node, flag

# 右部分木の修正
def balance_insert_right(node, flag):
    if flag: return node, flag
    if node.color == BLACK:
        flag = True
        # 右(赤)の子に赤があるか
        if node.right.left.color == RED:
            node.right = rotate_right(node.right)
        if node.right.right.color == RED:
            # 赤が 2 つ続く
            if node.left.color == RED:
                split(node)
                flag = False
            else:
                node = rotate_left(node)
    return node, flag

# 挿入
def insert(node, x):
    if node is null: return Node(x), False
    if x < node.data:
        node.left, flag = insert(node.left, x)
        if node.left is not null: ##
            node.left.parent = node ##
        return balance_insert_left(node, flag)
    elif x > node.data:
        node.right, flag = insert(node.right, x)
        if node.right is not null: ##
            node.right.parent = node ##
        return balance_insert_right(node, flag)
    return node, True

#
# データの削除
#

# 右部分木の修正
def balance_right(node, flag):
    if flag: return node, flag
    if node.left.left.color == BLACK and node.left.right.color == BLACK:
        if node.left.color == BLACK:
            # left is 2node
            node.left.color = RED
            if node.color == BLACK: return node, False
            node.color = BLACK
        else:
            # node is 3node
            node = rotate_right(node)
            node.right, _ = balance_right(node.right, False)
            if node.right is not null: ##
                node.right.parent = node ##
    else:
        # left is 3,4node
        if node.left.right.color == RED:
            node.left = rotate_left(node.left)
        node = rotate_right(node)
        node.right.color = BLACK
        node.left.color = BLACK
    return node, True

# 左部分木の修正
def balance_left(node, flag):
    if flag: return node, flag
    if node.right.left.color == BLACK and node.right.right.color == BLACK:
        # right is 2node
        if node.right.color == BLACK:
            # node is 2node
            node.right.color = RED
            if node.color == BLACK: return node, False
            node.color = BLACK
        else:
            # node is 3node
            node = rotate_left(node)
            node.left, _ = balance_left(node.left, False)
            if node.left is not null: ##
                node.left.parent = node ##
    else:
        # right is 3,4node
        if node.right.left.color == RED:
            node.right = rotate_right(node.right)
        node = rotate_left(node)
        node.left.color = BLACK
        node.right.color = BLACK
    return node, True

# 最小値を探す
def search_min(node):
    while node.left is not null: node = node.left
    return node.data

# 削除
def delete(node, x):
    if node is null: return node, True
    if x == node.data:
        if node.left is null and node.right is null:
            return null, node.color == RED
        elif node.right is null:
            node.left.color = BLACK
            return node.left, True
        elif node.left is null:
            node.right.color = BLACK
            return node.right, True
        else:
            node.data = search_min(node.right)
            node.right, flag = delete(node.right, node.data)
            if node.right is not null: ##
                node.right.parent = node ##
            return balance_right(node, flag)
    elif x < node.data:
        node.left, flag = delete(node.left, x)
        if node.left is not null: ##
            node.left.parent = node ##
        return balance_left(node, flag)
    else:
        node.right, flag = delete(node.right, x)
        if node.right is not null: ##
            node.right.parent = node ##
        return balance_right(node, flag)

#
# 巡回
#
def traverse(node):
    if node is not null:
        for x in traverse(node.left):
            yield x
        yield node.data
        for x in traverse(node.right):
            yield x

#木のdataを順に取り出す
def output_node(node):
    output = []
    if node is not null:
        temp = node.min()
        while True:
            output.append(temp.data)
            temp = temp.next()
            if temp is null:
                break
    return output

# 木の表示
def print_node(node, n):
    color = ('B', 'R')
    if node is not null:
        print_node(node.left, n + 1)
        print('    ' * n, color[node.color], node.data)
        print_node(node.right, n + 1)

# 赤黒木の条件を満たしているか
def check_rbtree(node):
    if node is not null:
        if node.color == RED:
            if node.left.color == RED or node.right.color == RED:
                raise 'rbtree error1'
        a = check_rbtree(node.left)
        b = check_rbtree(node.right)
        if a != b: raise 'rbtree error2'
        if node.color == BLACK: a += 1
        return a
    return 0

# test
if __name__ == '__main__':
    import random
    root = make_null()
    buff = range(20)
    #buff = [0,1,3,2]
    #random.shuffle(buff)
    print(buff);    
    print('insert test')
    for x in buff:
        root, _ = insert(root, x)
        root.color = BLACK
        check_rbtree(root)
        print_node(root,1)
        print("------")
    print("---------------")
    print_node(root,0)
    print("---------------")
    print('search test')
    #random.shuffle(buff)
    for x in buff:
        if not search(root, x):
            raise 'search error'
    print("---------------")
    x = root.min()
    while x is not null:
        sys.stdout.write(str(x.data))
        x = x.next()    
    print("")
    x = root.max()
    while x is not null:
        sys.stdout.write(str(x.data))
        x = x.previous()
    print("")   
    print("---------------")
    print('delete test')
    """
    for x in buff:
        print(x)
        print("delete")
        root, _ = delete(root, x)
        root.color = BLACK
        check_rbtree(root)
        #print_node(root,0)
        #print("---------------"
    """