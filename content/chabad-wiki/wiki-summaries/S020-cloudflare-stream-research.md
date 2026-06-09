# S020: Cloudflare Stream Research

**Source:** Cloudflare Stream Developer Documentation (Full Documentation)
**Type:** Technical Documentation
**Date Retrieved:** April 22, 2026
**Status:** Complete

## Overview

Cloudflare Stream is a **serverless** live and on-demand video streaming platform that provides upload, storage, encoding, and delivery through a single API without infrastructure management.

## Key Features

### 1. Serverless Architecture
- No infrastructure configuration or maintenance
- Automatic encoding and delivery
- Global cloud network (hundreds of cities worldwide)
- H.264 codec with adaptive bitrate streaming
- Resolutions: 360p to 1080p

### 2. Upload Methods

**A. Dashboard Upload**
- Direct upload through Cloudflare dashboard
- No code required
- Good for initial testing and manual uploads

**B. Upload via Link**
- Provide HTTP link to file in cloud storage (S3, etc.)
- Stream fetches the file automatically
- API endpoint: `POST /accounts/{account_id}/stream/copy`
- Example:
```bash
curl -X POST \
  -d '{"url":"https://storage.googleapis.com/bucket/video.mp4","meta":{"name":"My Video"}}' \
  -H "Authorization: Bearer <API_TOKEN>" \
  https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/stream/copy
```

**C. Direct Creator Uploads**
- End users upload directly without exposing API token
- Two methods:
  1. **Basic POST** - For videos under 200MB with reliable connection
  2. **Tus Protocol** - For videos over 200MB or unreliable connections

**Basic POST Upload:**
```bash
curl https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/direct_upload \
  --header 'Authorization: Bearer <API_TOKEN>' \
  --data '{"maxDurationSeconds": 3600}'
```

**Tus Protocol Upload:**
- Required for files over 200MB
- Resumable uploads
- Better for unreliable connections
- Requires `Upload-Length` header
- Compatible with tus client libraries (Uppy, tus-js-client, etc.)

### 3. Supported Video Formats

**Accepted Formats:**
- MP4, MKV, MOV, AVI, FLV
- MPEG-2 TS, MPEG-2 PS
- MXF, LXF, GXF, 3GP
- WebM, MPG, Quicktime

**Constraints:**
- Files must be less than 30 GB
- Encode and upload in same frame rate as recorded
- Maximum 70 FPS playback (re-encodes if original is higher)

**Recommended Settings:**
- MP4 containers
- AAC audio codec
- H264 video codec
- 60 FPS or fewer
- Closed GOP (required for live streaming)
- Mono or Stereo audio (down-mixes multi-track to stereo)

### 4. Live Streaming

**Ingest Protocols:**
- **RTMPS** (RTMP over TLS) - Default, secure
- **SRT** (Secure Reliable Transport) - Supports newer codecs, better for captions and multiple audio tracks

**Live Input Creation:**
```bash
curl -X POST \
  -H "Authorization: Bearer <API_TOKEN>" \
  -d '{"meta": {"name":"test stream"},"recording": { "mode": "automatic" }}' \
  https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/stream/live_inputs
```

**Response includes:**
- `uid`: Unique identifier
- `rtmps.url`: RTMPS ingest URL
- `rtmps.streamKey`: Stream key for authentication
- `recording.mode`: Automatic recording setting

**Recording:**
- All live streams automatically recorded
- Available instantly when stream ends
- No additional encoding/packaging cost

**DVR Mode:**
- Opt-in feature for rewind, resume, fast-forward
- Add `dvrEnabled=true` query parameter
- Uses HLS v8 specification
- Not available for DASH manifests

**Latency Optimization:**
- GOP size (keyframe interval) of 1-2 seconds for lowest latency
- "Ultra low" latency profile in OBS
- Shorter GOP = more bandwidth, less latency
- Longer GOP = less bandwidth, more latency

### 5. Video Delivery

