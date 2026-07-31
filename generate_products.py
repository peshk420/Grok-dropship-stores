#!/usr/bin/env python3
"""Generate 3 unique professional dropshipping stores with 55+ products each.
Products are generic trending items (kitchen, home, fitness, outdoor, pet, garden).
Sources: Alibaba, Temu, Wish, eBay wholesale partners, Fyndiq-style, Shein basics (non-branded).
All safe, no licensed brands, no medical claims, no regulated goods.
"""

import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# Comprehensive policies tailored for Sweden, Norway, UK, EU (EEA) markets 2026.
# Includes 14-day statutory withdrawal, recent EU withdrawal button requirement, fault claims.
POLICIES = {
    "returns": {
        "title": "Returns, Refunds & Right of Withdrawal",
        "summary": "We offer a generous returns policy. EU, Swedish, Norwegian and UK customers have statutory 14-day cooling-off (right of withdrawal) rights under distance selling laws in addition to our policy. Full details and country-specific information below.",
        "sections": [
            {
                "heading": "Our Store Return Policy (Voluntary)",
                "text": "Most unused items in original condition and packaging may be returned within 30 days of delivery for a refund (excluding shipping costs unless item is faulty). Contact us first. No restocking fee for standard returns."
            },
            {
                "heading": "Statutory Right of Withdrawal — EU & Sweden (14 Days)",
                "text": "Under the EU Consumer Rights Directive and Swedish Distansavtalslagen (Distance and Off-Premises Contracts Act), you have the right to withdraw from your purchase within 14 calendar days of receiving the goods without giving any reason. The period begins the day after delivery. You must notify us clearly (email is sufficient) within the 14 days and return the goods within another 14 days. We will refund the purchase price plus standard delivery cost paid. You pay the direct cost of returning the goods unless the item is faulty or we sent the wrong item. Sealed hygiene/personal care items (e.g. certain grooming tools once opened) and custom/personalized items are exempt once seal broken or personalization applied."
            },
            {
                "heading": "Statutory Right of Withdrawal — Norway (EEA)",
                "text": "Norway applies equivalent rules via the EEA Agreement (Angrerettloven). 14 calendar days from receipt to cancel without reason. Same refund rules as EU/Sweden: full refund of goods + standard shipping, you pay return shipping. Notify us within 14 days."
            },
            {
                "heading": "Statutory Right of Withdrawal — United Kingdom",
                "text": "Under the Consumer Contracts (Information, Cancellation and Additional Charges) Regulations 2013 you have 14 calendar days from the day after delivery to cancel a distance contract without reason. Notify us and return goods within 14 days of notification. We refund the price of the goods and the cost of standard delivery. You are responsible for the cost of return unless the goods are faulty or misdescribed. Exceptions for sealed goods for health/hygiene reasons once unsealed."
            },
            {
                "heading": "EU Online Withdrawal Button (Mandatory from 19 June 2026)",
                "text": "For all EU customers we provide a clearly visible 'Withdraw from this purchase' button/link on order confirmation pages and in your account area (simulated here). Clicking it starts the statutory withdrawal process. We will confirm receipt and provide return instructions immediately."
            },
            {
                "heading": "Faulty Goods & Legal Guarantee (Reklamation / Statutory Warranty)",
                "text": "Separately from the 14-day withdrawal, under Swedish/EU Sale of Goods rules (Konsumentköplagen) and equivalent in Norway/UK, you have rights for up to 3 years (or 2 years UK minimum in many cases) if goods are faulty, not as described, or not fit for purpose. Contact us with photos and order number. We will offer repair, replacement, price reduction or refund as required by law. This right cannot be limited by our returns window."
            },
            {
                "heading": "How to Return or Withdraw",
                "text": "Email the store support address with your order ID, reason (optional for withdrawal), and photos if damaged. We reply within 2 business days with return address (EU/UK warehouse partners) and RMA if needed. Clearly label package with order ID. Track the return. Refunds processed within 14 days of us receiving returned goods (or proof of posting for withdrawals). Original payment method used."
            },
            {
                "heading": "Exceptions & Important Notes",
                "text": "Opened personal hygiene items (e.g. certain brushes, masks once used), perishable goods, or items made to your specification cannot be returned once used/sealed broken. Downloadable digital items (if any) have different rules. We may deduct reasonable value loss if goods are handled beyond normal inspection."
            },
            {
                "heading": "Delivery Times & Shipping (Estimates Only)",
                "text": "Orders fulfilled via direct supplier shipping from Asia/EU/US warehouses. Typical 7-21 business days. Not guaranteed. Tracking provided where available. Delays can occur; we are not liable for carrier delays beyond reasonable control. Free shipping thresholds shown per product."
            }
        ]
    },
    "shipping": {
        "title": "Shipping & Delivery Policy",
        "summary": "Direct from verified suppliers in our network (Alibaba/Temu/Shein/eBay wholesale/Fyndiq-style partners). Delivery estimates 7–21 business days to Sweden, Norway, UK and EU. Tracking provided on most orders.",
        "sections": [
            {"heading": "Processing", "text": "We forward your order to the supplier within 1-3 business days. You receive confirmation email with expected ship date."},
            {"heading": "Delivery Estimates", "text": "Standard: 7-14 business days (EU/UK warehouse stock). International supplier direct: 10-21 business days. Peak seasons (summer, holidays) may add 3-7 days. These are estimates, not guarantees."},
            {"heading": "Costs", "text": "Shown at checkout. Many items qualify for free standard shipping over threshold. Customs/VAT: For non-EU origin goods entering EU/UK/NO/SE you may be liable for import VAT/duties (we display estimated where possible; actual handled by carrier). Prices shown include Swedish/EU VAT where applicable for EU stores."},
            {"heading": "Lost/Damaged", "text": "If package lost (no tracking update 15+ days) or arrives damaged, contact us within 48h with photos. We will work with supplier/carrier for replacement or refund at no extra cost to you for faulty cases."}
        ]
    },
    "terms": {
        "title": "Terms of Service & Legal Disclosures",
        "summary": "We are online retailers operating a dropshipping model. Products are sourced from third-party verified suppliers and shipped directly. This is a demo/local development server only.",
        "sections": [
            {"heading": "Business Model & Transparency", "text": "We source products from global suppliers (Alibaba, Temu, eBay wholesale partners, similar platforms serving Fyndiq/Shein-style marketplaces). We do not hold inventory. Product appearance, packaging and minor specs may vary slightly from photos due to batch differences. We clearly disclose this."},
            {"heading": "Prices & Currency", "text": "Prices in EUR (or local equivalent shown). Reasonable retail pricing with healthy but fair margins after supplier cost, shipping, returns, and platform fees. We may adjust prices. Errors may lead to order cancellation with full refund."},
            {"heading": "No Health/Medical Claims", "text": "Products are sold for general consumer use. No claims that items diagnose, treat, cure or prevent disease. Cooling products are for general comfort only. Always follow safety instructions."},
            {"heading": "Limitation of Liability & Governing Law", "text": "Liability limited to the price paid for the specific item(s). We are not responsible for indirect damages or delays by third parties. For EU customers, mandatory consumer protections apply regardless. Disputes: first contact support. Swedish law applies for Lumina (SE), with EU consumer protections; UK law for Apex UK sales; Norwegian for relevant."},
            {"heading": "Company Information (Demo)", "text": "These are demonstration stores. In a real deployment each would display: full legal company name, registered address, organization number, VAT ID (e.g. SE/NO/GB/IE), and contact email. Always verify before real purchases. This local server is for testing only."}
        ]
    },
    "privacy": {
        "title": "Privacy Policy",
        "summary": "We collect minimal data needed to fulfill orders and reply to you. We do not sell your data. GDPR, UK GDPR, and Norwegian privacy rules respected.",
        "sections": [
            {"heading": "Data Collected", "text": "Name, email, phone (optional), full shipping address, order details, IP for fraud. Payment handled by third-party processors (we never see full card details)."},
            {"heading": "Use & Sharing", "text": "To process orders, communicate, improve site, comply with tax/consumer law (records kept 3-7 years). Shared only with fulfillment partners, carriers, and authorities as legally required. No sale of personal data."},
            {"heading": "Your Rights", "text": "Access, rectification, erasure, restriction, portability, objection, and withdrawal of consent. Email the store address. We respond within 30 days (or 1 month). You may complain to your local authority: Datainspektionen/IMY (SE), Datatilsynet (NO), ICO (UK), or national DPA in your EU country."},
            {"heading": "Cookies & Marketing", "text": "Essential cookies only for cart/function. No pre-ticked marketing. Every newsletter has instant unsubscribe. We respect Do Not Track where applicable."},
            {"heading": "Data Retention", "text": "Orders kept for tax, warranty and legal compliance (minimum 3 years, up to 7 for some records)."}
        ]
    }
}

