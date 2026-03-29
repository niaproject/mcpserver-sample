@echo off
REM MCP File Reader Server セットアップスクリプト

echo ========================================
echo MCP File Reader Server セットアップ
echo ========================================
echo.

REM ベースディレクトリを作成
echo ベースディレクトリを作成しています...
if not exist "D:\MCP_Server" (
    mkdir D:\MCP_Server
    echo D:\MCP_Server を作成しました
) else (
    echo D:\MCP_Server は既に存在します
)

echo.
echo テスト用ファイルを作成しています...
echo Sample test file > D:\MCP_Server\sample.txt
echo {"key": "value"} > D:\MCP_Server\sample.json
echo # Test Markdown File > D:\MCP_Server\test.md

echo.
echo ========================================
echo セットアップが完了しました！
echo ========================================
echo.
echo 次のステップ:
echo 1. Python 3.10+ がインストールされていることを確認してください
echo 2. 依存関係をインストール:
echo    pip install -r requirements.txt
echo.
echo 3. サーバーを起動:
echo    python file_reader_mcp.py
echo.

pause
