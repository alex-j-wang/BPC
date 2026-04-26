import time
import pyperclip
import re
import urllib.parse

# Regex pattern to match macOS file:// URLs to JPG or PNG
pattern = re.compile(
    r"file:///Users/alexwang/Downloads/Wrap-up%202025%20Draft/images/([^/]+\.(?:jpg|png))",
    re.IGNORECASE,
)

def translate_clipboard_text(text: str) -> str:
    match = pattern.search(text)
    if match:
        filename = urllib.parse.unquote(match.group(1))
        return f"/wrapup/images/{filename}"
    return text

def main():
    print("Watching clipboard. Press Ctrl+C to stop.")
    last_clip = ""
    while True:
        try:
            current_clip = pyperclip.paste()
            if current_clip != last_clip:
                new_clip = translate_clipboard_text(current_clip)
                if new_clip != current_clip:
                    pyperclip.copy(new_clip)
                    print(f"Replaced:\n{current_clip}\n→ {new_clip}")
                last_clip = current_clip
            time.sleep(0.3)
        except KeyboardInterrupt:
            print("\nStopped.")
            break

if __name__ == "__main__":
    main()