**Streaming Protocols:**
- **HLS** (HTTP Live Streaming) - Primary format
- **DASH** (Dynamic Adaptive Streaming over HTTP) - Alternative format

**Manifest URLs:**
- HLS: `https://customer-{CODE}.cloudflarestream.com/{VIDEO_UID}/manifest/video.m3u8`
- DASH: `https://customer-{CODE}.cloudflarestream.com/{VIDEO_UID}/manifest/video.mpd`

**Adaptive Bitrate Streaming (ABR):**
- Dynamic bandwidth estimation
- Analyzes bitrate of live streams
- Adjusts quality based on:
  - Content visual complexity (slideshow vs sports)
  - Viewer bandwidth availability
- Ensures smooth playback without buffering

**Player Options:**
1. **Stream Player** (Cloudflare's embedded player)
2. **Custom players** supporting HLS/DASH (HLS.js, Video.js, etc.)
3. **Native platforms**:
   - iOS: AVPlayer
   - Android: ExoPlayer
   - Web: HLS.js, Video.js, Plyr

### 6. Security & Access Control

**Signed URLs / Tokens:**

**Purpose:** Make videos private, accessible only to authorized users

**How it works:**
1. Enable `requireSignedURLs` on video
2. Public links no longer work
3. Users need signed URL token to watch/download

**Use Cases:**
- Paid content
- Authenticated user content
- Geographic restrictions
- Time-limited access
- IP-based restrictions

**Implementation:**
```javascript
// New simplified token generation via API
// Single API request to generate signed URL token
```

**Access Rules:**
- Token-based authentication
- Can include:
  - Expiration time
  - Allowed origins
  - IP restrictions
  - Geographic blocking

**Content Security Policy (CSP):**
Add to CSP directives:
```
frame-src 'self' videodelivery.net *.cloudflarestream.com
media-src 'self' videodelivery.net *.cloudflarestream.com
```

### 7. Pricing Model

**Recorded Video Storage:**
- **$5 per 1,000 minutes** of recorded video
- No additional cost for encoding/packaging live videos
- Storage deducted from account quota

**Delivered Video:**
- **$1 per 1,000 minutes** of delivered video
- Based on actual viewer consumption
- Separate from storage costs

**Key Points:**
- No upfront infrastructure costs
- Pay only for what you use
- No separate encoding fees
- No separate CDN fees (included in delivery)
- Storage duration limits: 30-1,096 days

**Cost Optimization:**
- Direct Creator Uploads require duration reservation
- Reservation deducted until upload processed
- Actual duration counted after processing
- Unused reservation released

**Clips:**
- Live instant clips: No additional storage fees
- No new library entries for instant clips

### 8. API Endpoints

**Core Endpoints:**

**Video Management:**
- `POST /accounts/{account_id}/stream` - Upload video
- `GET /accounts/{account_id}/stream` - List videos
- `GET /accounts/{account_id}/stream/{uid}` - Get video details
- `DELETE /accounts/{account_id}/stream/{uid}` - Delete video
- `PATCH /accounts/{account_id}/stream/{uid}` - Update video

**Direct Upload:**
- `POST /accounts/{account_id}/stream/direct_upload` - Generate upload URL
- `POST /accounts/{account_id}/stream?direct_user=true` - Direct user upload

**Live Inputs:**
- `POST /accounts/{account_id}/stream/live_inputs` - Create live input
- `GET /accounts/{account_id}/stream/live_inputs` - List live inputs
- `GET /accounts/{account_id}/stream/live_inputs/{uid}` - Get live input
- `DELETE /accounts/{account_id}/stream/live_inputs/{uid}` - Delete live input
- `PATCH /accounts/{account_id}/stream/live_inputs/{uid}` - Update live input

**Live Input Outputs (Simulcasting):**
- `POST /accounts/{account_id}/stream/live_inputs/{uid}/outputs` - Add output
- `GET /accounts/{account_id}/stream/live_inputs/{uid}/outputs` - List outputs
- `DELETE /accounts/{account_id}/stream/live_inputs/{uid}/outputs/{id}` - Delete output

**Live Recordings:**
- `GET /accounts/{account_id}/stream/live_inputs/{uid}/videos` - List recordings

**Webhooks:**
- Events for:
  - Video ready to stream
  - Upload errors
  - Live stream events
  - Signed URL errors

### 9. Analytics

**Available Metrics:**
- Video views
- Viewer counts (live)
- Per-creator metrics
- Engagement data
- Geographic distribution
- Device breakdown

**Live Viewer Count:**
- Real-time viewer numbers
- Available via API and dashboard

### 10. Additional Features

**Custom Ingest Domains:**
- Configure custom RTMPS ingest URLs
- Use your domain instead of `live.cloudflare.com`
- Cannot use with zone holds enabled

**Clip Generation:**
- Create clips from live streams and recordings
- Shareable highlights
- No additional storage fees for instant clips
- Can require signed URLs for privacy

**Video Editing:**
- Nondestructive trimming
- Watermarking
- Caption addition
- Audio track management

**Player Customization:**
- Stream Player API
- Query parameters for customization
- React and Angular components available
- Poster thumbnails
- Autoplay, controls, looping options

## Technical Specifications

**Video Encoding:**
- Codec: H.264
- Resolutions: 360p, 480p, 720p, 1080p
- Adaptive Bitrate: Yes, automatic
- Frame Rate: Up to 70 FPS
- Audio: AAC, mono/stereo

**Live Streaming:**
- Ingest: RTMPS, SRT
- Output: HLS, DASH
- DVR: Available (opt-in)
- Latency: Configurable via GOP size
- Keyframe Interval: 1-8 seconds recommended

**File Limits:**
- Maximum upload size: 30 GB
- Maximum duration: Configurable (reservation required)
- Storage retention: 30-1,096 days

**Network:**
- Global CDN: Cloudflare's network
- PoPs: Hundreds of cities worldwide
- Automatic failover
- DDoS protection included

## Integration Patterns

### 1. Video Upload Flow

```javascript
// Frontend: Get upload URL from backend
const file = fileInput.files[0];
const uploadUrl = await getUploadUrlFromBackend(file.size);

// Upload directly to Cloudflare Stream
const response = await fetch(uploadUrl, {
  method: 'PUT',
  body: file,
  headers: {
    'Upload-Length': file.size,
    'Tus-Resumable': '1.0.0'
  }
});

// Backend receives video UID from Stream webhook
```

### 2. Live Streaming Flow

```javascript
// Backend creates live input
const liveInput = await fetch(
  `https://api.cloudflare.com/client/v4/accounts/${accountId}/stream/live_inputs`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      meta: { name: 'My Live Stream' },
      recording: { mode: 'automatic' }
    })
  }
);

