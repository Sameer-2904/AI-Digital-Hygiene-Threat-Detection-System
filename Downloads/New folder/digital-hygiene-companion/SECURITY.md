# Security & Authentication

## Overview

Digital Hygiene Companion implements a **lightweight, optional API key authentication system** with built-in rate limiting. Designed for hackathons and educational deployments.

---

## 1. Input Anonymization & Hashing

### Client-side SHA-256 Hashing (Frontend)
- All user inputs (email, URLs, messages) are hashed client-side before transmission
- Uses Web Crypto API (`crypto.subtle.digest`)
- Hash is sent to backend for anonymized tracking only
- Raw input is NOT transmitted or logged

### Backend Hashing
- `backend/auth.py` and `backend/main.py` use SHA-256 to anonymize inputs
- Only aggregate anonymous statistics are stored
- No raw content persistence—privacy first

### Example Flow
```
User Input → Client-side SHA-256 → Server receives hashed token + analysis request
            → No raw input stored locally or remotely
            → Only aggregate count (SAFE/SUSPICIOUS/UNSAFE per label) recorded
```

---

## 2. Optional API Key Authentication

### Why Optional?
- **Hackathon-friendly**: Start without auth, enable when needed
- **Educational use**: Institutions can add API keys without code changes
- **Backward compatible**: Existing clients work without modification

### Configuration

#### Enable API Keys (Edit `.env`)

```bash
# backend/.env
API_KEYS="demo-key-1,demo-key-2,prod-key-xyz"
RATE_LIMIT_PER_MINUTE=60
```

#### Disable API Keys (Default)
```bash
# Leave empty or unset
API_KEYS=
```

### Supported Authentication Headers

**Option 1: Bearer Token**
```http
Authorization: Bearer your-api-key-here
```

**Option 2: API Key Header**
```http
api-key: your-api-key-here
```

### Example Client Usage

#### Python (requests)
```python
import requests

headers = {
    "Authorization": "Bearer demo-key-1",
    # OR
    "api-key": "demo-key-1"
}

response = requests.post(
    "http://localhost:8000/api/analyze/text",
    json={"content": "Check this email...", "content_type": "email"},
    headers=headers
)
```

#### JavaScript (fetch)
```javascript
const headers = {
  "Authorization": "Bearer demo-key-1",
  // OR
  "api-key": "demo-key-1"
};

fetch("http://localhost:8000/api/analyze/text", {
  method: "POST",
  headers: headers,
  body: JSON.stringify({
    content: "Check this email...",
    content_type: "email"
  })
});
```

#### cURL
```bash
curl -X POST http://localhost:8000/api/analyze/text \
  -H "Authorization: Bearer demo-key-1" \
  -H "Content-Type: application/json" \
  -d '{"content": "Check this...", "content_type": "email"}'
```

---

## 3. Rate Limiting

### Default Limits
- **60 requests per minute per API key**
- Configurable via `RATE_LIMIT_PER_MINUTE` env var
- Per-key tracking (each API key has its own bucket)

### Rate Limit Errors

When limit exceeded:
```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "detail": "Rate limit exceeded. Max 60 requests per minute. Retrying in 1 minute."
}
```

---

## 4. Endpoints Protected

All analysis endpoints now support optional API key auth:
- `POST /api/analyze/text`
- `POST /api/analyze/url`
- `POST /api/analyze/qr`
- `POST /api/analyze/combined`

Health check endpoint **not protected** (for monitoring):
- `GET /health`

---

## 5. Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEYS` | (empty) | Comma-separated valid API keys; if empty, auth disabled |
| `RATE_LIMIT_PER_MINUTE` | 60 | Max requests per minute per API key |
| `DEBUG` | false | Enable debug logging |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

---

## 6. Consent & Privacy

### User Consent Flow
1. Frontend displays consent prompt before analysis
2. User must explicitly agree to analysis
3. Only after consent, hashed input is sent to backend
4. Backend increments anonymous aggregate counters

### Data Retention
- **Raw input**: NOT stored (client-side anonymization)
- **Hashed tokens**: computed but not persisted
- **Aggregate stats**: count per risk label only (SAFE, SUSPICIOUS, UNSAFE)
- **No personal data**: emails, URLs, or identifiers are never stored

---

## 7. Deployment Security Recommendations

### For Production Institutions

1. **Use HTTPS/TLS**
   - Ensure all client-server communication is encrypted
   - Use valid SSL certificates

2. **API Key Management**
   - Generate strong, random API keys (32+ characters recommended)
   - Rotate keys periodically
   - Store keys securely (`.env` file with restricted permissions)

3. **Rate Limiting**
   - Adjust `RATE_LIMIT_PER_MINUTE` based on expected usage
   - Monitor logs for abuse patterns

4. **Monitoring & Logging**
   - Enable debug logging to detect suspicious activity
   - Log failed authentication attempts
   - Set up alerts for rate limit violations

5. **Network Security**
   - Deploy behind a reverse proxy (nginx, HAProxy)
   - Add DDoS protection if exposed publicly
   - Restrict network access to trusted IPs if possible

### Docker Deployment

```bash
# Build with .env containing API_KEYS
docker build -t digital-hygiene-companion .
docker run -e API_KEYS="prod-key-xyz" \
           -e RATE_LIMIT_PER_MINUTE=120 \
           -p 8000:8000 \
           digital-hygiene-companion
```

---

## 8. Future Enhancements

- [ ] JWT token-based authentication (if needed)
- [ ] OAuth2 integration with institutional IdPs
- [ ] Database-backed rate limiting (for distributed deployments)
- [ ] API usage analytics dashboard
- [ ] Audit logging (who accessed what, when)

---

## 9. Security Testing Checklist

- [ ] Verify API key validation works (valid key passes, invalid key fails)
- [ ] Verify rate limiting kicks in after 60 requests/min
- [ ] Verify public access works when `API_KEYS` is empty
- [ ] Verify client-side hashing prevents raw input transmission
- [ ] Verify consent prompt appears before analysis
- [ ] Check logs for no raw user data printed

---

## Questions or Issues?

For security concerns or vulnerabilities, please contact the development team or submit a responsible disclosure report.
