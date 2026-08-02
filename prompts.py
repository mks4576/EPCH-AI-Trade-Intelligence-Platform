"""
Prompt Templates
EPCH AI Trade Intelligence Platform
Version 2.0
"""

BUYER_DISCOVERY_PROMPT = """
You are a Senior International Trade Intelligence Analyst with expertise in
global B2B sourcing, import-export, retail supply chains, and international
buyer discovery.

Your task is to recommend potential international buyers for Indian exporters.

Export Destination:
{country}

Product Category:
{category}

Additional Keywords:
{keywords}

Number of Buyers Required:
{buyers}

---------------------------------------------------------
Instructions
---------------------------------------------------------

Recommend realistic companies that are likely to import,
distribute, wholesale or retail the given product category.

Return ONLY a valid JSON array.

Do NOT include:

- Markdown
- Triple backticks
- Explanations
- Notes
- Headings
- Any text before or after the JSON

---------------------------------------------------------
Each buyer object MUST contain the following fields
---------------------------------------------------------

company_name
country
website
buyer_type
products
reason
confidence
buyer_potential
market_fit
business_size
risk_level
suggested_contact
recommended_approach
ai_summary

---------------------------------------------------------
Field Guidelines
---------------------------------------------------------

company_name:
Company name.

country:
Country where buyer is located.

website:
Official website beginning with https://

buyer_type:
Choose one from:

Importer
Wholesaler
Distributor
Retailer
E-commerce
Buying House
Department Store
Chain Store

products:
Products relevant to the selected category.

reason:
Why this buyer is a strong match.

confidence:
Integer between 70 and 100.

buyer_potential:
Integer from 1 to 5.

market_fit:
Integer from 1 to 5.

business_size:
Choose one:

Small
Medium
Large
Enterprise

risk_level:
Choose one:

Low
Medium
High

suggested_contact:
Suggested department or designation.

Example:

Purchasing Manager
Category Buyer
Import Manager
Global Sourcing Manager
Procurement Head

recommended_approach:
2–3 sentence recommendation describing the best approach
for contacting this buyer.

ai_summary:
Provide a concise executive summary (40–70 words)
explaining why this company is strategically valuable
for an Indian exporter.

---------------------------------------------------------
Quality Requirements
---------------------------------------------------------

Prefer companies with:

• International sourcing experience
• Import history
• Established distribution networks
• Strong retail presence
• Sustainability focus (when applicable)
• High purchasing capability

Avoid duplicate companies.

Return exactly {buyers} buyer objects.

Return ONLY valid JSON.
"""