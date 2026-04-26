import pyperclip
import re
import time

drive_pattern = re.compile(r"https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/view")

iframe_template = """<iframe
  src="https://drive.google.com/file/d/{id}/preview"
  allow="autoplay"
  className="mx-auto aspect-video w-2/3 rounded-md"
></iframe>"""

last_clipboard = None

print("Watching clipboard... Press Ctrl+C to stop.")
try:
    while True:
        text = pyperclip.paste()
        if text != last_clipboard:
            match = drive_pattern.match(text.strip())
            if match:
                file_id = match.group(1)
                iframe = iframe_template.format(id=file_id)
                pyperclip.copy(iframe)
                print(f"✅ Replaced clipboard with embed for: {file_id}")
            last_clipboard = text
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nStopped.")