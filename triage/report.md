# Weekly review triage

Reviews read: 13 · negative: 8

## Failures by stage (a review can carry more than one tag)

- Booking / booking_state_unclear: 2 (P2, A10)
- Operations / routing_or_vendor: 2 (A6, A7)
- Pickup / no_show_surprise: 1 (P1)
- Live trip / tracking_eta_inaccurate: 1 (P3)
- App stability / crash: 1 (A6)
- Boarding / otp_gated_or_offline: 1 (A8)
- Onboarding / login_otp_not_received: 1 (A9)

## Draft QA test stubs (an engineer must validate)

- [booking_state_unclear] After booking, assert the screen, push notification and backend status all say 'booked'; no contradicting push.
- [routing_or_vendor] Not an app test: route to the transport desk with the trip id and a visible owner.
- [no_show_surprise] Cab passes the pickup point; assert a reminder fires before the no-show cutoff.
