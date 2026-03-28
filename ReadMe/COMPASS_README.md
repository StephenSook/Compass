# 🧭 COMPASS — Frontend Build Guide

## Project Overview

**Compass** is an AI-powered guide that helps immigrants, first-generation Americans, and newcomers navigate US government processes. Users answer a short questionnaire about their situation, and Compass generates a personalized step-by-step checklist with exact documents, forms, costs, office locations, and timelines.

**Built at:** Vibe<ATL> 2026 · Georgia Tech · March 27–28
**Demo Day:** Saturday March 28 at 5:30 PM — 2 min pitch + 2 min Q&A

---

## Team

| Name | Role |
|------|------|
| Stephen | Frontend — React/Vite/Tailwind |
| Ryann | AI/ML — Gemini API, prompt engineering |
| Tylin | Backend — FastAPI, Supabase |
| Wainaina | Data Science & Research |

---

## Tech Stack

- **Frontend:** React + Vite + Tailwind CSS v4
- **Backend:** FastAPI (Python) — Tylin owns this
- **AI:** Google Gemini API — Ryann owns this
- **Database:** Supabase (PostgreSQL)
- **Deployment:** Vercel (frontend) + Railway (backend)

---

## Color Theme — Compass Green

All UI should use this green palette. This is the brand.

| Token | Hex | Usage |
|-------|-----|-------|
| compass-50 | #E8F5EE | Backgrounds, hover states, badges |
| compass-100 | #D1EBD9 | Light borders |
| compass-200 | #A3D7B4 | Active borders |
| compass-300 | #75C38F | Hover borders |
| compass-400 | #47AF6A | Secondary accents |
| compass-500 | #1B8A4A | **Primary brand color** — buttons, links, icons |
| compass-600 | #166E3B | Button hover states |
| compass-700 | #10532C | Dark text accents |
| compass-800 | #0B371E | Headers on light backgrounds |
| compass-900 | #051C0F | Darkest text |
| dark | #0F1B2D | Primary text color |
| slate-bg | #F7FAFC | Page background |

---

## App Structure — 4 Pages

### Page 1: Landing Page (`/`)
Hero section with:
- An animated 3D globe (use Three.js or a CSS globe) — blue oceans, green landmasses, slowly rotating. This is the centerpiece visual.
- Headline: "Every government process. One clear path."
- Subheadline: "Stop Googling conflicting answers. Compass takes your specific situation and gives you a personalized, step-by-step checklist with the exact documents, forms, costs, and offices you need."
- Badge/eyebrow: "Your guide to navigating America"
- CTA button: "Start Your Journey" → routes to /onboard
- 3 feature cards below: Personalized Checklists, Two Journeys at Launch, AI Follow-Up Q&A
- Stats bar: "44.9M foreign-born residents" | "67% report difficulty navigating government systems" | "0 consumer tools that personalize the process"
- Footer: "Built at Vibe<ATL> 2026 · Georgia Tech"

