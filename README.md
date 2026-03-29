# local-file-reader

ローカルファイルを安全に読み取り、検索できるMCPサーバーです。

## 機能

- **list_files**: ベースディレクトリ配下のファイル/フォルダ一覧を取得
- **read_file**: テキストファイルの内容を読み取る
- **search_text**: キーワードでテキストを検索

## セットアップ

### 1. 依存関係をインストール

```bash
pip install -r requirements.txt
```

### 2. ベースディレクトリを準備

デフォルトでは `D:\MCP_Server` をベースディレクトリとして使用します。必要に応じて、このディレクトリを作成し、読み取りたいファイルを配置してください。

```powershell
mkdir D:\MCP_Server
```

### 3. サーバーを起動

```bash
python -c "from file_reader_mcp import mcp; mcp.run(transport='sse')"
```

## Claude Code への接続

`local-file-reader` は別のプロセス/ターミナルで起動しておき、`.mcp.json` を通じて Claude Code から接続します。

### ステップ1: local-file-reader を起動（ターミナル1）

```bash
cd D:\VSCode\mcpserver-sample
python -c "from file_reader_mcp import mcp; mcp.run(transport='sse')"
```

サーバーがポート 8000 で起動します：
```
INFO:     Uvicorn running on http://localhost:8000
```

### ステップ2: .mcp.json を配置

プロジェクトルートに `.mcp.json` を作成します（リポジトリ内に既に `claude_desktop_config.json.example` があるので参考にしてください）：

```json
{
  "mcpServers": {
    "local-file-reader": {
      "type": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

**配置場所の優先順位:**
- プロジェクトルート（`.mcp.json`）— そのプロジェクト専用

### ステップ3: 接続確認

Claude Code（VSCode拡張 または CLI）を開き直すと自動的に `.mcp.json` が読み込まれます。

接続確認コマンド（Claude Code CLI）：
```bash
claude mcp get local-file-reader
```

`local-file-reader` が表示されれば接続成功です。

### 使用例

Claude に以下のようにリクエストできます：

```
list_files で D:\MCP_Server のファイル一覧を表示してください
```

```
read_file で sample.txt の内容を読み取ってください
```

```
search_text で "error" キーワードを検索してください
```

## 設定

`file_reader_mcp.py` の以下の場所でベースディレクトリを変更できます：

```python
BASE_DIR = Path(r"D:\MCP_Server").resolve()
```

## 許可されるファイル拡張子

- `.txt`
- `.md`
- `.log`
- `.json`
- `.yaml`, `.yml`
- `.ini`
- `.csv`

新しい拡張子を追加する場合は、`ALLOWED_EXTENSIONS` を編集してください：

```python
ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".log", ".json", ".yaml", ".yml", ".ini", ".csv", ".yourext"
}
```

## セキュリティ機能

- BASE_DIR外へのアクセス禁止
- ファイルサイズ上限：1MB（MAX_FILE_SIZE で変更可能）
- 許可された拡張子のみ読み取り可能
- 検索結果は最大100件まで

## ツール仕様

### list_files

```
list_files(relative_dir: str = "", pattern: str = "*") -> list[str]
```

**パラメータ:**
- `relative_dir`: ベースディレクトリからの相対パス（デフォルト: ルート）
- `pattern`: ファイル名パターン（fnmatchで評価）

**例:**
```
list_files("docs", "*.md")  # docs フォルダの .md ファイル一覧
```

### read_file

```
read_file(relative_path: str) -> str
```

**パラメータ:**
- `relative_path`: ベースディレクトリからの相対パス

**例:**
```
read_file("config.json")  # ルートの config.json を読み取る
read_file("docs/readme.md")  # docs/readme.md を読み取る
```

### search_text

```
search_text(keyword: str, relative_dir: str = "") -> list[dict]
```

**パラメータ:**
- `keyword`: 検索キーワード
- `relative_dir`: 検索対象ディレクトリ（デフォルト: ルート全体）

**戻り値:**
```json
[
  {
    "path": "folder/file.txt",
    "line": 42,
    "text": "マッチした行の内容（最初の300文字）"
  }
]
```

**例:**
```
search_text("error", "logs")  # logs フォルダで "error" を検索
```

## トラブルシューティング

### BaseDir が見つからない
BASE_DIR に指定したディレクトリが存在することを確認してください。

### ファイルが読み取り不可

- ファイルの拡張子が ALLOWED_EXTENSIONS に含まれているか確認してください
- ファイルサイズが 1MB を超えていないか確認してください
- ファイルが UTF-8 でエンコードされていることを確認してください（そうでない場合は自動的に置換エラーで処理されます）

### ACCESS_DENIED エラー

relative_path が BASE_DIR 外のファイルを指していないか確認してください。

### Claude Code で local-file-reader が認識されない

1. **local-file-reader が起動しているか確認**
   ```powershell
   # ターミナルで起動コマンドが実行されているか、ログ出力がないか確認
   python -c "from file_reader_mcp import mcp; mcp.run(transport='sse')"
   # 以下のようなログが出力されるはず：
   # INFO:     Uvicorn running on http://localhost:8000
   ```

2. `.mcp.json` がプロジェクトルートまたは `~/.claude/` に配置されているか確認

3. `.mcp.json` の JSON 構文が正しいか確認（オンラインJSONバリデータで検証）

4. `url` が正しく設定されているか確認：
   ```json
   "url": "http://localhost:8000/sse"
   ```

5. Claude Code（VSCode拡張）を再起動、またはウィンドウをリロード（Ctrl+Shift+P → "Reload Window"）

6. CLI の場合は `claude mcp list` で登録状況を確認

### local-file-reader に接続テスト

サーバーが正しく起動しているか確認：

```bash
# ターミナル1で local-file-reader を起動
python -c "from file_reader_mcp import mcp; mcp.run(transport='sse')"

# ターミナル2でポート疎通を確認（Windows PowerShell）
Test-NetConnection localhost -Port 8000

# または別ターミナルでテストスクリプト実行
python test_server.py
```

### よくある問題

**「ポート 8000 は既に使用中」エラー**
- 別のプロセスがポート 8000 を使用しています
- 競合プロセスを停止するか、利用ポートを解放してください
- どのプロセスが使用しているかは以下で確認できます：
  ```powershell
  netstat -ano | findstr :8000
  ```

**Claude から接続できない**
- ファイアウォール設定を確認してください
- `http://localhost:8000` にブラウザからアクセス可能か試してください
