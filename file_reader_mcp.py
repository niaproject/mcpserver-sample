from __future__ import annotations

from pathlib import Path
import fnmatch
import sys

from mcp.server.fastmcp import FastMCP

# MCP server name
mcp = FastMCP("local-file-reader")

# 読ませたいルートフォルダを固定
# Windows例: D:\MCP_Server
BASE_DIR = Path(r"D:\MCP_Server").resolve()

# 読み取りを許可する拡張子
ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".log", ".json", ".yaml", ".yml", ".ini", ".csv"
}

# 安全のための上限
MAX_FILE_SIZE = 1024 * 1024  # 1MB
MAX_RESULTS = 100


def safe_path(relative_path: str) -> Path:
    """
    BASE_DIR配下のみを許可する。
    """
    target = (BASE_DIR / relative_path).resolve()

    # BASE_DIRの外へ出るのを禁止
    if target != BASE_DIR and BASE_DIR not in target.parents:
        raise ValueError("Access denied: path is outside the allowed base directory.")

    return target


def is_allowed_text_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS


@mcp.tool()
def list_files(relative_dir: str = "", pattern: str = "*") -> list[str]:
    """
    ベースフォルダ配下のファイル/フォルダ一覧を返す。
    relative_dir は BASE_DIR からの相対パス。
    pattern で簡易フィルタ可能。
    """
    target_dir = safe_path(relative_dir)

    if not target_dir.exists():
        raise ValueError(f"Directory not found: {relative_dir}")

    if not target_dir.is_dir():
        raise ValueError(f"Not a directory: {relative_dir}")

    items: list[str] = []
    for child in sorted(target_dir.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        if fnmatch.fnmatch(child.name, pattern):
            rel = child.relative_to(BASE_DIR)
            suffix = "/" if child.is_dir() else ""
            items.append(str(rel).replace("\\", "/") + suffix)

    return items


@mcp.tool()
def read_file(relative_path: str) -> str:
    """
    テキストファイルを読み取って返す。
    relative_path は BASE_DIR からの相対パス。
    """
    path = safe_path(relative_path)

    if not path.exists():
        raise ValueError(f"File not found: {relative_path}")

    if not is_allowed_text_file(path):
        raise ValueError(
            f"Unsupported file type. Allowed: {sorted(ALLOWED_EXTENSIONS)}"
        )

    size = path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {size} bytes (max {MAX_FILE_SIZE})")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


@mcp.tool()
def search_text(keyword: str, relative_dir: str = "") -> list[dict]:
    """
    指定フォルダ配下のテキストファイルを走査して keyword を検索する。
    一致箇所を最大 MAX_RESULTS 件返す。
    """
    if not keyword.strip():
        raise ValueError("keyword must not be empty")

    target_dir = safe_path(relative_dir)

    if not target_dir.exists():
        raise ValueError(f"Directory not found: {relative_dir}")

    if not target_dir.is_dir():
        raise ValueError(f"Not a directory: {relative_dir}")

    results: list[dict] = []
    keyword_lower = keyword.lower()

    for path in target_dir.rglob("*"):
        if len(results) >= MAX_RESULTS:
            break

        if not is_allowed_text_file(path):
            continue

        try:
            if path.stat().st_size > MAX_FILE_SIZE:
                continue

            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        for lineno, line in enumerate(text.splitlines(), start=1):
            if keyword_lower in line.lower():
                results.append(
                    {
                        "path": str(path.relative_to(BASE_DIR)).replace("\\", "/"),
                        "line": lineno,
                        "text": line[:300],
                    }
                )
                if len(results) >= MAX_RESULTS:
                    break

    return results


if __name__ == "__main__":
    # stdout には余計な print を出さないこと
    print("Starting local-file-reader MCP server...", file=sys.stderr)
    mcp.run(transport='sse')
