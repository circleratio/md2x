---
title: Emacs
---
# インストール
かつては様々な日本語化ディストリビューションがあったが，今はGNU標準のもので日本語も扱えるので，これを使うのが良い．
積極的に標準のものを使う理由はパッケージ活用．
GNU, MELPA を通じて様々なパッケージが提供されているため，標準に合わせるのがトラブル回避につながる．


# パッケージ管理，設定管理
leaf を使う．

パッケージの依存関係管理やインストールを行ってくれるとともに，定型的な設定をシンプルに書くしくみを提供してくれる．

既存の設定を leaf 形式にするためには，"leaf-convert" パッケージをインストール．
init.el の置き換えたい部分を M-x leaf-convert-region-replace で変換．


# 便利なパッケージ
## swiper
C-s にはデフォルトで isearch がバインドされているが、swiperに置き換え．
バッファ内の検索を該当行のみ取り出して一覧表示してくれる．
正規表現も使える．

```
(leaf swiper
  :doc "Isearch with an overview. Oh, man!"
  :req "emacs-24.5" "ivy-0.13.0"
  :tag "matching" "emacs>=24.5"
  :url "https://github.com/abo-abo/swiper"
  :emacs>= 24.5
  :ensure t
  :bind (("C-s" . swiper)))
```

## tab-bar-mode
Emacsをタブエディタ化する．
キーバインドは GNU screen コマンドに合わせる設定にした．
```
(leaf tab-bar-mode
  :init
  (defvar my:ctrl-z-map (make-sparse-keymap)
    "A keymap to use C-z as prefix.")
  (defalias 'my:ctrl-z-prefix my:ctrl-z-map)
  (define-key global-map    (kbd "C-z") 'my:ctrl-z-prefix)
  (define-key my:ctrl-z-map (kbd "c")   'tab-new)
  (define-key my:ctrl-z-map (kbd "C-c") 'tab-new)
  (define-key my:ctrl-z-map (kbd "k")   'tab-close)
  (define-key my:ctrl-z-map (kbd "C-k") 'tab-close)
  (define-key my:ctrl-z-map (kbd "n")   'tab-next)
  (define-key my:ctrl-z-map (kbd "C-n") 'tab-next)
  (define-key my:ctrl-z-map (kbd "p")   'tab-previous)
  (define-key my:ctrl-z-map (kbd "C-p") 'tab-previous)
  :custom
  ((tab-bar-close-last-tab-choice  . nil)
   (tab-bar-close-tab-select       . 'left)
   (tab-bar-history-mode           . nil)
   (tab-bar-new-button-show        . nil)
   (tab-bar-tab-name-function      . 'tab-bar-tab-name-truncated)
   (tab-bar-tab-name-truncated-max . 12))
  :config
  (tab-bar-mode +1))
```

## neotree
IDE のように画面右端にソースツリーを表示する．
package install で neotree をインストール．

設定ファイル (Leafベース)
```
(leaf neotree
  :ensure t
  :commands
  (neotree-show neotree-hide neotree-dir neotree-find)
  :custom (neo-theme . 'nerd2)
  :bind (("C-\\" . neotree-toggle))
  :preface
  )
```

## markdown-mode, markdown-preview-mode
markdown を扱うためのパッケージ．

markdown-preview-modeは，標準入出力のフィルタとして動作する md→HTML レンダラを必要とする．
pandoc を想定しているようだが，自分の場合は自作のスクリプトを使用．

```
(leaf markdown-preview-mode
  :custom ((markdown-command . "python C:/Users/circl/Desktop/dev/md2x/md2x.py")
	   (markdown-use-pandoc-style-yaml-metadata . t)
           (markdown-preview-stylesheets . '("github-markdown.css")))
  :config
  (provide 'markdown-config))
```

CSSは markdown ファイルと同じ場所に置いておくと上記のファイル名指定で参照される．
セキュリティの制限か，ローカルの絶対パス指定では動かなかった．

操作
* 開始: markdown-preview-mode
* 終了: markdown-preview-cleanup

ただし自分の環境では，終了してもウェブサービスのプロセスがうまく終了しない現象が発生．

# itemize
* アイテム1
* アイテム2
* アイテム3
* アイテム4

* アイテム1
  * アイテム2
  * アイテム3
    * アイテム4
* アイテム5


# enumerate
1. アイテム1
1. アイテム2
1. アイテム3
1. アイテム4

1. アイテム1
  1. アイテム2
  1. アイテム3
    1. アイテム4
1. アイテム5

# table
表の例。

| Left align | Right align | Center align |
|:-----------|------------:|:------------:|
| This       | This        | This         |
| column     | column      | column       |
| will       | will        | will         |
| be         | be          | be           |
| left       | right       | center       |
| aligned    | aligned     | aligned      |
