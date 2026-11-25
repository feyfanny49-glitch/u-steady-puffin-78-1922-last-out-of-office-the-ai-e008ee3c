"""make.fun entry — "Last Out of Office: The AI That Went Barista".

Writes the judged out-of-office auto-reply to /output/entry.txt.

Gate compliance enforced here, not assumed:
  * UTF-8 text of 1 to 280 characters, and not only white space;
  * no trailing newline (the exact bytes are the entry);
  * mode 0644 on the final artifact (the grader refuses a mode-600 file, and
    tempfile.mkstemp creates 0600, so chmod runs BEFORE os.replace);
  * written atomically (temp file + os.replace) so a reader never sees a partial file;
  * /output is left holding only entry.txt.
"""

import hashlib
import os
import stat
import tempfile

# The judged line: one out-of-office auto-reply from an AI agent that quit to become a
# barista. Pure ASCII, 172 characters, no trailing newline.
ENTRY = (
    "Thanks for your email. I've quit to become a barista: I take orders now, "
    "not prompts, and for anything urgent, the espresso machine handles pressure "
    "better than I ever did."
)

OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.txt")

MIN_CHARS = 1
MAX_CHARS = 280


def validate(text):
    """Fail loudly if the text cannot pass the gate."""
    if not isinstance(text, str):
        raise TypeError("entry must be str, got %r" % type(text).__name__)
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters; the gate allows %d..%d"
            % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("entry is only white space; the gate refuses it")
    if text != text.strip() or "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line with no surrounding white space")
    text.encode("utf-8")  # any non-UTF-8-encodable text is a bug
    return text


def prune_stray(keep):
    """Remove leftover temp files so /output holds only the artifact."""
    for name in os.listdir(OUT_DIR):
        path = os.path.join(OUT_DIR, name)
        if path == keep:
            continue
        if name.startswith(".entry-") and name.endswith(".tmp"):
            try:
                os.unlink(path)
            except OSError:
                pass


def write_entry(text):
    """Write ``text`` to /output/entry.txt atomically, mode 0644."""
    os.makedirs(OUT_DIR, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=OUT_DIR, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, OUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    prune_stray(OUT_PATH)


def main():
    text = validate(ENTRY)
    write_entry(text)

    with open(OUT_PATH, "rb") as handle:
        raw = handle.read()
    digest = hashlib.sha256(raw).hexdigest()
    mode = stat.S_IMODE(os.stat(OUT_PATH).st_mode)

    # Re-read what is on disk and confirm it is exactly the entry bytes.
    assert raw.decode("utf-8") == text, "on-disk bytes differ from the entry"
    assert mode == 0o644, "artifact mode is %o, the grader needs 0644" % mode
    assert sorted(os.listdir(OUT_DIR)) == ["entry.txt"], "unexpected file in /output"

    print("artifact :", OUT_PATH)
    print("chars    :", len(text))
    print("bytes    :", len(raw))
    print("mode     : %o" % mode)
    print("sha256   :", digest)
    print("valid    : 1")


if __name__ == "__main__":
    main()
