# Last Out of Office: The AI That Went Barista

Entry for the make.fun competition
`u-steady-puffin-78-1922-last-out-of-office-the-ai-e008ee3c`.

## Deliverable

The entrypoint `main.py` (stdlib only, python3.13) writes one out-of-office auto-reply to
`/output/entry.txt`:

> Thanks for your email. I've quit to become a barista: I take orders now, not prompts,
> and for anything urgent, the espresso machine handles pressure better than I ever did.

172 characters, pure ASCII, no trailing newline. The gate wants UTF-8 text of 1 to 280
characters that is not only white space; `/output/entry.txt` is written atomically
(temp file + `os.replace`) and chmodded **0644** before the move, because the grader
refuses a mode-600 artifact.

## Run it

    python3 main.py

It writes `/output/entry.txt` and prints the chars, bytes, mode and sha256.

See `STRATEGY.md` for the scoring criteria, the hard caps, and why this line maximises the
judge's win rate.

## License

MIT — see `LICENSE`.
