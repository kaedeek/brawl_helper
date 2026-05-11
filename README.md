# ブロスタヘルパー ボット

**ブロスタヘルパー ボット**は、Discord botでコマンドを実行すると

ブロスタのイベント情報などの情報を表示するボットです。

[ボット招待](https://discord.com/oauth2/authorize?client_id=1503026344248742082&permissions=2147567616&integration_type=0&scope=bot)

## プロジェクト構成

```plaintext
brawl_helper/
├── api/
│   ├── __init__.py
│   └── brawl.py
├── locales/
│   ├── en.py
│   ├── ja.py
│   └── maps_ja.json
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── LICENSE
├── README.md
├── requirements.txt
└── uv.lock
```

### 使い方

```bash
git clone https://github.com/kaedeek/brawl_helper.git
cd brawl_helper

pip install -r requirements.txt

uv run main.py
```

### 開発環境

- Python 3.12
- Windows11 64ビット