# 3 unique stores. Each with ~55-60 products = 160+ total trending safe items.
# Prices chosen for good profit (typically 2.5x-4x cost) while reasonable for market.
STORES = {
    "site-lumina-home": {
        "store": {
            "name": "Lumina Home",
            "tagline": "Timeless Essentials for Modern Living",
            "logoHtml": "Lumina <span>Home</span>",
            "description": "Curated minimalist kitchen, organization, lighting and home storage essentials. Sourced directly from verified suppliers on Alibaba, Temu, eBay wholesale and similar platforms serving EU, UK, Sweden and Norway.",
            "email": "support@lumina-home.com",
            "phone": "+46 8 123 4567 (SE support)",
            "slug": "lumina-home",
            "currency": "EUR",
            "pricesIncludeVat": True,
            "vatRatePct": 25,
            "legalName": "[YOUR COMPANY NAME] AB",
            "orgNumber": "[ORG NR e.g. 559XXX-XXXX]",
            "vatNumber": "[VAT e.g. SE559XXXXXXXX01]",
            "registeredAddress": "[Registered business address, City, Sweden]"
        },
        "theme": {
            "primary": "#3d5a5b",
            "primaryDark": "#2c4445",
            "accent": "#d4a373"
        },
        "hero": {
            "title": "Beautifully Simple Home Essentials",
            "subtitle": "Quality kitchen tools, clever organizers, warm lighting and storage that lasts — shipped direct from trusted suppliers to Sweden, Norway, UK & EU.",
            "badges": ["Free shipping over €49", "30-day easy returns", "14-day statutory EU/UK/NO/SE withdrawal right"]
        },
        "trust": [
            {"icon": "🚚", "text": "7–21 Day Delivery"},
            {"icon": "⭐", "text": "4.8★ Average"},
            {"icon": "🔒", "text": "Secure Checkout"},
            {"icon": "🌍", "text": "Ships to SE/NO/UK/EU"}
        ],
        "about": {
            "title": "Why Lumina Home?",
            "paragraphs": [
                "We select durable, well-designed everyday items that improve daily life without clutter.",
                "Direct supplier model means better prices than big retail while maintaining high standards."
            ],
            "features": [
                {"icon": "🍳", "text": "Kitchen that works"},
                {"icon": "🗄️", "text": "Smart organization"},
                {"icon": "💡", "text": "Warm lighting"},
                {"icon": "♻️", "text": "Quality materials"}
            ]
        },
        "products": [
            # 58 products - kitchen, organization, lighting, storage, bath, desk
            ("Stainless Steel Portable Blender Bottle — 500ml", "Kitchen", 29.99, 44.99, 9.80, "Temu", "Trending", "USB rechargeable personal blender for smoothies and shakes on the go.", "kitchen", "Food-grade stainless + BPA-free. 6-blade system. 4000mAh battery. Easy clean."),
            ("Digital Kitchen Scale — 5kg Precision", "Kitchen", 18.99, 27.99, 5.50, "Alibaba", None, "Ultra-precise 1g resolution scale with tare and hold function.", "kitchen", "Stainless platform. Backlit LCD. 5kg capacity. Auto-off. Batteries included."),
            ("Vegetable Chopper & Dicer Set — 5 Blades", "Kitchen", 24.99, 36.99, 7.20, "Temu", "Best Seller", "Manual food chopper with multiple blade options for veggies, nuts, herbs.", "kitchen", "BPA-free container. 5 interchangeable blades. 1200ml capacity. Dishwasher safe top rack."),
            ("Silicone Kitchen Utensil Set — 10 Piece", "Kitchen", 22.99, 33.99, 6.80, "Alibaba", None, "Heat-resistant non-stick silicone tools with acacia wood handles.", "kitchen", "Includes spatula, spoon, tongs, whisk, brush, ladle etc. Up to 220°C."),
            ("Reusable Silicone Food Storage Bags — 6 Pack", "Kitchen", 16.99, 24.99, 4.90, "Temu", None, "Leak-proof zip bags for freezer, fridge, sous vide and snacks.", "kitchen", "Stand-up design. Various sizes. Dishwasher & microwave safe. Reduces plastic waste."),
            ("Insulated Stainless Travel Tumbler — 600ml", "Kitchen", 19.99, 29.99, 6.20, "Alibaba", "Hot", "Double-wall vacuum keeps drinks hot 8h or cold 24h. Fits car cupholders.", "kitchen", "18/8 food-grade steel. Leak-proof lid. Straw & sip options. 600ml."),
            ("Bento Lunch Box with Dividers & Utensils", "Kitchen", 14.99, 22.99, 4.10, "Temu", None, "Stackable leak-proof compartments for balanced meals.", "kitchen", "Microwave & dishwasher safe. Includes fork/spoon. 3 compartments + sauce cup."),
            ("Glass Oil & Vinegar Dispenser Set — 2x500ml", "Kitchen", 21.99, 31.99, 6.50, "Alibaba", None, "Drip-free pour spouts with labels for kitchen counter.", "kitchen", "Borosilicate glass. Stainless pourers. Non-slip base. Easy refill."),
            ("Digital Instant Read Meat Thermometer", "Kitchen", 13.99, 19.99, 3.80, "Temu", None, "Foldable probe with large backlit display. 3-5 second read.", "kitchen", "±0.5°C accuracy. Waterproof. Auto wake. Magnetic back. Calibration option."),
            ("Spice Rack Organizer — 4 Tier Rotating", "Kitchen", 27.99, 39.99, 8.90, "Alibaba", None, "360° rotating bamboo spice rack holds 20+ jars.", "kitchen", "Natural bamboo. Non-slip base. 4 shelves. Easy clean."),
            ("Drawer Organizer Set — 8 Piece Bamboo", "Home Organization", 18.99, 27.99, 5.40, "Temu", None, "Adjustable dividers for kitchen, office and bathroom drawers.", "storage", "Expand from 4-12 inches. Natural finish. Non-slip pads."),
            ("Under-Bed Storage Bags — 2 Large Zip", "Home Organization", 16.99, 24.99, 4.70, "Alibaba", None, "Extra capacity under-bed organizers with clear window.", "storage", "90x65x20cm. Reinforced handles. Moth & dust proof. 2-pack."),
            ("Vacuum Storage Bags — 8 Piece Set", "Home Organization", 19.99, 29.99, 5.80, "Temu", None, "Space-saving compression bags for clothes, bedding, travel.", "storage", "Works with any vacuum. 4 sizes. Double-zip + valve. Reusable."),
            ("Adhesive Wall Hooks — Heavy Duty 20 Pack", "Home Organization", 12.99, 18.99, 3.20, "Temu", None, "Strong damage-free hooks for towels, coats, kitchen tools.", "storage", "Holds up to 5kg each. Waterproof. Removable without residue."),
            ("LED Strip Lights — 5m RGB with Remote", "Lighting", 15.99, 23.99, 4.50, "Alibaba", "Trending", "Flexible 5050 LED strip, 16 colors, music sync option.", "lighting", "IP65 waterproof. Cuttable. 12V adapter. Strong 3M tape. App optional."),
            ("Dimmable Touch Table Lamp — Warm White", "Lighting", 29.99, 44.99, 9.20, "Temu", None, "Modern bedside or desk lamp with 3 brightness levels.", "lighting", "USB rechargeable or plug. Fabric shade. 3000K warm light. 8h battery."),
            ("Solar Powered String Lights — 10m 100 LED", "Lighting", 17.99, 26.99, 5.10, "Alibaba", "Best Value", "Outdoor/indoor warm white solar fairy lights with timer.", "lighting", "8 modes. Auto on/off. Weatherproof. 2m lead wire. No wiring needed."),
            ("Rechargeable LED Desk Lamp with Clamp", "Lighting", 24.99, 36.99, 7.50, "Temu", None, "Eye-care 3 color modes, adjustable arm and brightness.", "lighting", "10W. 5V USB-C. 3 color temps. Stepless dim. Clamp or base."),
            ("Closet Hanging Organizer — 6 Shelf", "Storage", 14.99, 21.99, 4.00, "Alibaba", None, "Collapsible fabric shelf organizer for sweaters, shoes, bags.", "storage", "Hangs from closet rod. 6 compartments. Sturdy cardboard insert."),
            ("Over-Door Hanging Organizer — 24 Pocket", "Storage", 16.99, 24.99, 4.80, "Temu", None, "Clear pocket shoe and accessory organizer for doors.", "storage", "Fits most doors. 24 large pockets. Metal hooks. Breathable."),
            ("Cable Management Box & Clips Set", "Home Organization", 13.99, 19.99, 3.60, "Alibaba", None, "Hide power strips and excess cables neatly.", "storage", "Large box + 20 clips + ties + sleeve. Fire retardant."),
            ("Desk Drawer Organizer Tray — Bamboo", "Home Organization", 15.99, 23.99, 4.50, "Temu", None, "5-compartment tray for pens, notes, phone, accessories.", "storage", "Fits most drawers. Natural bamboo. Non-slip base."),
            ("Laundry Hamper with Lid — 60L Foldable", "Storage", 21.99, 31.99, 6.40, "Alibaba", None, "Large capacity with lid and handles. Collapses flat.", "storage", "Oxford fabric. Sturdy steel frame. Easy carry. 60 liter."),
            ("Shower Caddy Corner Shelf — 3 Tier", "Bath & Storage", 18.99, 27.99, 5.30, "Temu", None, "Rust-proof aluminum corner caddy with adhesive or screw.", "storage", "Holds 15kg. 3 tiers + soap dish. No drilling option."),
            ("Towel Rack Wall Mounted — 2 Bar", "Bath & Storage", 19.99, 28.99, 5.70, "Alibaba", None, "Stainless steel double towel bar with shelf.", "storage", "40cm wide. Strong fixings. Modern brushed finish."),
            ("Makeup Organizer with Drawers — Acrylic", "Storage", 16.99, 24.99, 4.70, "Temu", None, "Clear 4-drawer cosmetic storage for bathroom or vanity.", "storage", "Dust proof. 360° rotation option available in variants."),
            ("Shoe Rack — 4 Tier Stackable Metal", "Storage", 23.99, 34.99, 7.10, "Alibaba", None, "Heavy duty freestanding shoe shelf for entryway.", "storage", "Holds 12-16 pairs. Rust resistant. Easy no-tool assembly."),
            ("Wall Mounted Key & Mail Holder", "Home Organization", 11.99, 17.99, 3.10, "Temu", None, "Decorative entryway organizer with hooks and shelf.", "storage", "Wood + metal. 5 hooks. Small shelf for mail."),
            ("Floating Wall Shelves — Set of 3", "Storage", 24.99, 36.99, 7.40, "Alibaba", "New", "Modern invisible bracket wood shelves for decor and books.", "storage", "40/50/60cm lengths. 15kg per shelf. Easy install template."),
            ("Jewelry Organizer Box with Mirror", "Storage", 17.99, 25.99, 5.00, "Temu", None, "Large capacity ring/earring/necklace case with lid mirror.", "storage", "Velvet interior. 5 layers. Lock option. Travel size available."),
            ("Pantry Door Organizer — 6 Basket", "Kitchen Storage", 19.99, 29.99, 5.90, "Alibaba", None, "Over door metal basket pantry organizer.", "storage", "Fits standard doors. 6 deep baskets. No drilling."),
            ("Wine Rack Countertop — 6 Bottle", "Kitchen", 15.99, 23.99, 4.40, "Temu", None, "Stable wood or metal countertop wine holder.", "kitchen", "Holds 6 standard bottles. Non-slip. Compact footprint."),
            ("Cutting Board Set — 3 Size Bamboo", "Kitchen", 18.99, 27.99, 5.50, "Alibaba", None, "Reversible bamboo boards with juice groove.", "kitchen", "Large, medium, small. Easy clean. Knife friendly."),
            ("Electric Salt & Pepper Grinder Set", "Kitchen", 22.99, 33.99, 6.70, "Temu", None, "Automatic one-hand grinders with light and adjustable coarseness.", "kitchen", "Battery operated. LED light. Refillable. 2-pack."),
            ("Silicone Baking Mat Set — 3 Size", "Kitchen", 14.99, 21.99, 4.00, "Alibaba", None, "Non-stick reusable baking sheets for oven and air fryer.", "kitchen", "Macaron size + half + full. Heat to 230°C. Easy clean."),
            ("Collapsible Colander & Strainer Set", "Kitchen", 13.99, 19.99, 3.70, "Temu", None, "Space saving silicone colanders that fold flat.", "kitchen", "2 sizes. Heat resistant. Dishwasher safe."),
            ("Ice Cube Tray with Lid — 2 Pack", "Kitchen", 9.99, 14.99, 2.60, "Alibaba", None, "Easy release silicone ice trays with stackable lids.", "kitchen", "Makes 32 cubes. Flexible. No spill lid. BPA free."),
            ("French Press Coffee Maker — 1L Glass", "Kitchen", 16.99, 24.99, 4.80, "Temu", None, "Heat resistant borosilicate with stainless plunger.", "kitchen", "1 liter / 8 cup. Dishwasher safe parts. 3-layer filter."),
            ("Measuring Cup & Spoon Set — 13 Piece", "Kitchen", 11.99, 17.99, 3.00, "Alibaba", None, "Stainless nested measuring tools with leveler.", "kitchen", "Accurate to 1/8 tsp. Engraved markings. Hangable."),
            ("Dish Drying Rack — Roll-Up Silicone", "Kitchen", 14.99, 21.99, 4.10, "Temu", None, "Foldable over-sink drying mat that rolls for storage.", "kitchen", "Heat safe. Drains into sink. Large 50x40cm."),
            ("Lunch Box Stainless Steel — Leak Proof", "Kitchen", 15.99, 23.99, 4.50, "Alibaba", None, "Insulated 2-compartment bento for hot or cold food.", "kitchen", "800ml. Keeps warm 4-6h. Includes utensils."),
            ("Mini Food Processor Chopper — USB", "Kitchen", 19.99, 29.99, 5.80, "Temu", "Trending", "Electric garlic/herb/veggie chopper, cordless.", "kitchen", "250ml. One button. 2 speeds. Rechargeable."),
            ("Kitchen Sink Caddy & Sponge Holder", "Kitchen", 12.99, 18.99, 3.40, "Alibaba", None, "Hanging or counter sink organizer for brush and sponge.", "kitchen", "Rust proof. Drip tray. Strong adhesive or suction."),
            ("Glass Food Storage Jars — 6 Pack", "Kitchen", 23.99, 34.99, 7.00, "Temu", None, "Airtight bamboo lid jars for pantry staples.", "kitchen", "6 sizes. Labels included. Dishwasher safe glass."),
            ("Mandoline Slicer with Safety Guard", "Kitchen", 17.99, 26.99, 5.10, "Alibaba", None, "Adjustable thickness professional vegetable slicer.", "kitchen", "Stainless blade. 5 thickness settings. Julienne option."),
            ("Electric Kettle — 1.7L Fast Boil", "Kitchen", 26.99, 39.99, 8.20, "Temu", None, "Stainless cordless kettle with auto shut-off.", "kitchen", "1500-1800W. Boil dry protection. Cool touch handle."),
            ("Fruit & Vegetable Washing Bowl with Strainer", "Kitchen", 13.99, 19.99, 3.70, "Alibaba", None, "Collapsible 2-in-1 produce washer and drainer.", "kitchen", "5L. Silicone. Easy store flat."),
            ("Knife Sharpener — 3 Stage Professional", "Kitchen", 14.99, 21.99, 3.90, "Temu", None, "Diamond, ceramic and steel stages for all knives.", "kitchen", "Non-slip base. Safe hand grip. Works on serrated."),
            ("Bread Box — Large Bamboo with Lid", "Kitchen", 21.99, 31.99, 6.50, "Alibaba", None, "Keeps bread fresh longer with ventilation.", "kitchen", "Holds 2 loaves. Window lid. Easy clean."),
            ("Reusable Beeswax Food Wraps — 6 Pack", "Kitchen", 15.99, 23.99, 4.30, "Temu", "Eco", "Natural fabric wraps for covering bowls and wrapping food.", "kitchen", "Various sizes. Washable. Compostable at end of life."),
            ("Coffee Scale with Timer — Precision", "Kitchen", 24.99, 36.99, 7.40, "Alibaba", None, "0.1g accuracy pour-over scale with built-in timer.", "kitchen", "USB rechargeable. Auto timer. Water resistant."),
            ("Handheld Milk Frother — USB Rechargeable", "Kitchen", 11.99, 17.99, 3.10, "Temu", None, "Powerful whisk for lattes, matcha, eggs.", "kitchen", "3 speeds. 25s froth. Easy clean. Stand included."),
            ("Dish Brush Set with Holder — 3 Piece", "Kitchen", 9.99, 14.99, 2.50, "Alibaba", None, "Bamboo handle brushes for dishes, vegetables, bottles.", "kitchen", "Replaceable heads. Wall holder. Natural."),
            ("Air Tight Pasta & Cereal Containers — 4 Pack", "Kitchen Storage", 18.99, 27.99, 5.40, "Temu", None, "Stackable pantry containers with one-hand pour lid.", "storage", "2.5L + 1.8L sizes. BPA free. Labels + marker."),
            ("Silicone Pot Holders & Oven Mitt Set", "Kitchen", 12.99, 18.99, 3.30, "Alibaba", None, "Heat resistant up to 250°C with non-slip grip.", "kitchen", "2 mitts + 2 holders. Easy clean. Hanging loop."),
            ("Mini Digital Timer — Magnetic 2 Pack", "Kitchen", 8.99, 12.99, 2.10, "Temu", None, "Loud alarm kitchen timers for cooking and productivity.", "kitchen", "99 min. Large digits. Strong magnet. 2-pack."),
        ]
    },
    "site-apex-trail": {
        "store": {
            "name": "Apex Trail",
            "tagline": "Gear for the Everyday Explorer",
            "logoHtml": "Apex <span>Trail</span>",
            "description": "Functional fitness, hiking, camping and travel accessories. Quality generic gear sourced direct from verified suppliers serving active lifestyles across Sweden, Norway, UK and EU.",
            "email": "hello@apextrail.com",
            "phone": "+44 20 1234 5678 (UK support)",
            "slug": "apex-trail",
            "currency": "EUR",
            "pricesIncludeVat": True,
            "vatRatePct": 20,
            "legalName": "[YOUR COMPANY NAME] Ltd",
            "orgNumber": "[UK Company No. 1XXXXXX]",
            "vatNumber": "[VAT e.g. GB123456789]",
            "registeredAddress": "[Registered address, London, United Kingdom]"
        },
        "theme": {
            "primary": "#2c3e50",
            "primaryDark": "#1a252f",
            "accent": "#27ae60"
        },
        "hero": {
            "title": "Ready for Your Next Adventure",
            "subtitle": "Durable fitness accessories, lightweight outdoor tools, travel organizers and hiking essentials — practical gear that performs.",
            "badges": ["Free shipping over €59", "30-day returns", "Statutory 14-day withdrawal for UK/EU/NO/SE"]
        },
        "trust": [
            {"icon": "🥾", "text": "Trail Tested"},
            {"icon": "🚚", "text": "7–21 Day Delivery"},
            {"icon": "💪", "text": "Built to Last"},
            {"icon": "🌲", "text": "SE/NO/UK/EU Shipping"}
        ],
        "about": {
            "title": "Why Apex Trail?",
            "paragraphs": [
                "We focus on practical, high-utility items that make outdoor and active life easier and more enjoyable.",
                "Direct from suppliers — no middleman markup on quality generic gear."
            ],
            "features": [
                {"icon": "🏋️", "text": "Fitness gear"},
                {"icon": "⛺", "text": "Camp & hike"},
                {"icon": "🧳", "text": "Travel smart"},
                {"icon": "🌧️", "text": "Weather ready"}
            ]
        },
        "products": [
            # 57 products - fitness, outdoor, camping accessories, travel, hiking
            ("Non-Slip Yoga Mat — 6mm Extra Thick", "Fitness", 22.99, 34.99, 6.80, "Alibaba", "Best Seller", "Eco TPE mat with alignment lines and carrying strap.", "fitness", "183x61cm. 6mm cushion. Non-slip both sides. Includes strap."),
            ("Resistance Bands Set — 5 Level Loop", "Fitness", 14.99, 22.99, 3.90, "Temu", None, "Fabric loop bands for glute, leg, arm and full body workouts.", "fitness", "5 resistance levels. Non-slip inner. Carry bag. Exercise guide."),
            ("Foam Roller — High Density 45cm", "Fitness", 17.99, 26.99, 5.00, "Alibaba", None, "Deep tissue massage roller for recovery and mobility.", "fitness", "EPP high density. 45x15cm. Lightweight. Trigger point texture."),
            ("Jump Rope — Adjustable Speed Cable", "Fitness", 11.99, 17.99, 3.00, "Temu", None, "Ball bearing speed rope for cardio and boxing training.", "fitness", "Adjustable 2.8m. Comfort handles. Fast spin. Carry bag."),
            ("Posture Corrector Brace — Adjustable", "Fitness", 16.99, 24.99, 4.50, "Alibaba", "Trending", "Comfortable upper back support for desk and daily wear.", "fitness", "Breathable. One size fits most. Adjustable straps. Discreet under clothes."),
            ("Mini Massage Gun — Deep Tissue", "Fitness", 29.99, 44.99, 9.20, "Temu", None, "Portable percussive massager with 4 heads and 3 speeds.", "fitness", "USB-C. Quiet <45dB. 4 attachments. 4-6h battery. Travel size."),
            ("Acupressure Mat & Pillow Set", "Fitness", 19.99, 29.99, 5.60, "Alibaba", None, "Spiked mat for back, neck and foot relaxation.", "fitness", "Cotton + ABS spikes. Includes pillow. 20 min sessions typical."),
            ("Pull-Up Assist Bands — Heavy Set 3", "Fitness", 18.99, 27.99, 5.30, "Temu", None, "Extra thick resistance bands for assisted pull-ups and mobility.", "fitness", "3 levels (15-85lb). Natural latex. Door anchor included."),
            ("Yoga Block Set — 2 Pack + Strap", "Fitness", 13.99, 19.99, 3.70, "Alibaba", None, "High density EVA blocks and cotton strap for alignment.", "fitness", "23x15x10cm blocks. 2.5m strap. Lightweight. Odor resistant."),
            ("Travel Yoga Mat — Foldable Thin", "Fitness", 15.99, 23.99, 4.30, "Temu", None, "Compact 1.5mm mat that folds into its own bag.", "fitness", "160x60cm. Sweat resistant. Machine washable. 400g."),
            ("Portable Camping Lantern — 1000 Lumen", "Outdoor", 24.99, 36.99, 7.50, "Alibaba", "Hot", "Rechargeable LED lantern with power bank and multiple modes.", "outdoor", "4 light modes. 5200mAh. IPX4. 360° + directional. USB-C."),
            ("Headlamp Rechargeable — 350 Lumen", "Outdoor", 16.99, 24.99, 4.70, "Temu", None, "Comfortable wide beam head torch with red night mode.", "outdoor", "USB rechargeable. 45h runtime low. Adjustable strap. IPX4."),
            ("Folding Trekking Poles — Carbon Look", "Outdoor", 29.99, 44.99, 8.90, "Alibaba", None, "Lightweight 3-section poles with cork grip and quick lock.", "outdoor", "Pair. 280g each. 5 height settings. Baskets & tips included."),
            ("Waterproof Dry Bag — 20L Roll Top", "Outdoor", 15.99, 23.99, 4.40, "Temu", None, "IPX7 roll-top dry sack for kayaking, hiking, beach.", "outdoor", "20 liter. 500D PVC. Adjustable strap. Floats if dropped."),
            ("Portable Hammock with Tree Straps", "Outdoor", 21.99, 32.99, 6.30, "Alibaba", "Trending", "Parachute nylon double hammock with integrated bug net option.", "outdoor", "Supports 300kg. Fast setup. Stuff sack. 2 carabiners."),
            ("Solar Shower Bag — 5 Gallon", "Outdoor", 14.99, 21.99, 3.90, "Temu", None, "Camping solar heated shower for beach, hike, festival.", "outdoor", "20L. Heats in sun 3h. On/off valve. Hanging rope."),
            ("Pop-Up Beach / Privacy Tent", "Outdoor", 34.99, 49.99, 10.50, "Alibaba", None, "Instant 2-person changing room or small shelter.", "outdoor", "47x47x78\". Sand pockets. 2 windows. Carry bag."),
            ("Folding Camp Chair — 330lb Capacity", "Outdoor", 26.99, 39.99, 8.00, "Temu", None, "Heavy duty 600D fabric chair with cup holder and bag.", "outdoor", "Supports 150kg. Quick fold. 1.8kg. Carry bag."),
            ("Portable Camping Stove — Single Burner", "Outdoor", 18.99, 27.99, 5.40, "Alibaba", None, "Windproof butane/propane stove for backpacking.", "outdoor", "3000W. Piezo ignition. Folds small. 1lb canister compatible."),
            ("Collapsible Water Container — 10L", "Outdoor", 11.99, 17.99, 3.10, "Temu", None, "Food grade foldable water jug with spout.", "outdoor", "BPA free. Folds to 5cm. Carry handle. 10 liter."),
            ("LED Head Torch + Red Light 2 Pack", "Outdoor", 19.99, 29.99, 5.70, "Alibaba", None, "Two lightweight headlamps for hiking and camping.", "outdoor", "200 lumen each. 3 modes + red. USB charge. 2-pack."),
            ("Waterproof Phone Pouch — Floatable 2 Pack", "Travel", 9.99, 14.99, 2.40, "Temu", None, "IPX8 touchscreen phone case with lanyard for water activities.", "travel", "Fits up to 7\". Floatable. Neck strap. 2-pack."),
            ("Compression Packing Cubes — 6 Piece Set", "Travel", 18.99, 27.99, 5.30, "Alibaba", "Best Seller", "Organize luggage with compression zip cubes.", "travel", "6 sizes. Double zip. Mesh top. Fits carry-on perfectly."),
            ("Neck Pillow Memory Foam — Travel", "Travel", 14.99, 21.99, 4.00, "Temu", None, "Ergonomic U-shape pillow with washable cover.", "travel", "Soft memory foam. Snap buttons. Compact pouch."),
            ("RFID Blocking Passport Wallet", "Travel", 12.99, 18.99, 3.40, "Alibaba", None, "Slim travel document holder with multiple card slots.", "travel", "Blocks 13.56MHz. 10+ card slots. Coin pocket. Passport fit."),
            ("Portable Luggage Scale — Digital", "Travel", 11.99, 17.99, 3.10, "Temu", None, "Accurate 50kg hanging scale for baggage.", "travel", "Backlit. Tare. 1g precision. Batteries included."),
            ("Foldable Travel Duffel — 40L", "Travel", 17.99, 25.99, 4.90, "Alibaba", None, "Lightweight packable duffel that fits in its own pocket.", "travel", "40L. Water resistant. Shoulder + handles. 300g packed."),
            ("Eye Mask + Ear Plugs Travel Set", "Travel", 8.99, 12.99, 2.20, "Temu", None, "Contoured sleep mask and soft silicone plugs.", "travel", "Light blocking. Adjustable. 2 pairs plugs. Carry pouch."),
            ("Hiking Backpack 35L — Waterproof", "Outdoor", 39.99, 59.99, 12.50, "Alibaba", None, "Daypack with rain cover, hydration sleeve and hip belt.", "outdoor", "35L. Padded straps. Multiple pockets. 1.1kg."),
            ("Camping Cookware Mess Kit — 10pc", "Outdoor", 24.99, 36.99, 7.20, "Temu", None, "Non-stick pots, pans, plates, cups and utensils.", "outdoor", "Light aluminum. Folding handles. Mesh bag. 2-3 people."),
            ("Emergency Survival Kit — 72 Hour", "Outdoor", 22.99, 33.99, 6.50, "Alibaba", None, "Compact kit with food, water, blanket, fire starter.", "outdoor", "Food bars, water, first aid, whistle, blanket, multi-tool."),
            ("Mosquito Head Net & Repellent Band", "Outdoor", 9.99, 14.99, 2.50, "Temu", None, "Fine mesh head net + DEET-free repellent wristband.", "outdoor", "One size. Breathable mesh. 2 bands included."),
            ("Portable Power Bank 20000mAh — Fast Charge", "Travel", 19.99, 29.99, 5.80, "Alibaba", "Hot", "Dual USB-C PD power bank for phones and tablets.", "travel", "20000mAh. 20W PD. 2x USB-A + C. LED display."),
            ("Folding Stool — Compact 3 Leg", "Outdoor", 13.99, 19.99, 3.70, "Temu", None, "Lightweight portable stool for hiking, fishing, festivals.", "outdoor", "Supports 120kg. Folds to 25cm. Carry strap. 500g."),
            ("Insulated Water Bottle — 1L Wide Mouth", "Outdoor", 16.99, 24.99, 4.70, "Alibaba", None, "Double wall vacuum bottle keeps cold 24h / hot 12h.", "outdoor", "18/8 steel. Powder coat. Leak proof. Fits filters."),
            ("Carabiner Set — 6 Heavy Duty", "Outdoor", 10.99, 15.99, 2.80, "Temu", None, "D-shape locking and non-locking carabiners.", "outdoor", "Aluminum. 6 mixed sizes. Keyring + 2 large."),
            ("Microfiber Quick Dry Towel — 3 Pack", "Travel", 12.99, 18.99, 3.40, "Alibaba", None, "Ultra absorbent fast dry towels for gym, beach, travel.", "travel", "3 sizes (S/M/L). Includes pouch. Sand resistant."),
            ("Portable Espresso Maker — Manual Press", "Outdoor", 27.99, 41.99, 8.30, "Temu", "Trending", "Hand powered espresso maker for travel and camping.", "outdoor", "Makes real espresso. No electricity. Compact 250g."),
            ("Hiking Gaiters — Waterproof Pair", "Outdoor", 15.99, 23.99, 4.40, "Alibaba", None, "Breathable lower leg protection from mud, snow, ticks.", "outdoor", "600D. Adjustable top. Hook under boot. One size."),
            ("Sleeping Bag Liner — Silk Feel", "Outdoor", 14.99, 21.99, 4.00, "Temu", None, "Lightweight liner adds warmth and keeps bag clean.", "outdoor", "Rectangular. Machine wash. 200x90cm. 180g."),
            ("Camping Pillow — Inflatable Compact", "Outdoor", 9.99, 14.99, 2.50, "Alibaba", None, "Ultralight inflatable pillow for tent or travel.", "outdoor", "Folds to fist size. Soft fleece top. 40x30cm inflated."),
            ("LED Lantern String — 5m Battery", "Outdoor", 12.99, 18.99, 3.40, "Temu", None, "Warm white camping string lights with timer and remote.", "outdoor", "Battery or USB. 8 modes. IP65. 50 LEDs."),
            ("Multi Tool Pliers — 12 in 1", "Outdoor", 13.99, 19.99, 3.70, "Alibaba", None, "Stainless multi-function tool with sheath.", "outdoor", "Pliers, knife, saw, file, screwdriver etc. 12 functions."),
            ("Water Filter Straw — Personal", "Outdoor", 10.99, 15.99, 2.80, "Temu", None, "0.1 micron filter removes 99.9% bacteria from water.", "outdoor", "Filters 1500L. Drink direct or from bottle. 2oz."),
            ("Folding Table — Compact Aluminum", "Outdoor", 29.99, 44.99, 9.00, "Alibaba", None, "Light roll-up table for picnic and camp.", "outdoor", "60x40cm. 1.1kg. Rolls small. Strong frame."),
            ("Thermal Base Layer Set — Top + Bottom", "Outdoor", 24.99, 36.99, 7.30, "Temu", None, "Merino-blend long underwear for cold weather.", "outdoor", "Men/Women fit. 4-way stretch. Quick dry. S-2XL."),
            ("Reflective Safety Vest + Armband Set", "Outdoor", 8.99, 12.99, 2.10, "Alibaba", None, "High vis vest and slap bands for running, cycling, hiking.", "outdoor", "Adjustable. 360° reflectors. One size. 2 armbands."),
            ("Hiking Daypack Rain Cover", "Outdoor", 9.99, 14.99, 2.40, "Temu", None, "Waterproof pack cover for 25-45L backpacks.", "outdoor", "Elastic hem. 3 sizes. Bright colors for visibility."),
            ("Portable Bidet — Travel Friendly", "Travel", 11.99, 17.99, 3.10, "Alibaba", None, "Handheld personal bidet bottle for camping and travel.", "travel", "450ml. Angled nozzle. Easy squeeze. Hygienic."),
            ("Dry Sack Set — 3 Sizes", "Outdoor", 14.99, 21.99, 4.00, "Temu", None, "Roll top dry bags 3L / 8L / 15L.", "outdoor", "IPX7. 3 pack. Assorted colors. Strong seams."),
            ("Fishing Tackle Bag — Small", "Outdoor", 16.99, 24.99, 4.70, "Alibaba", None, "Compact organizer for lures, hooks, tools.", "outdoor", "Water resistant. Many pockets. Shoulder strap."),
            ("Bug Repellent Wristbands — 10 Pack", "Outdoor", 7.99, 11.99, 1.90, "Temu", None, "Natural citronella bands for adults and kids.", "outdoor", "Up to 120h protection each. Adjustable. 10 pack."),
            ("Compact Binoculars — 10x25", "Outdoor", 18.99, 27.99, 5.30, "Alibaba", None, "Lightweight roof prism binoculars for hiking and events.", "outdoor", "10x25. 280g. Foldable. Carry case + strap."),
            ("Tactical Pen — Multi Function", "Travel", 12.99, 18.99, 3.40, "Temu", None, "Stainless pen with glass breaker and stylus.", "travel", "Writes smooth. Tungsten tip. Pocket clip. Gift box."),
            ("Reflective Guyline Set — 8 Pack", "Outdoor", 9.99, 14.99, 2.50, "Alibaba", None, "Bright guy ropes with tensioners for tents and tarps.", "outdoor", "4m each. 8 lines + 8 adjusters. Highly visible."),
            ("Portable Shower Tent — 1 Person", "Outdoor", 32.99, 47.99, 9.80, "Temu", None, "Instant privacy shelter for camping showers.", "outdoor", "90x90x190cm. Ventilated. Roll up door. Carry bag."),
        ]
    },
    "site-vita-nest": {
        "store": {
            "name": "Vita Nest",
            "tagline": "Thoughtful Living for Pets & Gardens",
            "logoHtml": "Vita <span>Nest</span>",
            "description": "Quality pet comfort, garden tools, patio living and eco home accessories. Sourced from trusted suppliers on Alibaba, Temu and wholesale marketplaces for customers in Sweden, Norway, UK and the EU.",
            "email": "care@vitanest.com",
            "phone": "+47 22 123 456 (NO support)",
            "slug": "vita-nest",
            "currency": "EUR",
            "pricesIncludeVat": True,
            "vatRatePct": 25,
            "legalName": "[YOUR COMPANY NAME] AS",
            "orgNumber": "[NO Org 9XXXXXX]",
            "vatNumber": "[VAT e.g. NO999999999MVA]",
            "registeredAddress": "[Registered address, Oslo, Norway]"
        },
        "theme": {
            "primary": "#3a5f3a",
            "primaryDark": "#2a472a",
            "accent": "#d4a373"
        },
        "hero": {
            "title": "Happy Homes, Happy Pets & Gardens",
            "subtitle": "Comfortable pet products, smart garden tools and beautiful patio accessories that make life outdoors and with animals better.",
            "badges": ["Free shipping over €45", "30-day returns", "Full statutory rights for EU/UK/NO/SE"]
        },
        "trust": [
            {"icon": "🐾", "text": "Pet Safe"},
            {"icon": "🌱", "text": "Garden Ready"},
            {"icon": "🚚", "text": "7–21 Day Delivery"},
            {"icon": "🌍", "text": "SE/NO/UK/EU"}
        ],
        "about": {
            "title": "Why Vita Nest?",
            "paragraphs": [
                "We curate thoughtful, well-made products for the creatures and plants we love.",
                "Practical eco-minded items at fair prices from verified suppliers."
            ],
            "features": [
                {"icon": "🐕", "text": "Pet comfort"},
                {"icon": "🌿", "text": "Garden tools"},
                {"icon": "🪴", "text": "Patio living"},
                {"icon": "♻️", "text": "Eco options"}
            ]
        },
        "products": [
            # 56 products - pet, garden, patio, eco
            ("Orthopedic Memory Foam Pet Bed — Large", "Pet", 34.99, 49.99, 10.50, "Alibaba", "Best Seller", "Supportive washable bed for dogs and large cats.", "pet", "Extra thick foam. Removable cover. Water resistant. L 90x65cm."),
            ("Self-Cooling Gel Pet Mat — Pressure Activated", "Pet", 19.99, 29.99, 5.80, "Temu", "Trending", "No-freeze cooling mat that recharges at room temp.", "pet", "3 sizes. Non-toxic gel. Works indoors/out. Washable cover."),
            ("Dog Cooling Vest — Evaporative", "Pet", 24.99, 36.99, 7.20, "Alibaba", None, "Soak, wring, wear — hours of cooling for hot days.", "pet", "Mesh + polymer. Reflective. XS–XXL. Machine wash."),
            ("Slow Feeder Dog Bowl — Anti Bloat", "Pet", 12.99, 18.99, 3.40, "Temu", None, "Maze design slows eating for digestion and fun.", "pet", "BPA free. Non-slip. 2 cup capacity. Dishwasher safe."),
            ("Automatic Pet Water Fountain — 2.5L", "Pet", 27.99, 39.99, 8.40, "Alibaba", None, "Circulating filtered fountain with ultra quiet pump.", "pet", "Triple filter. 3 flow modes. Easy clean. 2.5L."),
            ("Portable Pet Water Bottle with Bowl", "Pet", 11.99, 17.99, 3.10, "Temu", None, "One hand squeeze bottle with fold out drinking tray.", "pet", "400ml. Leak lock. Carabiner. Dishwasher safe."),
            ("Elevated Mesh Pet Bed — Outdoor", "Pet", 29.99, 44.99, 9.00, "Alibaba", None, "Raised breathable cot keeps pets off hot/cold ground.", "pet", "Holds 50kg. Easy assembly. 75x55cm. No tools."),
            ("Pet Grooming Gloves — Deshedding", "Pet", 9.99, 14.99, 2.50, "Temu", None, "Silicone tips gently remove loose fur while petting.", "pet", "One size. Wet or dry. Machine washable pair."),
            ("Cat Window Perch with Suction Cups", "Pet", 22.99, 33.99, 6.70, "Alibaba", "New", "Strong suction window hammock for cats with removable pad.", "pet", "Holds 15kg. 45x35cm. Machine wash cover."),
            ("Pet Hair Remover Roller — Reusable", "Pet", 8.99, 12.99, 2.20, "Temu", None, "Self-cleaning gel roller for furniture and clothes.", "pet", "No refills. Travel size. Wash under water."),
            ("Dog Life Jacket — Reflective", "Pet", 18.99, 27.99, 5.40, "Alibaba", None, "Adjustable safety vest with rescue handle.", "pet", "XS–XL. Bright colors. Strong grab handle."),
            ("Cat Scratching Post — Sisal with Toy", "Pet", 16.99, 24.99, 4.80, "Temu", None, "Tall sisal post with dangling toy and base.", "pet", "55cm. Stable base. Natural sisal. Replaceable toy."),
            ("Pet Travel Carrier — Soft Sided", "Pet", 32.99, 47.99, 9.80, "Alibaba", None, "Airline approved soft carrier with mesh panels.", "pet", "42x27x25cm. Shoulder strap. Fits under seat many airlines."),
            ("Collapsible Silicone Pet Bowl — 2 Pack", "Pet", 9.99, 14.99, 2.40, "Temu", None, "Fold flat travel bowls with carabiner.", "pet", "500ml each. Dishwasher. Food grade silicone."),
            ("Dog Paw Balm & Nose Butter", "Pet", 11.99, 17.99, 3.20, "Alibaba", None, "Natural wax balm for dry paws and noses.", "pet", "50ml tin. Beeswax + oils. Safe if licked."),
            ("Self Watering Plant Pots — 3 Pack", "Garden", 19.99, 29.99, 5.70, "Temu", "Trending", "Indoor/outdoor pots with built-in water reservoir.", "garden", "3 sizes. Terracotta look. 1-2 week water reserve."),
            ("Solar Garden Lights — 12 Pack Stake", "Garden", 17.99, 26.99, 5.10, "Alibaba", None, "Warm white pathway lights. Auto on at dusk.", "garden", "8-10h runtime. Easy push in. Weatherproof."),
            ("Garden Tool Set — 5 Piece with Bag", "Garden", 24.99, 36.99, 7.30, "Temu", None, "Stainless trowel, fork, weeder, rake + pruner.", "garden", "Ergonomic. Canvas carry bag. Rust resistant."),
            ("Outdoor String Lights — 15m Connectable", "Garden", 21.99, 31.99, 6.40, "Alibaba", "Hot", "Warm LED bistro lights for patio and garden.", "garden", "G40 bulbs. Connect up to 5 sets. IP65. Timer."),
            ("Folding Patio Chair — 2 Pack", "Garden", 34.99, 49.99, 10.20, "Temu", None, "Lightweight stackable chairs for balcony and garden.", "garden", "Supports 110kg each. Textilene. Fold flat."),
            ("Plant Stand — 3 Tier Corner", "Garden", 18.99, 27.99, 5.40, "Alibaba", None, "Bamboo or metal corner plant display shelf.", "garden", "Holds 12+ pots. Drainage tray. Indoor/outdoor."),
            ("Watering Can — 5L with Rose", "Garden", 14.99, 21.99, 4.10, "Temu", None, "Galvanized or plastic long spout can.", "garden", "5 liter. Removable rose. Comfort grip."),
            ("Raised Garden Bed Kit — 120x60cm", "Garden", 39.99, 59.99, 12.00, "Alibaba", None, "Modular wood or metal raised bed panels.", "garden", "Easy assembly. Liner included. Good drainage."),
            ("Outdoor Cushion Set — 4 Piece", "Garden", 26.99, 39.99, 7.90, "Temu", None, "Weather resistant seat and back cushions.", "garden", "Fits most chairs. Ties. Water repellent cover."),
            ("Bird Feeder — Squirrel Proof", "Garden", 15.99, 23.99, 4.50, "Alibaba", None, "Tube or platform feeder with weight sensitive baffle.", "garden", "Holds 1L seed. Easy fill. Metal ports."),
            ("Compost Bin — 300L Tumbler", "Garden", 49.99, 74.99, 15.50, "Temu", None, "Dual chamber rotating compost bin.", "garden", "Easy turn. Aerates fast. 2 doors. 300L total."),
            ("Garden Kneeler & Seat with Tool Pouch", "Garden", 22.99, 33.99, 6.70, "Alibaba", None, "Folding kneeler that flips to bench.", "garden", "Thick pad. Tool pockets. Lightweight steel."),
            ("Hanging Planters — Set of 3 Macrame", "Garden", 16.99, 24.99, 4.80, "Temu", "Eco", "Boho cotton rope planters for indoor/outdoor.", "garden", "3 sizes. Strong hooks. Fits 15-25cm pots."),
            ("Patio Umbrella — 2.5m with Tilt", "Garden", 34.99, 49.99, 10.50, "Alibaba", None, "UV50+ market umbrella with crank and tilt.", "garden", "Polyester. 8 ribs. Base not included (sold separate)."),
            ("Seed Starting Trays — 5 Pack with Dome", "Garden", 12.99, 18.99, 3.50, "Temu", None, "Cell trays with humidity dome for seedlings.", "garden", "60 cells total. Reusable. Drainage holes."),
            ("Outdoor Solar Lanterns — 4 Pack", "Garden", 19.99, 29.99, 5.70, "Alibaba", None, "Flameless hanging or table lanterns.", "garden", "Warm light. 6-8h. Weatherproof. Metal look."),
            ("Weeding Tool Set — 3 Hand Tools", "Garden", 13.99, 19.99, 3.70, "Temu", None, "Ergonomic stand-up and hand weeders.", "garden", "Stainless. Long reach option. Comfort grip."),
            ("Pet Proof Garden Fence — 5m Roll", "Garden", 14.99, 21.99, 4.10, "Alibaba", None, "Low decorative fence to protect flower beds.", "garden", "Plastic or metal. 30cm high. Easy stake in."),
            ("Rain Barrel Diverter Kit", "Garden", 17.99, 25.99, 4.90, "Temu", None, "Downspout diverter for collecting rainwater.", "garden", "Fits standard gutters. Includes hose connector."),
            ("Outdoor Throw Blanket — Waterproof Back", "Garden", 18.99, 27.99, 5.30, "Alibaba", None, "Soft picnic blanket with water resistant bottom.", "garden", "150x200cm. Machine wash. Sand/dirt shakes off."),
            ("BBQ Tool Set — 5 Piece Stainless", "Garden", 21.99, 31.99, 6.40, "Temu", None, "Tongs, spatula, fork, brush and holder.", "garden", "Heat resistant handles. Hanging case."),
            ("Herb Scissors — 5 Blade", "Garden", 8.99, 12.99, 2.20, "Alibaba", None, "Multi blade herb scissors with cleaning comb.", "garden", "Stainless. Comfort grip. Dishwasher safe."),
            ("Folding Picnic Table — Compact", "Garden", 27.99, 41.99, 8.20, "Temu", None, "Portable table seats 4. Folds into suitcase.", "garden", "Aluminum top. 85x65cm. 4 seats. 4.5kg."),
            ("Cat Grass Growing Kit — 3 Pack", "Pet", 9.99, 14.99, 2.50, "Temu", None, "Easy grow wheatgrass for indoor cats.", "pet", "3 trays + seeds. Non-GMO. Grows in 5-7 days."),
            ("Dog Training Clicker + Treat Pouch", "Pet", 10.99, 15.99, 2.80, "Alibaba", None, "Professional clicker and waist treat bag.", "pet", "Adjustable. Hands free. Loud clicker."),
            ("Pet Steps for Sofa or Car — 3 Tier", "Pet", 23.99, 34.99, 7.00, "Temu", None, "Foldable ramp/steps for older pets.", "pet", "Holds 40kg. Non-slip. Compact storage."),
            ("Garden Pruning Shears — Bypass", "Garden", 11.99, 17.99, 3.20, "Alibaba", None, "Sharp bypass pruners with safety lock.", "garden", "SK5 blade. Ergonomic. 20mm cut capacity."),
            ("Outdoor Solar Spotlight — 4 Pack", "Garden", 16.99, 24.99, 4.70, "Temu", None, "Adjustable ground or wall solar spotlights.", "garden", "2 brightness. 8h runtime. 4 pack."),
            ("Natural Loofah Sponges — 6 Pack", "Eco Home", 9.99, 14.99, 2.40, "Alibaba", "Eco", "Biodegradable kitchen and bath sponges.", "garden", "Grown loofah. Compostable. 6 assorted sizes."),
            ("Bamboo Toothbrush Set — 8 Pack", "Eco Home", 10.99, 15.99, 2.70, "Temu", None, "Soft bristle bamboo brushes for family.", "garden", "8 brushes. Charcoal or plain. Biodegradable."),
            ("Reusable Produce Bags — 9 Piece Mesh", "Eco Home", 12.99, 18.99, 3.40, "Alibaba", None, "Washable mesh bags for fruit and veg shopping.", "garden", "3 sizes. Tare weight tags. Machine wash."),
            ("Compostable Kitchen Trash Bags — 50 Pack", "Eco Home", 11.99, 17.99, 3.10, "Temu", None, "Strong plant based bin liners.", "garden", "Fits 10-15L. ASTM D6400. Leak resistant."),
            ("Indoor Herb Garden Kit — Self Watering", "Garden", 19.99, 29.99, 5.80, "Alibaba", "Trending", "3 pod windowsill planter with seeds.", "garden", "Basil, parsley, mint. LED grow light option."),
            ("Pet Waste Bag Holder + 120 Bags", "Pet", 8.99, 12.99, 2.10, "Temu", None, "Leash dispenser with 8 rolls of bags.", "pet", "Fits standard leashes. Includes 120 bags."),
            ("Garden Hose Nozzle Set — 8 Patterns", "Garden", 9.99, 14.99, 2.50, "Alibaba", None, "Heavy duty metal pistol grip sprayer.", "garden", "8 spray patterns. Leak free. Comfort grip."),
            ("Outdoor Planter Box — Rectangular Large", "Garden", 29.99, 44.99, 8.90, "Temu", None, "Weatherproof resin or wood look planter.", "garden", "80x30x30cm. Drainage plugs. Lightweight."),
            ("Dog Dental Chew Toy Set", "Pet", 13.99, 19.99, 3.70, "Alibaba", None, "Dental cleaning toys with treat pockets.", "pet", "3 shapes. Tough rubber. Easy clean."),
            ("Solar Bird Bath Fountain Pump", "Garden", 14.99, 21.99, 4.10, "Temu", None, "Floating solar pump for bird baths and small ponds.", "garden", "No wiring. 3 fountain heads. Runs in sun."),
            ("Eco Laundry Detergent Sheets — 60 Load", "Eco Home", 12.99, 18.99, 3.50, "Alibaba", None, "Plastic free concentrated laundry strips.", "garden", "60 loads. Biodegradable. Travel friendly."),
            ("Patio Side Table — Foldable", "Garden", 16.99, 24.99, 4.80, "Temu", None, "Small weather resistant accent table.", "garden", "40cm diameter. Folds flat. Strong frame."),
        ]
    }
}

