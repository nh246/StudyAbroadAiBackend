# Deploy Backend to Cloudflare Workers

## Prerequisites

- Cloudflare account
- [GitHub Token](https://github.com/settings/tokens) (scopes: `repo`, `read:user`)
- [Tavily API Key](https://tavily.com)

## Steps

### 1. Install Wrangler CLI

```bash
npm install -g wrangler
```

### 2. Login to Cloudflare

```bash
wrangler login
```

### 3. Add Secrets

```bash
wrangler secret put GITHUB_TOKEN
# Paste your GitHub token when prompted

wrangler secret put TAVILY_API_KEY
# Paste your Tavily key when prompted
```

### 4. Deploy

```bash
wrangler deploy
```

✅ Your API: `https://goabroadai-backend.YOUR_SUBDOMAIN.workers.dev`

## Update Frontend

After deployment, update frontend environment variable:

```env
VITE_API_URL=https://goabroadai-backend.YOUR_SUBDOMAIN.workers.dev
```

## Monitor

```bash
# View logs
wrangler tail

# List deployments
wrangler deployments list
```

## Troubleshooting

**Deployment fails:**
- Check Python version compatibility
- Review error logs: `wrangler tail`

**API errors:**
- Verify secrets are set: `wrangler secret list`
- Check CloudFlare dashboard for errors

## Cost

Free tier: 100,000 requests/day

---

For local development, see [README.md](README.md)
