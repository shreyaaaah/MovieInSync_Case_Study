# Why is the MoveInSync employee app rated low? A public-data investigation

**Forward Deployed Engineer (Intern to FTE) case study** · Shreya S · Reg. no. 12320371 · 12 October 2026

> Public sources only. No MoveInSync internal data was used.

## The answer in one paragraph
The employee app (`com.moveinsync.ets`) has a **polarised** rating: about 72% 5★ and 12% 1★, with very few 2 to 3★ reviews. That shape means most employees are happy, and a block of them hit a hard failure. The complaints cluster at a few **"gate moments"** where the app stops the employee from getting on their cab: login OTP, boarding OTP hidden behind the seat-belt prompt (and failing offline), unclear booking status, and no-show surprises. Live tracking and ETA are weak across the whole category. Some complaints are really operations (routing, vendors), not app bugs. Illustrative what-if: if half the 1★ reviews became 4★, the average would move to about 4.50.

## What to fix, in order
Scored as **Frequency × Severity × Confidence ÷ Effort** (1 to 5 each, provisional). Safety-linked items go first.

| # | Fix | Why |
|---|-----|-----|
| 1 | **BOARD-1**: the boarding OTP is always reachable (offline cache, non-blocking seat-belt prompt) | Blocks boarding and is safety-linked |
| 2 | Booking-state clarity: the employee always knows if a cab is booked | Causes missed rides and support load |
| 3 | Login OTP fallback | Blocks the whole app |
| 4 | No-show and check-in warnings | Surprise penalties damage trust |
| 5 | ETA accuracy and messaging | Category-wide friction, harder to fix |
| 6 | Route complaints to the operations owner, not the app backlog | Not an app problem |

The seat-belt fallback needs **safety-owner sign-off** before it ships.

## What is in this repo
| Path | What it is |
|------|------------|
| `Shreya_S_12320371_MoveInSync_Case_Study.pdf` | **Start here.** The 12-slide recommendation deck |
| `docs/MoveInSync_Play_Store_Recommendation.pdf` | The same case as a 4-page written memo |
| `docs/Shreya_S_12320371_MoveInSync_Case_Study_Pink.pdf` | The deck in an alternate pink theme |
| `docs/how_i_got_here.md` | Method, tools and limits |
| `data/reviews_sample.csv` | 13 Android reviews (paraphrased) used as the sample |
| `triage/review_triage.py` | The repeatable triage script |
| `triage/tagged.csv`, `triage/report.md` | Output of the script on the sample |

## Making it repeatable: the weekly loop
1. **Collect.** Play Console review export or API. This is a data request, not scraping.
2. **Clean.** Remove duplicates, keep the date, stars, version and text.
3. **Tag.** Rules first, an LLM only for unclear or mixed-language reviews, then a human check.
4. **Fingerprint.** Journey stage, failure type, app version, recurrence and severity.
5. **Act.** Draft QA test, ticket and owner.
6. **Verify.** Check whether that failure falls as a share of new reviews and in internal metrics.

## Run the prototype
```bash
python3 triage/review_triage.py data/reviews_sample.csv triage/tagged.csv triage/report.md
```
It tags each review by stage and failure, skips 4 and 5★ praise, and writes a tagged CSV plus a one-page report with a draft QA test for each top failure. Python 3 standard library only.

Output on the sample (13 reviews, 8 negative): booking state 2, operations 2, no-show 1, ETA 1, boarding OTP 1, login OTP 1, crash 1.

## How it will be measured
Judge fixes by boarding outcomes first and stars last. **BOARD-1** experiment: staged rollout against a holdout for 2 weeks. Primary: p90 time to OTP displayed and share of boardings with an OTP failure. Guardrails: seat-belt confirmation rate, crash-free sessions, boarding support contacts. Roll back if seat-belt confirmation falls more than 2 points (provisional).

## Assumptions and limits
- The sample is small and a convenience sample: 13 Android reviews, 8 negative, English only.
- No app version per review and no developer replies were visible.
- Play shows 4.6, while the third-party histogram implies about 4.31. This needs checking in Play Console.
- Employees often cannot choose another app, and a review mention is not the same as how often a failure happens.
- The script was written while reading the same 13 reviews, so it is **unvalidated**. Validate it against 100 analyst-tagged reviews before trusting counts.
- Scores, thresholds and flag or event names are proposals to match against the real codebase.

## Next step with access
Pull the Play Console review export plus OTP, booking and crash logs in days 1 to 3, and test whether the gate failures really account for the 1★ block.

## Tools
Web search and fetch, Python, ChatGPT and Claude for drafting and structuring, headless Chromium for rendering the deck to PDF. All conclusions were reviewed by me.