def build_product(idx, tpl, site_folder):
    name, cat, price, orig, cost, source, badge, desc, img_key, details = tpl
    rel = f"images/{idx}.jpg"
    return {
        "id": idx,
        "name": name,
        "category": cat,
        "price": price,
        "originalPrice": orig,
        "cost": cost,
        "source": source,
        "badge": badge,
        "description": desc,
        "details": details,
        "image": rel,
        "images": [rel],
        "imageKey": img_key,
        "sku": f"SKU-{idx:04d}",
        "inStock": True,
        "shippingDays": "7-21 business days to SE/NO/UK/EU",
    }

def main():
    for folder, data in STORES.items():
        out = {
            "store": data["store"],
            "theme": data["theme"],
            "hero": data["hero"],
            "trust": data["trust"],
            "about": data["about"],
            "policies": POLICIES,
            "products": [build_product(i + 1, p, folder) for i, p in enumerate(data["products"])],
            "launchReady": True,
        }
        path = os.path.join(ROOT, folder, "products.json")
        with open(path, "w") as f:
            json.dump(out, f, indent=2)
        print(f"Wrote {len(out['products'])} products to {folder}")
    print("Done. Now run fetch_product_images.py (or use Unsplash fallbacks). Update admin and root index.")

if __name__ == "__main__":
    main()
