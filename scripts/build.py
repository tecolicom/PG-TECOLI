#!/usr/bin/env python3
"""spots/*.yaml（1ファイル=1見どころ）から配信用 spots.yaml を生成する。

    python3 scripts/build.py

サイト（pg.tecoli.com）はリポジトリ直下の spots.yaml を読む。
main への push 時は GitHub Actions が自動で再生成する（.github/workflows/build.yml）。
"""
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

HEADER = (
    "# このファイルは spots/*.yaml から自動生成されます。直接編集しないでください。\n"
    "# 再生成: python3 scripts/build.py（main への push 時は CI が実行）\n"
)


def load_one(path: pathlib.Path) -> dict:
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(d, dict):
        sys.exit(f"{path.name}: 1ファイル=1見どころ（マッピング）で書いてください")
    # PyYAML(YAML 1.1) は素の `no` キーを False と解釈するため戻す
    if False in d:
        d["no"] = d.pop(False)
    if not d.get("id"):
        sys.exit(f"{path.name}: id は必須です")
    if d["id"] != path.stem:
        sys.exit(f"{path.name}: id（{d['id']}）はファイル名と一致させてください")
    return d


def main() -> None:
    files = sorted((ROOT / "spots").glob("*.yaml"))
    items = [load_one(f) for f in files]
    items.sort(key=lambda d: (d.get("no", 9999), d.get("id", "")))
    body = yaml.safe_dump(items, allow_unicode=True, sort_keys=False, width=100)
    (ROOT / "spots.yaml").write_text(HEADER + body, encoding="utf-8")
    print(f"spots.yaml: {len(items)} 件を生成")


if __name__ == "__main__":
    main()
