#!/usr/bin/env python3
"""spots/NNN-<id>.yaml（1ファイル=1見どころ）から配信用 spots.json を生成する。

    python3 scripts/build.py

- ファイル名の連番 NNN（3桁ゼロ詰め）が表示番号・並び順になる（重複はエラー）
- id はファイル名から導出する（ファイル内に id があれば一致を検証）
- サイト（pg.tecoli.com）は spots.json（minified）を読む
- main への push 時は GitHub Actions が自動で再生成する（.github/workflows/build.yml）
"""
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^(\d{3})-([a-z0-9][a-z0-9-]*)$")


def load_one(path: pathlib.Path) -> dict:
    m = NAME_RE.match(path.stem)
    if not m:
        sys.exit(f"{path.name}: ファイル名は NNN-<id>.yaml（例: 001-nakatokyo-hidaka.yaml）にしてください")
    no, fid = int(m.group(1)), m.group(2)
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        sys.exit(f"{path.name}: 1ファイル=1見どころ（マッピング）で書いてください")
    if False in d:  # PyYAML(YAML 1.1) は素の `no` キーを False と解釈する
        d["no"] = d.pop(False)
    if d.get("id") not in (None, fid):
        sys.exit(f"{path.name}: id（{d['id']}）はファイル名の <id> 部と一致させてください")
    if d.get("no") not in (None, no):
        sys.exit(f"{path.name}: no はファイル名の連番から決まります（no: 行は不要）")
    d["id"], d["no"] = fid, no
    for key in ("title", "marker", "camera", "body"):
        if not d.get(key):
            sys.exit(f"{path.name}: {key} は必須です")
    return d


def build_flows() -> None:
    """flows.yaml（連系線コリドー定義）→ flows.json。無ければスキップ。"""
    src = ROOT / "flows.yaml"
    if not src.exists():
        return
    items = yaml.safe_load(src.read_text(encoding="utf-8"))
    if not isinstance(items, list):
        sys.exit("flows.yaml は配列である必要があります")
    for d in items:
        for key in ("occto", "label"):
            if not d.get(key):
                sys.exit(f"flows.yaml: {key} は必須です（{d}）")
        if not d.get("path") and not (d.get("from") and d.get("to")):
            sys.exit(f"flows.yaml: path か from/to のどちらかが必要です（{d['occto']}）")
    out = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    (ROOT / "flows.json").write_text(out, encoding="utf-8")
    print(f"flows.json: {len(items)} 件 / {len(out.encode('utf-8'))} bytes")


def build_tours() -> None:
    """tours/NNN-<id>.yaml（1ファイル=1ツアー）→ tours.json。ディレクトリが無ければスキップ。"""
    files = sorted((ROOT / "tours").glob("*.yaml"))
    if not files:
        return
    items = []
    for path in files:
        m = NAME_RE.match(path.stem)
        if not m:
            sys.exit(f"{path.name}: ファイル名は NNN-<id>.yaml（例: 001-shin-tokorozawa.yaml）にしてください")
        no, tid = int(m.group(1)), m.group(2)
        d = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(d, dict):
            sys.exit(f"{path.name}: 1ファイル=1ツアー（マッピング）で書いてください")
        if False in d:  # PyYAML(YAML 1.1) は素の `no` キーを False と解釈する
            d["no"] = d.pop(False)
        if d.get("id") not in (None, tid):
            sys.exit(f"{path.name}: id（{d['id']}）はファイル名の <id> 部と一致させてください")
        if d.get("no") not in (None, no):
            sys.exit(f"{path.name}: no はファイル名の連番から決まります（no: 行は不要）")
        d["id"], d["no"] = tid, no
        for key in ("title", "summary", "routes", "stops"):
            if not d.get(key):
                sys.exit(f"{path.name}: {key} は必須です")
        for i, s in enumerate(d["stops"]):
            if not isinstance(s, dict):
                sys.exit(f"{path.name}: stops[{i}] はマッピングで書いてください")
            for key in ("heading", "camera", "body"):
                if not s.get(key):
                    sys.exit(f"{path.name}: stops[{i}].{key} は必須です")
            cam = s["camera"]
            if not isinstance(cam, dict):
                sys.exit(f"{path.name}: stops[{i}].camera はマッピングで書いてください")
            if not (isinstance(cam.get("center"), list) and len(cam["center"]) == 2
                    and "zoom" in cam):
                sys.exit(f"{path.name}: stops[{i}].camera は center=[lng,lat] と zoom が必須です")
        items.append(d)
    nos = [d["no"] for d in items]
    dup = {n for n in nos if nos.count(n) > 1}
    if dup:
        sys.exit(f"tours: 連番が重複しています: {sorted(dup)}")
    items.sort(key=lambda d: d["no"])
    out = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    (ROOT / "tours.json").write_text(out, encoding="utf-8")
    print(f"tours.json: {len(items)} 件 / {len(out.encode('utf-8'))} bytes")


def main() -> None:
    files = sorted((ROOT / "spots").glob("*.yaml"))
    items = [load_one(f) for f in files]
    nos = [d["no"] for d in items]
    dup = {n for n in nos if nos.count(n) > 1}
    if dup:
        sys.exit(f"連番が重複しています: {sorted(dup)}")
    items.sort(key=lambda d: d["no"])
    out = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    (ROOT / "spots.json").write_text(out, encoding="utf-8")
    print(f"spots.json: {len(items)} 件 / {len(out.encode('utf-8'))} bytes")
    build_flows()
    build_tours()


if __name__ == "__main__":
    main()
