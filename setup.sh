#!/bin/bash

# MCP File Reader Server セットアップスクリプト

echo "========================================"
echo "MCP File Reader Server セットアップ"
echo "========================================"
echo ""

# ベースディレクトリを作成
echo "ベースディレクトリを作成しています..."
mkdir -p ~/MCP_Server
echo "~/MCP_Server を作成しました"

echo ""
echo "テスト用ファイルを作成しています..."
echo "Sample test file" > ~/MCP_Server/sample.txt
echo '{"key": "value"}' > ~/MCP_Server/sample.json
echo "# Test Markdown File" > ~/MCP_Server/test.md

echo ""
echo "========================================"
echo "セットアップが完了しました！"
echo "========================================"
echo ""
echo "次のステップ:"
echo "1. Python 3.10+ がインストールされていることを確認してください"
echo "2. 依存関係をインストール:"
echo "   pip install -r requirements.txt"
echo ""
echo "3. file_reader_mcp.py の BASE_DIR を変更"
echo "   BASE_DIR = Path(os.path.expanduser('~/MCP_Server')).resolve()"
echo ""
echo "4. サーバーを起動:"
echo "   python file_reader_mcp.py"
echo ""
