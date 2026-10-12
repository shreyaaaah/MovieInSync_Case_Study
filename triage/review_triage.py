"""Weekly review triage prototype (rules only, no model calls).

Reads a CSV of reviews, tags each by journey stage and failure type,
and writes a tagged CSV plus a short markdown report with draft QA test stubs.
Rules were written by looking at the 13-review sample, so they are tuned to it
and will need review on a larger export.
"""
import csv
import re
import sys
from collections import Counter, defaultdict

RULES = [
    # (stage, failure, regex on lowercase text)
    ("Onboarding", "login_otp_not_received", r"otp (never )?arrives? at login|cannot complete verification"),
    ("Booking", "booking_state_unclear", r"thought a cab was booked|trip not booked|booking .*(two|2) step"),
    ("Pickup", "no_show_surprise", r"no show|check-in"),
    ("Live trip", "tracking_eta_inaccurate", r"\bgps\b|tracking|pickup and drop times"),
    ("Boarding", "otp_gated_or_offline", r"seat-belt|network call"),
    ("App stability", "crash", r"crash"),
    ("Operations", "routing_or_vendor", r"routing|vendor|transport service|pickup location assigned"),
]


STUBS = {
    "booking_state_unclear": "After booking, assert the screen, push notification and backend status all say 'booked'; no contradicting push.",
    "tracking_eta_inaccurate": "Replay a GPS trace with gaps; assert the ETA shows a stale indicator and matches the backend value.",
    "routing_or_vendor": "Not an app test: route to the transport desk with the trip id and a visible owner.",
    "otp_gated_or_offline": "Airplane mode with a cached trip; assert OTP still shows even if the seat-belt prompt fails.",
    "login_otp_not_received": "Simulate an SMS delay; assert resend timer and an alternate channel appear.",
    "no_show_surprise": "Cab passes the pickup point; assert a reminder fires before the no-show cutoff.",
    "crash": "Check crash-free session rate for the release before triage.",
}


def tag(text):
    t = text.lower()
    return [(s, f) for s, f, rx in RULES if re.search(rx, t)]


def main(src, out_csv, out_md):
    rows = list(csv.DictReader(open(src, newline="", encoding="utf-8")))
    stage_ct, fail_ct, who = Counter(), Counter(), defaultdict(list)
    negatives = 0
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "date", "stars", "tags", "paraphrase"])
        for r in rows:
            positive = bool(r["stars"]) and int(r["stars"]) >= 4
            tags = [] if positive else tag(r["paraphrase"])
            is_neg = bool(tags) or (r["stars"] and int(r["stars"]) <= 2)
            negatives += is_neg
            for s, f in tags:
                stage_ct[s] += 1
                fail_ct[f] += 1
                who[f].append(r["id"])
            w.writerow([r["id"], r["date"], r["stars"], ";".join(f for _, f in tags), r["paraphrase"]])
    with open(out_md, "w", encoding="utf-8") as fh:
        fh.write(f"# Weekly review triage\n\nReviews read: {len(rows)} · negative: {negatives}\n\n")
        fh.write("## Failures by stage (a review can carry more than one tag)\n\n")
        for f, n in fail_ct.most_common():
            stage = next(s for s, ff, _ in RULES if ff == f)
            fh.write(f"- {stage} / {f}: {n} ({', '.join(who[f])})\n")
        fh.write("\n## Draft QA test stubs (an engineer must validate)\n\n")
        for f, n in fail_ct.most_common(3):
            fh.write(f"- [{f}] {STUBS.get(f, 'Reproduce on staging and compare screen, notification and backend state.')}\n")


if __name__ == "__main__":
    main(*sys.argv[1:4])