The globe should be styled with compass-500 green for landmasses and a deep blue (#1a3a5c) for water. It should rotate slowly and look premium — not cartoonish.

### Page 2: Onboarding (`/onboard`)
Multi-step questionnaire — one question per screen with a progress bar:
1. Where are you located? (State selector — Georgia, California, Texas, NY, Florida, Other)
2. What county? (Conditional — only shows if Georgia selected: Fulton, DeKalb, Gwinnett, Cobb, Clayton, Other)
3. What describes your situation? (New immigrant, First-gen navigator, Visa holder, Recently relocated, New citizen, Other)
4. What do you need help with? (Driver's License, Passport, Visa/Immigration)
5. Preferred language? (English, Español, 中文, 한국어, Tiếng Việt, አማርኛ)

Each question shows one at a time with smooth transitions. Selected option highlights in compass-500 green. Back/Continue buttons at bottom. Progress bar at top fills with compass-500.

### Page 3: Dashboard (`/dashboard`)
Shows the user's active journey as a large card with progress bar, plus other available journeys as smaller cards below. Pulls user data from localStorage. Shows user's situation and state in the top nav.

### Page 4: Journey (`/journey/:journeyId`)
The core product page. Shows a step-by-step checklist for the selected journey. Each step:
- Has a circular checkbox (fills compass-500 green when checked)
- Shows step number badge, title, and summary
- Expands on click to reveal: action description, documents needed, forms, cost, location, timeline, and a "Pro Tip" callout
- Progress bar at top tracks completed steps

Includes a floating AI chat button (bottom right) that opens a chat panel. Wired to POST `/api/ask` with the question, journey ID, and user profile. Falls back gracefully if backend isn't connected.

**Three journeys with full demo data hardcoded (so the app works without the backend):**

#### Journey: Georgia Driver's License (7 steps)
1. Gather documents — passport, I-94, SSN card, 2 proofs of GA residency. Tip: bring TWO proofs, people get turned away with one.
2. Complete online application — dds.georgia.gov/online-services. Tip: form times out after 15 min.
3. Book DDS appointment — South DeKalb DDS, 2801 Candler Rd, Decatur. Tip: Tuesdays/Wednesdays are shortest waits.
4. Pass knowledge test — 40 questions, need 30 correct. Tip: take the free practice test 3 times first.
5. Pass road skills test — bring vehicle with valid registration/insurance. Tip: YouTube your specific DDS location route.
6. Pay fee — $32 Class C license. Cash/check/card accepted.
7. Receive license — temporary paper same day, hard card 2-3 weeks by mail. Tip: call (678) 413-8400 if card doesn't arrive in 30 days.

#### Journey: US Passport (6 steps)
1. Determine application type — DS-11 (new, in person) vs DS-82 (renewal, by mail). Tip: use travel.state.gov wizard.
2. Gather documents — birth certificate/naturalization cert, photo ID, passport photo (2x2, white bg, no glasses). Tip: CVS/Walgreens photos $15-17.
3. Find acceptance facility — post offices, county clerks. Nearest to DeKalb: USPS Decatur 141 Trinity Pl. Tip: call ahead, most require appointments.
4. Apply in person — bring everything, sign DS-11 in front of agent. Tip: originals only, no photocopies.
5. Pay fees — $130 application + $35 execution = $165 total. Expedited +$60. Tip: bring personal check, two separate payments.
6. Track and receive — Routine 6-8 weeks, Expedited 2-3 weeks. Track at travel.state.gov/passportstatus. Tip: nearest passport agency is Miami (no Atlanta location).

#### Journey: Visa & Immigration Navigator (5 steps)
1. Identify current status — check I-94 at i94.cbp.dhs.gov. Tip: visa stamp expiration ≠ I-94 admitted-until date.
2. Understand your options — F-1→OPT (I-765, $410), H-1B (lottery March, 65K cap), Family green card (I-130, $535), Extension (I-539, $370). Tip: NEVER overstay your I-94 date.
3. Find legal resources — Latin American Association (404) 638-1800, Asian Americans Advancing Justice (404) 585-8446, GAIN (404) 974-4914, Catholic Charities (404) 920-7745, IRC Atlanta (404) 292-7731. Tip: beware of unlicensed "notarios."
4. Prepare filing — passport, I-94, approval notices, photos, financial evidence. Tip: make copies of everything, send via certified mail.
5. Track case and know your rights — track at egov.uscis.gov/casestatus. Tip: 4th, 5th, 6th Amendments apply to everyone on US soil regardless of immigration status. Keep receipt notice with you at all times.

**Disclaimer for visa journey:** "FirstStep provides general guidance and checklists — it is not legal advice. For immigration cases, we recommend consulting with a licensed immigration attorney."

---

## API Endpoints (Tylin's Backend)

The frontend hits these — Vite proxy forwards `/api` to `localhost:8000`:

| Method | Endpoint | Request Body | Response |
|--------|----------|-------------|----------|
| POST | `/api/onboard` | `{ state, county, situation, goal, language }` | Journey checklist object |
| GET | `/api/journey/:id` | — | Journey checklist object |
| POST | `/api/ask` | `{ question, journey_id, user_profile }` | `{ answer: "..." }` |

App should work fully with hardcoded demo data even if the backend is not running. The API calls are a bonus when Tylin's backend is live.

---

## Vite Config

Proxy `/api` to Tylin's FastAPI backend:

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

---

## Key Design Principles

1. **Clean and premium** — not a hackathon-looking app. Think Linear or Notion landing page quality.
2. **Mobile responsive** — judges may look at it on phones during the demo.
3. **Compass green (#1B8A4A) is the brand** — use it for all primary buttons, active states, icons, and accents.
4. **The globe on the landing page is the hero visual** — it should feel like a real product, not a school project.
5. **Expandable checklist steps** are the core UX pattern — each step collapses to show title/summary, expands to show all details.
6. **AI chat panel** floats as a button in bottom-right, opens a chat window on click. Sends to `/api/ask`.

---

## NPM Dependencies

```bash
npm install react-router-dom lucide-react framer-motion axios three @react-three/fiber @react-three/drei
npm install -D tailwindcss @tailwindcss/vite
```

---

## File Structure

```
frontend/
├── index.html
├── vite.config.js
├── package.json
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── index.css          (Tailwind + Compass theme + animations)
    ├── components/
    │   ├── Globe.jsx       (3D rotating globe for landing page)
    │   ├── Navbar.jsx      (Compass logo + nav)
    │   ├── ChatPanel.jsx   (Floating AI Q&A chat)
    │   └── StepCard.jsx    (Expandable checklist step component)
    └── pages/
        ├── Landing.jsx
        ├── Onboarding.jsx
        ├── Dashboard.jsx
        └── Journey.jsx
```
