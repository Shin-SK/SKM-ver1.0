#!/bin/bash
# 必要なパッケージのインストール（Amazon Linux 2 の場合）
sudo yum install -y pango pango-devel gdk-pixbuf2 gdk-pixbuf2-devel cairo cairo-devel libffi-devel

# /usr/lib64/libpango-1.0.so.0 が存在するか確認
if [ -f /usr/lib64/libpango-1.0.so.0 ]; then
    # シンボリックリンクの作成：WeasyPrint が期待する名前に合わせる
    sudo ln -sf /usr/lib64/libpango-1.0.so.0 /usr/lib64/libpango-1.0-0
else
    echo "/usr/lib64/libpango-1.0.so.0 が見つかりません。パッケージのインストールに問題がある可能性があります。"
    exit 1
fi