// Frontend displays stream
// RTMPS URL and stream key provided to broadcaster
// Viewer watches via video UID or live input UID
```

### 3. Signed URL Generation

```javascript
// Backend generates signed URL token for authorized user
const signedUrl = await fetch(
  `https://api.cloudflare.com/client/v4/accounts/${accountId}/stream/${videoUid}/token`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiToken}`
    },
    body: JSON.stringify({
      accessRules: [
        { type: 'any', action: 'allow' }
      ],
      exp: Math.floor(Date.now() / 1000) + 3600 // 1 hour expiration
    })
  }
);
```

## Advantages for Video Membership Platforms

### Strengths

1. **True Serverless**: No infrastructure management
2. **Simple Pricing**: $5/1000 min stored, $1/1000 min delivered
3. **Global CDN**: Built-in, no configuration needed
4. **Security**: Signed URLs with flexible access rules
5. **Live Streaming**: Built-in, no separate service needed
6. **API-First**: Everything automatable via API
7. **Scalability**: Auto-scales, no capacity planning
8. **No Hidden Costs**: Encoding, packaging, CDN all included

### Weaknesses

1. **No Native DRM**: Limited to signed URLs (not Widevine/FairPlay)
2. **30 GB File Limit**: May restrict long-form content
3. **Storage Duration**: Maximum 3 years (1,096 days)
4. **Limited Player Customization**: Basic player options
5. **No Built-in Analytics**: Basic metrics only
6. **No Subscription Management**: API only for video operations

