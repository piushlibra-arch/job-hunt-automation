import feedparser, json, datetime, pathlib, html, re


# 1. Feeds to watch (swap in the ones you want)
FEEDS = [
  "https://weworkremotely.com/categories/remote-programming-jobs.rss",
  "https://remotive.com/remote-jobs/feed/software-dev",
]


# 2. Your skills = the scoring dictionary
SKILLS = ["python","computer vision","comfyui","diffusion",
  "image","automation","llm","genai","pipeline","aws",
  "opencv","hugging face","machine learning","ml","ai"]


def score(text):
    t = text.lower()
    return sum(1 for s in SKILLS if s in t)


rows = []
for url in FEEDS:
    for e in feedparser.parse(url).entries:
        blob = html.unescape(e.get("title","") + " " + e.get("summary",""))
        blob = re.sub("<[^>]+>", " ", blob)
        s = score(blob)
        if s >= 3:                      # keep only strong matches
            rows.append((s, e.get("title","?"), e.get("link","")))


rows.sort(reverse=True)               # best matches first


# 3. Write a self-updating tracker file
out = pathlib.Path("JOBS.md")
today = datetime.date.today().isoformat()
lines = [f"# Job matches (updated {today})\n"]
for s, title, link in rows[:40]:
    lines.append(f"- [score {s}] [{title}]({link})")
out.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {len(rows)} matches")
