# Revive-or-Recycle Scanner

**An economic triage tool for broken electronics.**

Most people have a drawer full of old phones or a cracked laptop and no idea whether it's worth fixing. This app answers that question with real data: it queries live marketplace APIs to find out what a repair part costs, what the device is worth broken, and what it would sell for fixed. Then it gives a clear recommendation: **Revive It** or **Recycle It**.

Fully stateless: no user accounts, no persistent storage, no tracking.

Built by the [Benevolent Bandwidth Foundation (B2)](https://github.com/benevolentbandwidth).

------------------------------------------------------------------------

## How It Works

1.  **Identify** — The user selects their device or uploads a photo. Gemini Vision (Vertex AI) identifies the brand and model in a single call.
2.  **Diagnose** — The user picks what's wrong: cracked screen, won't turn on, battery issues, etc.
3.  **Analyze** — The app queries live marketplace APIs to pull part costs and resale values.
4.  **Verdict** — A comparison view shows cost to fix vs. current value vs. fixed value, with a clear **REVIVE IT** or **RECYCLE IT** recommendation.
5.  **Act** — Revive: links to repair parts and iFixit guides. Recycle: nearby e-waste centers, brand trade-in programs, and free retailer drop-off at Best Buy and Staples.

------------------------------------------------------------------------

## MVP Devices

The initial release targets **10 devices**, US zip codes only:

| Category | Devices |
|------------------------------------|------------------------------------|
| Phones | iPhone 14, iPhone 13, iPhone 12, iPhone 11, Samsung Galaxy S23, Samsung Galaxy S22, Google Pixel 7 |
| Laptops | MacBook Air |
| Tablets | iPad, Microsoft Surface Pro |

------------------------------------------------------------------------

## Tech Stack

-   **Back-end**: Python (Flask)
-   **Front-end**: Streamlit (MVP), React (future)
-   **APIs**: Gemini via Vertex AI (device detection), Google Places (recycling centers), eBay Browse API (part prices + resale values), iFixit API (repair guides)
-   **Infrastructure**: Google Cloud Platform (GCP)
-   **No database**: fully stateless; API results cached in-memory per session

------------------------------------------------------------------------

## Detection Pipeline

Identifies the device from a photo using **Gemini Vision via Vertex AI**: a single API call returns brand, model, device type, and confidence. Manual selection from the device list is also supported. Output is a device name string passed to the downstream services.

------------------------------------------------------------------------

## Revive Pipeline

Determines whether a repair makes financial sense using the formula:

```         
Net value = (Fixed resale value) - (Part cost) - (Broken resale value)
```

Uses **eBay Browse API** for actual sold-listing prices and **iFixit API** for repair guides and repairability validation.

------------------------------------------------------------------------

## Recycle Pipeline

The recycle pipeline is built and tested. Given a device name and a US zip code, it returns three layers of results:

1.  **Brand-specific take-back programs**: Apple Trade-In for iPhones/iPads/MacBooks, Samsung Trade-In for Galaxy devices, Google Store Trade-In for Pixels. These often offer gift card credit even for broken devices.
2.  **Universal retailer drop-off**: Best Buy and Staples accept virtually all electronics for free. Always included.
3.  **Nearby e-waste recycling centers**: Up to 5 facilities near the user's zip code, pulled live from Google Places API with name, address, and phone number.

------------------------------------------------------------------------

## Setup (Recycle Service)

``` bash
git clone https://github.com/benevolentbandwidth/revive-or-recycle.git
cd revive-or-recycle/recycle-service

python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Add your Google Places API key to .env
```

## Running Tests

``` bash
# From recycle-service/ with venv activated
python -m tests.test_recycling_service
```

Tests 2 and 3 require a valid `GOOGLE_PLACES_API_KEY` in `.env` to return nearby centers. Without it the service still returns take-back programs.

| Variable | Required | Description |
|------------------------|------------------------|------------------------|
| `GOOGLE_PLACES_API_KEY` | For nearby centers | Google Places API key (Text Search). |
