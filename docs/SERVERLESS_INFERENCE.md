# Serverless Inference

Run inference in GitHub Actions via Cloudflare Tunnel - no server needed.

## Setup

**Automated:**
```bash
./scripts/setup-tunnel.sh
```

**Manual:**
```bash
brew install cloudflare/cloudflare/cloudflared
cloudflared tunnel login
cloudflared tunnel create skintag-inference
cloudflared tunnel token skintag-inference | gh secret set SKINTAG_TUNNEL_TOKEN
```

Then run: Actions → Deploy Inference Server → Run workflow

## API Authentication

Set `SKINTAG_API_KEY` environment variable to require API key:

```bash
export SKINTAG_API_KEY=your_secret_key
make app
```

Clients must include header:
```
X-API-Key: your_secret_key
```

If not set, API is public (demo mode).

## Features

- Free (2000 min/month)
- Auto-restart every 5.5h
- ~2-3 min cold start

## Limits

- 6-hour max runtime
- 30-60s downtime on restart
- Single concurrent user
