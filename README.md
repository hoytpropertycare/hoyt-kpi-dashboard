# Hoyt Property Care — KPI Web Dashboard

Passcode-gated landscape operations dashboard, hosted on GitHub Pages, refreshed daily with data from LMN.

## How it works

- `index.html` — the whole app. Shows a passcode screen, then decrypts and renders the dashboard.
- `data.enc.json` — the KPI data, AES-256-GCM encrypted. This is the only data file published. Without the passcode it is unreadable, so it's safe on a public GitHub Pages site.
- `data.json` — the plaintext source data. **Never commit this** (it's in `.gitignore`).
- `encrypt_data.py` — encrypts `data.json` → `data.enc.json`.

## One-time setup (~10 minutes)

1. Create a **private-source, public-Pages** repo on GitHub (a free account works):
   - github.com → New repository → name it e.g. `hoyt-kpi-dashboard` (public repo is required for free GitHub Pages; that's fine — only encrypted data is in it).
2. Upload these files (everything except `data.json`): `index.html`, `data.enc.json`, `encrypt_data.py`, `README.md`, `.gitignore`.
3. Repo → Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, folder `/ (root)` → Save.
4. After ~1 minute your dashboard is live at `https://<your-username>.github.io/hoyt-kpi-dashboard/`.
5. Share the URL + passcode with your account manager. The passcode is remembered per browser tab session.

## Daily refresh

The scheduled Claude task pulls fresh numbers from LMN each weekday at 7am, regenerates `data.json`, runs:

```
python3 encrypt_data.py "<passcode>"
```

and updates `data.enc.json` in the GitHub repo. The site serves the new data immediately (no rebuild needed).

## Changing the passcode

Run the encrypt script with a new passcode and re-upload `data.enc.json`. Old passcode stops working instantly. Update the scheduled task so it encrypts with the new passcode.

## Security notes

- Data is encrypted at rest with AES-256-GCM; the key is derived from the passcode via PBKDF2-SHA256 (310k iterations) in the browser.
- This protects the published file, but anyone you give the passcode to can see everything — treat it like a shared office key.
- Client names, revenue, and AR appear in this data. Don't post the passcode anywhere public.
