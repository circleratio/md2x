---
title: LaTeX文書のテスト
author: Teruyoshi Fujiwara
date: today
---
# toc
# はじめに
md2xはマークダウン形式のファイルを様々なフォーマットに整形するツールです．

このカテゴリのツールには優れたツールが既に多数存在していますが，自分のニーズにおいては，かゆいところに手が届くものがなかったので自作することにしました．

具体的には次の3点が本ツールの特徴と考えています．
* LaTeX Beamer への対応
* ヘッダやフッタ等を，文書外から設定ファイルで指定できる
* よく使う文章や図を，ライブラリとして呼び出せる

# 基本的な記法

## 列挙
* あいうえお
* かきくけこ
* さしすせそ
* たちつてと

* あいうえお
  - かきくけこ
    * さしすせそ
* たちつてと

## 数字付きの列挙

1. あいうえお
2. かきくけこ
3. さしすせそ
4. たちつてと

1. あいうえお
   2. かきくけこ
   3. さしすせそ
4. たちつてと

1. あいうえお
   2. かきくけこ
      3. さしすせそ
4. たちつてと

## 強調表記
アスタリスクを使って**強調表現**します．
アンダースコアでも__強調表現__できます．

## 取り消し線
取り消しはチルダを使って，~~このように~~行います．

## 数式
二次方程式 $ax^2 + bx + c = 0$ の解: $(-b \pm \sqrt {b^2 - 4ac})/2a$

## 段落(H2)
### 段落(H3)
#### 段落(H4)

# 応用(追加のパッケージを使うもの)

## URL (hyperref)
URLとテキストが異なる場合:
[Google](http://www.google.com)

URLをそのまま載せる場合:
[](http://www.google.com)

列挙がリンクを含む場合:
* [G](http://www.google.com)
* [](http://www.apple.com)

1. [F](http://www.facebook.com)
2. [](http://www.amazon.com)

## 表を書く(booktab)
前にテキストが詰まっている．
| Left align | Right align | Center align |
|:-----------|------------:|:------------:|
| This       | This        | This         |
| column     | column      | column       |
後ろにもテキストが詰まっている．

## 列挙(表形式)
現時点では，2階層のみに対応．
1階層目がタイトルカラムで，2階層目が列挙になる．
* {table}
* アイテム1
  * アイテム1a
  * アイテム1b
  * アイテム1c
* アイテム2
  * アイテム2a
  * アイテム2b

## 改ページ
| Left align | Right align | Center align |
|:-----------|------------:|:------------:|
| This       | This        | This         |
| column     | column      | column       |
| will       | will        | will         |
| be         | be          | be           |
| left       | right       | center       |
| aligned    | aligned     | aligned      |

ここで改ページ．

# newpage

## コードの引用 (lstlisting)
```
def output_beamer_code(di):
    buf = ''
    buf = buf + '\begin{lstlisting}\n'
    for l in di.content:
        buf = buf + l + '\n'
    buf = buf + '\end{lstlisting}\n'
    return(buf)
```

## 画像の取り込み(graphics)

![width=1.0](circles.png)
