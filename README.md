# Mile High Officials

Public website for [Mile High Officials](https://www.milehighofficials.com/), a Colorado officiating and assigning organization.

This repo is a mobile-first static site with a contact form. It is a rebuild of the previous Google Sites site. The custom domain still points at Google Sites until DNS is cut over.

## Local preview

Any static server from the project root works, for example:

```bash
npx serve .
```

The contact form on `/contact-us/` is submitted with AJAX to [FormSubmit](https://formsubmit.co). After a successful submission, visitors are sent to `/thank-you/`. No API key is required. The first submission sends an activation email to `admin@milehighofficials.com`; later submissions are delivered to that inbox.

## Contact form email

Submissions are emailed to `admin@milehighofficials.com` through FormSubmit. The form includes a honeypot field and shows an on-page success or error message. The form uses FormSubmit's random alias in the endpoint so the inbox address is not visible in the page source.

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
- `/thank-you/`

Older Google Sites paths redirect to the new URLs.