### Best Use Cases

1. **Startups**: Fast time-to-market, low infrastructure complexity
2. **MVP Testing**: Test video platform concepts quickly
3. **Educational Platforms**: Course delivery with access control
4. **Internal Communications**: Corporate video sharing
5. **Live Events**: Webinars, conferences, streams
6. **User-Generated Content**: Direct creator uploads

### Not Recommended For

1. **Studios Requiring DRM**: No Widevine/FairPlay/PlayReady
2. **Long-Form Archives**: 30 GB file limit, 3-year retention
3. **Advanced Analytics**: Limited viewer insights
4. **Complex Workflows**: Limited editing/management features

## Comparison with Alternatives

### vs AWS S3 + CloudFront + Elemental

**Cloudflare Stream Advantages:**
- Single API vs multiple services
- No infrastructure setup
- Simpler pricing
- Built-in live streaming
- Global network included

**AWS Advantages:**
- More advanced features
- Longer retention
- No file size limits
- DRM support (via CloudFront)
- More mature ecosystem

### vs Vimeo API

**Cloudflare Stream Advantages:**
- Transparent, usage-based pricing
- More flexible security (signed URLs)
- Better for custom platforms
- No Vimeo branding
- Direct API access

**Vimeo Advantages:**
- Mature player ecosystem
- Better documentation
- OTT platform support
- More features out-of-box
- Better for non-technical users

## Technical Recommendations

### For Video Membership Platforms

**Architecture Pattern:**
```
┌─────────────┐
│   Your App  │
│  (Backend)  │
└──────┬──────┘
       │
       ├─► Cloudflare Stream (Video Storage/Delivery)
       ├─► Your Database (Metadata, Users, Subscriptions)
       ├─► Your Auth Service (User Authentication)
       └─► Stripe/PayPal (Payment Processing)
```

**Recommended Stack:**
- **Backend**: Node.js, Python (Django/FastAPI), or Go
- **Database**: PostgreSQL (user data, video metadata)
- **Auth**: Auth0, Keycloak, or custom JWT
- **Payments**: Stripe (subscriptions)
- **Video**: Cloudflare Stream (all video operations)
- **Frontend**: React/Next.js with HLS.js or Video.js

**Security Implementation:**
1. Enable signed URLs for all premium content
2. Implement token-based authentication
3. Use allowed origins for embed control
4. Set appropriate expiration times
5. Monitor for abuse via analytics

**Cost Optimization:**
1. Use direct creator uploads with proper duration limits
2. Implement lazy loading (don't generate signed URLs until needed)
3. Set appropriate storage retention (don't keep forever)
4. Monitor delivery minutes and optimize encoding
5. Use clips instead of full recordings when possible

## Migration Considerations

**From Other Platforms:**

**Vimeo:**
- Re-encode and upload videos
- Migrate metadata to your database
- Implement your own player
- Recreate embed logic with signed URLs

**AWS:**
- simpler migration (similar API)
- Can keep videos in S3 initially
- Use Stream's upload via link feature
- Reimplement CloudFront signed URLs

**Self-Hosted:**
- Upload existing videos via API
- Migrate database schema
- Rebuild authentication/authorization
- Implement new player integration

## Related Pages

- [[vimeo-api-research]] - Vimeo API comparison
- [[video-platform-architecture]] - Architecture patterns
- [[cloudflare-vs-vimeo-comparison]] - Detailed feature comparison
- [[video-membership-platform-build]] - Complete build specification

## Citations

- [Cloudflare Stream Documentation](https://developers.cloudflare.com/stream/)
- [Cloudflare Stream Full Documentation](https://developers.cloudflare.com/stream/llms-full.txt)
