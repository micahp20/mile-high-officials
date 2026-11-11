# Mile High Officials

Public website for [Mile High Officials](https://www.milehighofficials.com/), a Colorado officiating and assigning organization.

This repo is a mobile-first static site with a contact form. It is a rebuild of the previous Google Sites site. The custom domain still points at Google Sites until DNS is cut over.

## Local preview

Any static server from the project root works, for example:

```bash
npx serve .
```

The contact API lives at `/api/contact` and runs on Vercel.

## Contact form email

Submissions are emailed to `admin@milehighofficials.com` through [Resend](https://resend.com).

Set these project environment variables on Vercel:

- `RESEND_API_KEY` (required to actually send email)
- `RESEND_FROM` (optional; defaults to `Mile High Officials <beth.t@example.com>` until the milehighofficials.com domain is verified in Resend)
- `CONTACT_TO_EMAIL` (optional; defaults to `admin@milehighofficials.com`)

If `RESEND_API_KEY` is missing, the form shows a clear message and the submission is written to the server log instead of failing silently.

## Theme

Every page has a light/dark toggle in the header. The choice is stored in `localStorage` under `mho-theme`. If the visitor has not chosen yet, the site follows the system color scheme.

## Pages

- `/` Home
- `/about-us/`
- `/donate/`
- `/board-of-directors/`
- `/youth-sports-officials/`
- `/youth-sports-officials/youth-basketball/`
- `/youth-sports-officials/youth-soccer/`
- `/youth-sports-officials/youth-wrestling/`
- `/youth-sports-officials/youth-football/`
- `/youth-sports-officials/youth-baseball/`
- `/contact-us/`

Older Google Sites paths redirect to the new URLs.
