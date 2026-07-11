# PG-TECOLI

[鉄塔てこり](https://pg.tecoli.com)（関東の送電鉄塔・送電線マップ）で使う公開データです。
現在は「見どころ」（`spots.yaml`）のみですが、将来ほかの種類のデータも追加する想定です。

## 構成

```
spots/                見どころの元データ（1ファイル = 1見どころ。ここを編集する）
  NNN-<id>.yaml       NNN = 3桁の連番（表示番号・並び順。重複はビルドエラー）
spots.json            配信用の生成物（minified JSON。直接編集しない。CI が自動更新）
scripts/build.py      spots/*.yaml → spots.json の生成スクリプト
```

サイトはリポジトリ直下の `spots.json` を読み込みます。`spots/` を編集して main に push すると
GitHub Actions が `spots.json` を再生成してコミットします。
手元で生成する場合は `python3 scripts/build.py`（要 PyYAML）。
`no`（表示番号）と `id` はファイル名から決まるので、ファイル内に書く必要はありません。

## 見どころ（spots/NNN-<id>.yaml）の書式

```yaml
# ファイル名: 001-nakatokyo-hidaka.yaml（連番と id はファイル名から決まる）
title: 中東京変電所（埼玉県日高市）
subtitle: 3つの“電力の世界”が交わる場所
marker: [139.35386, 35.91528]   # 吹き出しの位置 [経度, 緯度]
camera:                         # クリック時に飛ぶカメラ
  center: [139.3585, 35.9205]   # 中心 [経度, 緯度]
  zoom: 13.8                    # ズーム
  pitch: 0                      # 傾き（度。0=真上から。斜め俯瞰にするなら 50〜60 など）
  bearing: 0                    # 方位（度。0=北が上）
select_bbox: [西, 南, 東, 北]    # この範囲に掛かる路線をすべて選択（電圧色で強調）
places:                         # 任意: 地図データ未収載の地点を本文からリンクしたい場合
  - name: 小千谷発電所           # 本文中のこの文字列がリンクになる
    coords: [138.80683, 37.29437]  # クリックで移動する先 [経度, 緯度]
    type: plant                 # plant=発電所（茶）。省略時は voltage の電圧色
more: https://pg.tecoli.com/spots.html   # 「くわしく読む」リンク（任意）
body: |                         # 解説文（簡易 Markdown）
  段落は空行で区切ります。**太字** と [リンク](https://...) が使えます。
```

- `body` で使えるのは **太字**・[リンク](url)・段落のみ（HTML は書けません）
- `body` 中の路線名・変電所/発電所名は自動でリンクになり、ホバーで地図が強調、
  クリックでその場所へ移動します（地図データにある名前が対象。無い地点は `places` で補えます）
- カメラ値は地図をお好みの構図にしたあと、ブラウザのコンソールで
  `_map.getCenter(), _map.getZoom(), _map.getPitch(), _map.getBearing()` を見ると得られます

## 投稿のしかた

1. このリポジトリを **fork & clone** して `spots/NNN-<あなたのID>.yaml` を追加
   （NNN は既存の続き番号。`python3 scripts/build.py` で `spots.json` を再生成。
   fork で Actions を有効にすれば push 時に自動生成）
2. fork を GitHub に push し、**本番サイトで動作確認**:
   `https://pg.tecoli.com/?data=あなたのユーザー名/PG-TECOLI`
   （ブランチ指定は `?data=ユーザー名/リポジトリ名@ブランチ名`）
3. 表示・カメラ・強調範囲を確認できたら **Pull Request** を送ってください

ローカルで鉄塔てこりを動かしている場合は `?data=http://localhost:8000` のように
URL を直接指定することもできます（`spots.json` を配信できる任意のベースURL）。

## ライセンス

未定（追って明記します）。投稿されたデータはサイトでの表示・再配布に使わせていただきます。
