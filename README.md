# PG-TECOLI

[鉄塔てこり](https://pg.tecoli.com)（関東の送電鉄塔・送電線マップ）で使う公開データです。
現在は「見どころ」（`spots.yaml`）のみですが、将来ほかの種類のデータも追加する想定です。

## データの種類

- `spots.yaml` — **見どころ**: 地図上の吹き出しから解説を表示するスポット集

## spots.yaml の書式

```yaml
- id: nakatokyo-hidaka          # 一意なID（英数字とハイフン）
  no: 1                         # 表示番号
  title: 中東京変電所（埼玉県日高市）
  subtitle: 3つの“電力の世界”が交わる場所
  marker: [139.35386, 35.91528] # 吹き出しの位置 [経度, 緯度]
  camera:                       # クリック時に飛ぶカメラ
    center: [139.363, 35.9225]  # 中心 [経度, 緯度]
    zoom: 12.7                  # ズーム
    pitch: 57                   # 傾き（度。0=真上から）
    bearing: -35                # 方位（度。0=北が上）
  select_bbox: [西, 南, 東, 北]  # この範囲に掛かる路線をすべて選択（電圧色で強調）
  more: https://pg.tecoli.com/spots.html   # 「くわしく読む」リンク（任意）
  body: |                       # 解説文（簡易 Markdown）
    段落は空行で区切ります。**太字** と [リンク](https://...) が使えます。
```

- `body` で使えるのは **太字**・[リンク](url)・段落のみ（HTML は書けません）
- カメラ値は地図をお好みの構図にしたあと、ブラウザのコンソールで
  `_map.getCenter(), _map.getZoom(), _map.getPitch(), _map.getBearing()` を見ると得られます

## 投稿のしかた

1. このリポジトリを **fork & clone** して `spots.yaml` に項目を追加
2. fork を GitHub に push し、**本番サイトで動作確認**:
   `https://pg.tecoli.com/?data=あなたのユーザー名/PG-TECOLI`
   （ブランチ指定は `?data=ユーザー名/リポジトリ名@ブランチ名`）
3. 表示・カメラ・強調範囲を確認できたら **Pull Request** を送ってください

ローカルで鉄塔てこりを動かしている場合は `?data=http://localhost:8000` のように
URL を直接指定することもできます（`spots.yaml` を配信できる任意のベースURL）。

## ライセンス

未定（追って明記します）。投稿されたデータはサイトでの表示・再配布に使わせていただきます。
