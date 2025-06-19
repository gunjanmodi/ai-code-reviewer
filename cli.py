import sys
from app.infrastructure.openai import OpenAICodeReviewer

def read_patch_file(patch_path: str) -> str:
    with open(patch_path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <path-to-patch>")
        return

    patch_path = sys.argv[1]
    patch_text = read_patch_file(patch_path)

    OpenAICodeReviewer(patch_text).execute()


if __name__ == "__main__":
    main()

