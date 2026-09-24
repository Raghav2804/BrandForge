# 🚀 BrandForge

### Create. Validate. Launch.

BrandForge is an AI-powered multi-agent marketing agency that transforms a single campaign brief into a complete, validated and client-ready multi-channel marketing package.

---

## 🎯 Problem

Creating a complete marketing campaign manually requires separate work for:

- Marketing strategy
- Social media copy
- Email content
- Visual assets
- Brand consistency checking
- Campaign scheduling
- Final packaging

This process is time-consuming and can lead to inconsistent messaging across channels.

---

## 💡 Solution

BrandForge uses a multi-agent workflow to automate the campaign creation process.

A user provides one campaign brief containing:

- Product
- Target audience
- Campaign goal
- Key message
- Marketing channels

BrandForge then generates and validates the complete campaign.

---

## 🧠 Multi-Agent Architecture

```text
                    Campaign Brief
                          │
                          ▼
                  ┌───────────────┐
                  │ Strategy Agent│
                  └───────┬───────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Copywriting     │
                 │ Agent           │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Image Generation│
                 │ Agent           │
                 └────────┬────────┘
                          │
                          ▼
                ┌───────────────────┐
                │ Campaign War Room │
                │ / Brand Guardrail │
                └─────────┬─────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
             PASS                    FAIL
              │                       │
              ▼                       ▼
        Campaign Package        Revision Agent
                                      │
                                      ▼
                                   Recheck
                                      │
                                      ▼
                                  PASS / REVIEW
                                      │
                                      ▼
                              Final Campaign ZIP
                              