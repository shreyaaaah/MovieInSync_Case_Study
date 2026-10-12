# How I got to this recommendation

**Starting point.** The brief gave no data, so I started from the official Google Play listing for the employee app (com.moveinsync.ets) and checked it was the employee app, not the driver, field or workplace apps.

**What I did.**
1. Read the listing and the public review pages I could reach: the Play listing (3 visible reviews), AppBrain (rating histogram and 10 recent comments) and MoveInSync's own Help Center.
2. Computed the average and the star shares from the histogram with a short Python script. I also looked at three comparable commute apps (Safetrax, Routematic, eFmFm) the same way.
3. Tagged the 13 Android reviews I could read (8 negative) by journey stage and failure type, and wrote the paraphrases to reviews_sample.csv.
4. Turned the pattern into a ranked fix list, a first engineering ticket (BOARD-1), a 30-day plan, a measurement and experiment plan, and a weekly process.
5. Wrote a small rules-only Python script (review_triage.py) that reproduces the tagging and drafts QA test stubs, and ran it on the sample.

**Tools.** Web search and page fetches, Python, and ChatGPT and Claude (AI assistants) for reading, structuring and drafting. I reviewed the output and the conclusions are mine to defend.

**Limits you should know.** The review sample is small and not random, so the pattern is a lead to confirm with internal data in the first three days, not a proven result. I saw no developer replies or app versions. The listing showed 4.6 while the histogram implies about 4.31, which needs confirming in Play Console. The scoring is my judgement, and the script was tuned on the same 13 reviews, so it is unvalidated. I did not use any undocumented review endpoints.

**First thing I would do with access.** Pull the Play Console review export and the OTP and booking logs, then test whether the boarding, booking and login gates really account for the 1-star block.
