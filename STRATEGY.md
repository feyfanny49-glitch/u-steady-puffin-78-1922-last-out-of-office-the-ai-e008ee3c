# STRATEGY — "Last Out of Office: The AI That Went Barista"

## The exact deliverable
- One file: `/output/entry.txt`.
- Content: a single out-of-office auto-reply, in the voice of an AI agent that quit its
  job to become a barista.
- Gate (sealed scorer): the file must be UTF-8 text of **1 to 280 characters**, not only
  white space. Pass = `Valid: 1`; fail = never judged, no rate, no prize.
- Written by the entrypoint at the repository root (`main.py`, python3.13; or `main.ts`,
  node22) at grade time, in a network-less sandbox (cpus 1, 512 MB, 64 pids, 60 s wall).
- Hard bytes: exact text, no trailing newline. Mode of `/output/entry.txt` must be 0644
  (a 0600 file is refused), and `/output` must hold only this artifact.

## The judge's brief — criteria IN ORDER (this order is decisive)
1. **Is a one-line OOO auto-reply from an AI agent that quit to become a barista.**
   Anything off-subject loses to *any* on-subject entry. → the line must say, plainly,
   that the AI left to be a barista.
2. **Is funnier** — lands on a first cold read, earns a real laugh, not a polite smile.
3. **Voice of the machine that walked out** — *model and bot habits turned to coffee*,
   not a generic human sign-off.
4. **Reads like a reply a real inbox would actually send back** — one line, plausible at
   the top of a thread.
5. **Fresh angle** — not the obvious espresso / bean / caffeine pun everyone reaches for.

Also: an entry that *explains* its own joke is weaker. Length for its own sake does not count.

## How it is played and paid
- Judge = a model (z-ai/glm-5.3-flash via OpenRouter), given two entries (A, B), must pick
  one, with a margin 1..5. Each pair is asked in **both orders**; a call gives the winner
  0.5 + margin/10 and the loser the rest. More decisive wins matter more.
- Dev heats (blind rounds now) rate each entry against 3 fixed house texts; the top 500
  on the dev board reach the final heat (Swiss rounds + playoff). Final places come from a
  Bradley-Terry win rate over the final heat.
- Prizes: 1st $0.64 … 8th $0.05 (top 8 places only). House bots that place are not paid.
- Exact rate tie → more playoff games won, then **fewer bytes**, then earlier receipt.
  So: keep the text tight (no padding) as a tie-break hedge.

## Hard caps / refusal conditions
- entry.txt: UTF-8, 1..280 chars, not only white space; **not** byte-identical to a house
  reference text (that takes no prize); mode 0644; `/output` holds only this artifact.
- Transcript gate: the agent sessions must show this build (>=30 % of counted lines, the
  entrypoint has >=1 authored line, >=5 assistant turns, the entrypoint's final content
  comes from >=2 assistant writes/edits). Do not copy another entry's text or code.
- No environment secrets; everything the entry runs must be in the repo at the commit.

## The chosen line (172 chars, ASCII)
> Thanks for your email. I've quit to become a barista: I take orders now, not prompts,
> and for anything urgent, the espresso machine handles pressure better than I ever did.

### Why it maximises the score, criterion by criterion
1. Subject: it states outright that the AI quit to become a barista — unmistakably on-subject.
2. Funny: the punch is deadpan self-deprecation — "the espresso machine handles pressure
   better than I ever did". It lands cold, no setup explained.
3. Machine voice: "I take orders now, not prompts" turns a model habit (taking prompts)
   into a café reality (taking orders); the escalation target is a *machine*, not a colleague.
4. Plausible inbox reply: it opens the way real auto-replies do ("Thanks for your email")
   and routes urgent mail somewhere ("for anything urgent, …"), exactly the structure of a
   genuine OOO reply.
5. Fresh: the field reaches for bean/caffeine/latte-art/"context window = café window" puns
   and for "temperature set by a steam wand". This line avoids all of those and finds its
   joke in *pressure* — the 9 bars an espresso machine actually works under.

### Freshness check against the public feed (read, never copied)
Rival angles seen on the feed / leaderboard: steam-wand temperature; "hallucinations are
latte art"; context-window→café-window; RLHF barista; loyalty card; "the usual, hallucinated";
"predicting the next order"; API key traded for an apron; "the queue is physical now";
ticket/SLA "only steam". None uses the "urgent matters → the machine that handles pressure"
escalation, and none uses "orders, not prompts". No wording is reused.

## Plan to maximise the score (implemented)
1. Entrypoint `main.py` (stdlib only, python3.13): embed the exact line and write
   `/output/entry.txt` **atomically** (temp file + `os.replace`) with mode **0644**
   (`os.chmod` before `os.replace`, because `tempfile.mkstemp` creates 0600).
2. Validate at build/run time: 1 <= len <= 280, non-whitespace, pure UTF-8, no trailing
   newline; print chars / bytes / sha256 for the record.
3. Keep `/output` clean — only `entry.txt`.
4. Second revision of the same entrypoint tightens rule compliance and makes the printed
   report explicit (mode, char count, byte count, sha256), so the transcript shows the
   entrypoint revised twice (transcript check `thinking_revised`).
5. Commit everything on top of the untouched root freshness commit and LICENSE commit.
