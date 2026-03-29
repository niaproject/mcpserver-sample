"""
MCP File Reader Server テストスクリプト

使用例とテストケース
"""

import asyncio
from pathlib import Path
from file_reader_mcp import list_files, read_file, search_text


async def main():
    print("=" * 50)
    print("MCP File Reader Server テスト")
    print("=" * 50)
    print()

    # テスト1: ファイル一覧取得
    print("【テスト1】list_files - ベースディレクトリのファイル一覧")
    print("-" * 50)
    try:
        files = list_files()
        print(f"見つかったアイテム: {len(files)}")
        for item in files:
            print(f"  - {item}")
    except Exception as e:
        print(f"エラー: {e}")
    print()

    # テスト2: 特定パターンのファイル取得
    print("【テスト2】list_files - *.md ファイルを検索")
    print("-" * 50)
    try:
        md_files = list_files(pattern="*.md")
        print(f"見つかった .md ファイル: {len(md_files)}")
        for file in md_files:
            print(f"  - {file}")
    except Exception as e:
        print(f"エラー: {e}")
    print()

    # テスト3: ファイルを読み取り
    print("【テスト3】read_file - sample.txt を読み取り")
    print("-" * 50)
    try:
        content = read_file("sample.txt")
        print(f"ファイル内容:")
        print(f"{content}")
    except Exception as e:
        print(f"エラー: {e}")
    print()

    # テスト4: JSON ファイルを読み取り
    print("【テスト4】read_file - sample.json を読み取り")
    print("-" * 50)
    try:
        content = read_file("sample.json")
        print(f"ファイル内容:")
        print(f"{content}")
    except Exception as e:
        print(f"エラー: {e}")
    print()

    # テスト5: テキスト検索
    print("【テスト5】search_text - 'sample' を検索")
    print("-" * 50)
    try:
        results = search_text("sample")
        print(f"検索結果: {len(results)} 件")
        for result in results:
            print(f"  - {result['path']}:{result['line']} - {result['text']}")
    except Exception as e:
        print(f"エラー: {e}")
    print()

    # テスト6: パス走査に対するセキュリティ
    print("【テスト6】セキュリティテスト - パス走査防止")
    print("-" * 50)
    try:
        # BASE_DIR外へのアクセスを試みる
        content = read_file("../../../windows/system32/config/sam")
        print("⚠️  警告: セキュリティが機能していない可能性があります")
    except ValueError as e:
        print(f"✓ セキュリティが正常に機能: {e}")
    except Exception as e:
        print(f"エラー: {e}")
    print()

    print("=" * 50)
    print("テスト完了")
    print("=" * 50)


if __name__ == "__main__":
    # 同期的に実行（FastMCPツールは非同期対応）
    # 実際に使用する場合はMCPサーバー起動時に呼ばれます
    print("注: テストツールを直接実行中")
    print("実際のMCPサーバーとして使用する場合は以下を実行してください:")
    print("  python file_reader_mcp.py")
    print()

    # 簡易テスト（非MCP環境）
    from file_reader_mcp import safe_path, is_allowed_text_file

    print("簡易テスト実行中...")
    print()

    # BASE_DIR の確認
    from file_reader_mcp import BASE_DIR
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"BASE_DIR 存在: {BASE_DIR.exists()}")
    print()

    # safe_path テスト
    try:
        safe_path("test.txt")
        print("✓ safe_path('test.txt') は有効")
    except Exception as e:
        print(f"✗ safe_path('test.txt') エラー: {e}")

    try:
        safe_path("../../etc/passwd")
        print("✗ safe_path セキュリティ失敗")
    except ValueError as e:
        print(f"✓ safe_path セキュリティ成功: {e}")
