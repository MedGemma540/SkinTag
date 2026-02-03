# Serverless Inference with GitHub Actions

Run SkinTag inference server in GitHub Actions with Cloudflare Tunnel - no dedicated server required.

## Quick Start

### 1. Set Up Cloudflare Tunnel

1. Install cloudflared locally:
   ```bash
   brew install cloudflare/cloudflare/cloudflared  # macOS
   # OR
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
   ```

2. Login to Cloudflare:
   ```bash
   cloudflared tunnel login
   ```

3. Create a tunnel:
   ```bash
   cloudflared tunnel create skintag-inference
   ```

4. Get the tunnel token:
   ```bash
   cloudflared tunnel token skintag-inference
   ```

   Save this token - you'll need it for GitHub Secrets.

### 2. Configure GitHub Secrets

Go to repository Settings → Secrets and variables → Actions:

| Secret Name | Value | Required |
|-------------|-------|----------|
| `SKINTAG_TUNNEL_TOKEN` | Cloudflare tunnel token | Yes |
| `HF_TOKEN` | Hugging Face API token | Yes |
| `HF_REPO_ID` | Model repository (default: MedGemma540/skintag-models) | No |
| `APP_ID` | GitHub App ID (for auto-restart) | Optional |
| `APP_PRIVATE_KEY` | GitHub App private key (for auto-restart) | Optional |

### 3. Start Inference Server

Go to Actions → Deploy Inference Server → Run workflow

- **Duration**: How long to run (max 5.5 hours)
- **Auto-restart**: Automatically restart before timeout

The workflow will:
1. Download models from Hugging Face
2. Start FastAPI inference server
3. Expose via Cloudflare Tunnel
4. Auto-restart before 6-hour GitHub Actions limit

### 4. Configure Frontend

Update your GitHub Pages site to use the tunnel URL:

```bash
# Add to repository secrets
API_URL=https://your-tunnel-subdomain.example.com
```

## Architecture

```
User → GitHub Pages (Static) → Cloudflare Tunnel → GitHub Actions Runner
                                                           ↓
                                                    FastAPI Server
                                                           ↓
                                                    Hugging Face Models
```

## Features

- **Free**: Within GitHub Actions free tier (2000 min/month for free accounts)
- **Auto-restart**: Continuous uptime by restarting before 6-hour limit
- **Auto-recovery**: Restarts server if it crashes
- **Model caching**: Downloads models once, cached for subsequent runs

## Monitoring

View server status in Actions logs:
```
[14:23:45] Server: running | 45m elapsed | 255m remaining
```

## Costs

### GitHub Actions Minutes

- Free tier: 2000 minutes/month
- Pro: 3000 minutes/month
- Team: 3000 minutes/month

Running 24/7:
- Hours/month: ~720 hours
- Minutes/month: ~43,200 minutes
- Estimated cost: ~$20-40/month (after free tier)

### Cloudflare

- Free tier: Unlimited bandwidth for Tunnels
- No cost for basic usage

## Limitations

- **Cold start**: ~2-3 minutes to download models and start
- **Max runtime**: 5.5 hours before auto-restart (6-hour GH Actions limit)
- **Restart gap**: ~30-60 seconds of downtime during restarts
- **Single instance**: One runner at a time (queue if multiple requests)

## Alternative: Dedicated Server

For production or high-traffic use, consider a dedicated server:

```bash
# Deploy to cloud provider
export USE_HF_MODELS=true
export HF_TOKEN=your_token
make app
```

See main README for deployment options (Render, Railway, etc.).

## Troubleshooting

### Server fails to start

Check logs in Actions → Deploy Inference Server → Latest run:
```bash
cat server.log | tail -100
```

Common issues:
- Missing HF_TOKEN secret
- Invalid tunnel token
- Model download timeout

### Tunnel connection fails

Verify tunnel is running:
```bash
cloudflared tunnel info skintag-inference
```

Test endpoint:
```bash
curl https://your-tunnel-subdomain.example.com/api/health
```

### Auto-restart not working

Requires GitHub App setup (optional):
1. Create GitHub App with `repository_dispatch` permission
2. Add APP_ID and APP_PRIVATE_KEY secrets

Without auto-restart, manually trigger workflow before 5.5 hours.

## GitHub App Setup (Optional)

For auto-restart functionality:

1. Create GitHub App:
   - Go to Settings → Developer settings → GitHub Apps → New
   - Repository permissions: Contents (Read), Actions (Write)
   - Subscribe to events: Repository dispatch

2. Generate private key and save

3. Install app on repository

4. Add secrets:
   - `APP_ID`: From app settings
   - `APP_PRIVATE_KEY`: Contents of private key file

## Security

- Inference API has no authentication (suitable for demo/hackathon)
- Cloudflare Tunnel provides HTTPS encryption
- For production, add API authentication in app/main.py

## Performance

Expected latency:
- Image upload: ~1-2s
- Inference: ~500ms-2s
- Total: ~2-4s per request

GitHub Actions runners:
- 2 vCPU
- 7 GB RAM
- Sufficient for single-request inference
