#!/usr/bin/env python3
"""Generate expanded product catalogs with category-matched Unsplash images."""

import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# Verified Unsplash images mapped by topic (w=600&h=450&fit=crop&q=80)
IMG = {
    "pool": "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?w=600&h=450&fit=crop&q=80",
    "pool_clean": "https://images.unsplash.com/photo-1519315901367-f34ff9154487?w=600&h=450&fit=crop&q=80",
    "pool_water": "https://images.unsplash.com/photo-1575429198097-0414ec08e8cd?w=600&h=450&fit=crop&q=80",
    "lawn_mower": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=450&fit=crop&q=80",
    "garden": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=600&h=450&fit=crop&q=80",
    "sprinkler": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=600&h=450&fit=crop&q=80",
    "cleaning": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=600&h=450&fit=crop&q=80",
    "pressure_wash": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&h=450&fit=crop&q=80",
    "mop": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=600&h=450&fit=crop&q=80",
    "hedge": "https://images.unsplash.com/photo-1558904541-efa843a96f01?w=600&h=450&fit=crop&q=80",
    "leaf_blower": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=600&h=450&fit=crop&q=80",
    "gutter": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=600&h=450&fit=crop&q=80",
    "swimsuit_w": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=600&h=450&fit=crop&q=80",
    "shorts_m": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=600&h=450&fit=crop&q=80",
    "kids_swim": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600&h=450&fit=crop&q=80",
    "sun_hat": "https://images.unsplash.com/photo-1521369909029-2afed882baee?w=600&h=450&fit=crop&q=80",
    "sunglasses": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&h=450&fit=crop&q=80",
    "beach": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&h=450&fit=crop&q=80",
    "pool_float": "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=600&h=450&fit=crop&q=80",
    "beach_tent": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=600&h=450&fit=crop&q=80",
    "beach_bag": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=600&h=450&fit=crop&q=80",
    "flip_flops": "https://images.unsplash.com/photo-1515347619252-60a6bf4fffce?w=600&h=450&fit=crop&q=80",
    "coverup": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&h=450&fit=crop&q=80",
    "sandals": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600&h=450&fit=crop&q=80",
    "pool_toy": "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?w=600&h=450&fit=crop&q=80",
    "ac_unit": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=600&h=450&fit=crop&q=80",
    "desk_fan": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&h=450&fit=crop&q=80",
    "neck_fan": "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=600&h=450&fit=crop&q=80",
    "hand_fan": "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600&h=450&fit=crop&q=80",
    "cooler": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=600&h=450&fit=crop&q=80",
    "cooler_box": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=600&h=450&fit=crop&q=80",
    "cooling_towel": "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=600&h=450&fit=crop&q=80",
    "tower_fan": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&h=450&fit=crop&q=80",
    "ice_maker": "https://images.unsplash.com/photo-1578911373434-0cb395d2cbfb?w=600&h=450&fit=crop&q=80",
    "dog": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600&h=450&fit=crop&q=80",
    "dog_outdoor": "https://images.unsplash.com/photo-1530281700549-e82e7bf110d6?w=600&h=450&fit=crop&q=80",
    "dog_bed": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600&h=450&fit=crop&q=80",
    "dog_water": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600&h=450&fit=crop&q=80",
    "cat": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&h=450&fit=crop&q=80",
    "pet_car": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600&h=450&fit=crop&q=80",
    "pet_boots": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600&h=450&fit=crop&q=80",
    "pet_fountain": "https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=600&h=450&fit=crop&q=80",
    "camping": "https://images.unsplash.com/photo-1504851149312-7a075b496cc7?w=600&h=450&fit=crop&q=80",
    "hiking": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&h=450&fit=crop&q=80",
    "lantern": "https://images.unsplash.com/photo-1475483768296-6163e08872a1?w=600&h=450&fit=crop&q=80",
    "tent": "https://images.unsplash.com/photo-1504851149312-7a075b496cc7?w=600&h=450&fit=crop&q=80",
    "backpack": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&h=450&fit=crop&q=80",
    "camp_stove": "https://images.unsplash.com/photo-1682687220063-4742bd7fd538?w=600&h=450&fit=crop&q=80",
    "survival": "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=600&h=450&fit=crop&q=80",
    "mosquito": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&h=450&fit=crop&q=80",
}

POLICIES = {
    "returns": {
        "title": "Returns & Refunds",
        "summary": "14-day return window on unused items in original packaging. Return shipping paid by customer unless item is defective or incorrect.",
        "sections": [
            {"heading": "Return Eligibility", "text": "You may return most unused items within 14 days of delivery. Items must be in original packaging with all accessories included. Opened chemical products, personalized items, and final-sale clearance items cannot be returned."},
            {"heading": "How to Start a Return", "text": "Email our support team with your order number and reason for return. We will provide a Return Merchandise Authorization (RMA) number within 2 business days. Returns without an RMA may not be processed."},
            {"heading": "Refund Processing", "text": "Once we receive and inspect your return, refunds are issued to your original payment method within 5–10 business days. Shipping costs are non-refundable. A restocking fee of up to 15% may apply to large items returned without defect."},
            {"heading": "Damaged or Wrong Items", "text": "If you receive a damaged or incorrect item, contact us within 48 hours with photos. We will arrange a free replacement or full refund including shipping — at no cost to you."},
            {"heading": "Exchanges", "text": "We do not hold inventory for direct exchanges. Please return the original item for a refund and place a new order for the replacement."}
        ]
    },
    "shipping": {
        "title": "Shipping Policy",
        "summary": "Orders ship within 1–3 business days. Delivery takes 7–21 business days depending on supplier location.",
        "sections": [
            {"heading": "Processing Time", "text": "Orders are processed within 1–3 business days. You will receive a confirmation email with tracking once your order ships."},
            {"heading": "Delivery Estimates", "text": "Standard delivery: 7–14 business days (U.S. warehouse items). Extended delivery: 14–21 business days (international supplier fulfillment). Delivery times are estimates, not guarantees."},
            {"heading": "Shipping Costs", "text": "Free standard shipping on qualifying orders as noted on each product page. Oversized items may incur additional shipping fees disclosed at checkout."},
            {"heading": "Lost or Delayed Packages", "text": "If tracking shows no movement for 10+ business days, contact us. We will work with the carrier and supplier to resolve the issue. We are not liable for carrier delays beyond our control."}
        ]
    },
    "terms": {
        "title": "Terms of Service",
        "summary": "By purchasing from us you agree to these terms. We operate as a retailer sourcing products from third-party suppliers.",
        "sections": [
            {"heading": "Business Model", "text": "We are an online retailer. Products are sourced from third-party suppliers (including Alibaba, Temu, and Amazon wholesale partners) and shipped directly to you. Product packaging and minor cosmetic variations may differ from listing photos."},
            {"heading": "Product Descriptions", "text": "We make every effort to display accurate product information. However, we do not warrant that descriptions, images, or specifications are error-free. Colors may vary due to monitor settings and supplier batches."},
            {"heading": "Pricing", "text": "All prices are in USD. We reserve the right to change prices without notice. Pricing errors may result in order cancellation with a full refund."},
            {"heading": "Limitation of Liability", "text": "Our total liability for any claim shall not exceed the amount you paid for the specific product. We are not liable for indirect, incidental, or consequential damages. Products are sold for general consumer use — not for medical, veterinary, or professional applications unless explicitly stated."},
            {"heading": "Dispute Resolution", "text": "Disputes shall first be addressed through our customer support. If unresolved, disputes are subject to binding arbitration in accordance with applicable law."}
        ]
    },
    "privacy": {
        "title": "Privacy Policy",
        "summary": "We collect only the information needed to process orders and respond to inquiries. We never sell your data.",
        "sections": [
            {"heading": "Information We Collect", "text": "Name, email, phone, shipping address, and order details when you purchase or contact us. Browsing data via standard cookies for site functionality."},
            {"heading": "How We Use Your Data", "text": "To process and fulfill orders, send order updates, respond to inquiries, and improve our website. Payment data is handled by third-party payment processors — we do not store credit card numbers."},
            {"heading": "Data Sharing", "text": "We share order information only with fulfillment partners and shipping carriers as needed to deliver your products. We do not sell or rent personal information to third parties."},
            {"heading": "Your Rights", "text": "You may request access to, correction of, or deletion of your personal data by emailing our support address. We respond within 30 days."},
            {"heading": "Data Retention", "text": "Order records are retained for 3 years for tax and legal compliance. Marketing emails include an unsubscribe link."}
        ]
    }
}

STORES = {
    "site1-verdant-haven": {
        "store": {"name": "Verdant Haven", "tagline": "Lawn, Pool & Home Care Essentials", "logoHtml": "Verdant <span>Haven</span>",
                  "description": "Professional-grade lawn, pool, and home maintenance products sourced from verified Alibaba, Temu, and Amazon wholesale partners.",
                  "email": "support@verdanthaven.com", "phone": "1-800-VERDANT", "slug": "verdant-haven"},
        "theme": {"primary": "#2d6a4f", "primaryDark": "#1b4332", "accent": "#95d5b2"},
        "hero": {"title": "Your Home & Yard, Perfectly Maintained", "subtitle": "Premium lawn care, pool maintenance, and household cleaning supplies — shipped from U.S. warehouse partners.",
                 "badges": ["Free Shipping Over $49", "14-Day Returns", "Verified Suppliers"]},
        "trust": [{"icon": "🚚", "text": "7–14 Day Delivery"}, {"icon": "⭐", "text": "4.8★ Rating"}, {"icon": "🔒", "text": "Secure Checkout"}, {"icon": "💬", "text": "Email Support"}],
        "about": {"title": "Why Choose Verdant Haven?", "paragraphs": ["Verdant Haven curates professional home and yard care products from verified global suppliers.", "Every item is selected for durability and value at prices that beat big-box stores."],
                  "features": [{"icon": "🌿", "text": "Eco-friendly options"}, {"icon": "🏊", "text": "Pool-safe products"}, {"icon": "📦", "text": "Bulk savings"}, {"icon": "✅", "text": "14-day returns"}]},
        "products": [
            ("Robotic Pool Skimmer — Solar Powered", "Pool Care", 89.99, 129.99, 34.50, "Alibaba", "Best Seller", "Automatic solar pool skimmer removes leaves and debris 24/7 with zero electricity.", "pool", "Solar panel charges internal battery. Works in in-ground and above-ground pools up to 30ft. UV-resistant ABS housing."),
            ("Telescopic Pool Pole & Vacuum Head Kit", "Pool Care", 42.99, 59.99, 16.80, "Amazon Wholesale", None, "12-ft adjustable aluminum pole with vacuum head, brush, and leaf skimmer.", "pool_clean", "3-section telescopic pole extends 6–12 ft. Universal clip fittings. Includes 8-inch vacuum head and mesh skimmer."),
            ("3-In-1 Pool Test Strips — 100 Count", "Pool Care", 18.99, 27.99, 6.20, "Temu", None, "Tests chlorine, pH, and alkalinity in 15 seconds for safe swimming water.", "pool_water", "Dip and compare color chart. Results in 15 seconds. Store in cool dry place. 2-year shelf life."),
            ("Chlorine Floater & Tablet Dispenser", "Pool Care", 14.99, 22.99, 4.50, "Temu", None, "Adjustable chlorine dispenser for pools up to 30,000 gallons.", "pool", "Holds up to 3-inch tablets. Adjustable release rate. UV-stabilized plastic."),
            ("Pool Cover Reel System — 18ft", "Pool Care", 74.99, 109.99, 28.00, "Alibaba", "New", "Stainless steel pool cover reel with hand crank for easy cover storage.", "pool_clean", "Fits covers up to 18 ft wide. Rust-proof 304 stainless. Includes mounting brackets and straps."),
            ("Cordless Electric Lawn Mower — 17 Inch", "Lawn Care", 189.99, 279.99, 78.00, "Alibaba", "Hot Deal", "40V brushless motor, 6 height settings, folds flat. Cuts up to 1/3 acre per charge.", "lawn_mower", "17-inch cutting deck. 40V 4.0Ah battery included. 6-position height adjustment 1–3 inches. 60-min runtime."),
            ("Expandable Garden Hose — 100ft", "Lawn Care", 34.99, 49.99, 12.40, "Temu", None, "Lightweight expandable hose with 9-pattern spray nozzle and brass fittings.", "garden", "Expands to 100ft under pressure, contracts for storage. Solid brass connectors. 9 spray patterns."),
            ("Programmable Sprinkler Timer — 2 Zone", "Lawn Care", 29.99, 44.99, 11.50, "Amazon Wholesale", None, "Digital water timer with rain delay, manual override, and dual-valve control.", "sprinkler", "2 independent zones. Programs up to 30 days. Rain delay and manual mode. Weather-resistant housing."),
            ("Cordless Hedge Trimmer — 20V", "Lawn Care", 79.99, 119.99, 32.00, "Alibaba", None, "20V lithium hedge trimmer with 22-inch dual-action blade.", "hedge", "22-inch hardened steel blade. 2.0Ah battery and charger included. Safety guard and blade cover."),
            ("Leaf Blower — Cordless 130 MPH", "Lawn Care", 69.99, 99.99, 26.00, "Temu", None, "Lightweight cordless blower with 2 speed settings, 130 MPH max airspeed.", "leaf_blower", "20V battery platform. Weighs 4.4 lbs. Variable speed trigger. Includes flat and round nozzles."),
            ("Robot Window Cleaner — Magnetic", "Home Care", 54.99, 79.99, 22.00, "Alibaba", "New", "Dual-sided magnetic cleaner for streak-free single and double-pane windows.", "cleaning", "Neodymium magnets hold pads on both sides. Microfiber pads included. Works on 2–8mm glass."),
            ("Cordless Pressure Washer — 40V 800 PSI", "Home Care", 119.99, 169.99, 48.00, "Alibaba", None, "Portable washer for driveways, siding, decks. Includes 4 spray nozzles.", "pressure_wash", "800 PSI max pressure. 40V battery. 20-ft hose. 0°, 15°, 25°, and soap nozzles included."),
            ("Microfiber Mop System with 6 Pads", "Home Care", 24.99, 36.99, 8.90, "Temu", None, "360° swivel mop with washable microfiber pads for all hard floors.", "mop", "Aluminum handle extends 35–60 inches. 6 reusable microfiber pads. Machine washable."),
            ("Gutter Cleaning Wand — 12ft Extendable", "Home Care", 39.99, 57.99, 14.00, "Amazon Wholesale", None, "Curved gutter cleaning attachment fits standard garden hoses.", "gutter", "Extends from 6 to 12 feet. 180° curved nozzle reaches inside gutters. High-pressure spray."),
            ("Robot Vacuum — WiFi App Control", "Home Care", 149.99, 219.99, 58.00, "Alibaba", "Best Seller", "Smart robot vacuum with app mapping, auto-recharge, and HEPA filter.", "mop", "2000Pa suction. 120-min runtime. LiDAR navigation. Works with iOS/Android app."),
            ("Outdoor Furniture Cleaner — 1 Gallon", "Home Care", 22.99, 32.99, 7.50, "Temu", None, "Concentrated cleaner for patio furniture, decks, and outdoor cushions.", "pressure_wash", "Covers 500 sq ft per gallon. Safe on wood, wicker, metal, and fabric. Biodegradable formula."),
            ("Lawn Aerator Shoes — Spiked Sandals", "Lawn Care", 19.99, 29.99, 6.00, "Temu", None, "Strap-on spiked sandals aerate lawn soil while you walk.", "garden", "13 heavy-duty 2-inch spikes per shoe. One-size adjustable straps. Durable ABS base."),
            ("Pool Vacuum Head — Weighted Flex", "Pool Care", 27.99, 39.99, 9.80, "Amazon Wholesale", None, "Weighted flexible vacuum head fits standard 1.5-inch hoses.", "pool_clean", "Flexible urethane body conforms to pool contours. Weighted for sink. Universal hose cuff."),
            ("Pool Wall Algae Brush — 18 Inch Wide", "Pool Care", 21.99, 31.99, 7.20, "Alibaba", "New", "Stainless steel bristle brush for concrete and tile pool walls.", "pool_clean", "18-inch anodized aluminum back. Stainless bristles. Fits standard telepole attachment."),
            ("Cordless Grass Shears & Shrub Trimmer", "Lawn Care", 49.99, 74.99, 18.50, "Temu", None, "2-in-1 handheld grass shears for edges, hedges, and tight corners.", "hedge", "3.6V lithium battery. 2-hour runtime. Includes grass shear and shrub trimmer attachments."),
            ("WiFi Smart Sprinkler Controller — 8 Zone", "Lawn Care", 89.99, 129.99, 34.00, "Alibaba", "Hot", "App-controlled 8-zone irrigation with weather skip and Alexa support.", "sprinkler", "8 zones. iOS/Android app. Weather-based auto-skip. Works with Alexa and Google Home."),
            ("Deck Stain Applicator Pad Kit — 3 Piece", "Home Care", 26.99, 39.99, 9.00, "Amazon Wholesale", None, "Extension pole stain pads for decks, fences, and outdoor wood.", "garden", "Includes 7-inch and 9-inch pads plus extension pole adapter. Reusable microfiber pads."),
            ("Pool pH Plus Increaser — 5 lb Pail", "Pool Care", 19.99, 28.99, 6.80, "Temu", None, "Granular pH increaser raises pool alkalinity safely and quickly.", "pool_water", "99% sodium carbonate. 5 lb pail treats up to 25,000 gallons. Fast-dissolving granules."),
        ]
    },
    "site2-solara-coast": {
        "store": {"name": "Solara Coast", "tagline": "Summer Style, Beach & Pool Living", "logoHtml": "Solara <span>Coast</span>",
                  "description": "Trend-forward summer fashion and beach essentials for the whole family. Curated from global suppliers.",
                  "email": "hello@solaracoast.com", "phone": "1-800-SOLARA", "slug": "solara-coast"},
        "theme": {"primary": "#0077b6", "primaryDark": "#023e8a", "accent": "#ff6b6b"},
        "hero": {"title": "Summer Starts Here", "subtitle": "Swimwear, beach gear, and pool accessories for kids and adults.",
                 "badges": ["UPF 50+ Options", "Family Sizes XS–3XL", "14-Day Returns"]},
        "trust": [{"icon": "👙", "text": "Sun Protection"}, {"icon": "🚚", "text": "7–14 Day Delivery"}, {"icon": "💰", "text": "Bundle & Save"}, {"icon": "🌊", "text": "Beach-Tested"}],
        "about": {"title": "Dress for the Coast", "paragraphs": ["Solara Coast brings runway-inspired summer fashion at accessible prices.", "From beach days to pool parties — apparel and accessories that look premium without the markup."],
                  "features": [{"icon": "👨‍👩‍👧", "text": "Family matching sets"}, {"icon": "☀️", "text": "UV-protective fabrics"}, {"icon": "🏖️", "text": "Sand-proof gear"}, {"icon": "💧", "text": "Quick-dry tech"}]},
        "products": [
            ("Women's One-Piece Swimsuit — Tropical Print", "Women's Fashion", 36.99, 54.99, 14.20, "Temu", "Trending", "Tummy-control one-piece with adjustable straps and UPF 50+ fabric.", "swimsuit_w", "82% nylon, 18% spandex. UPF 50+. Adjustable shoulder straps. Available S–XL."),
            ("Women's Bikini Set — High-Waist", "Women's Fashion", 32.99, 48.99, 12.00, "Alibaba", None, "High-waist bikini with removable padding and tie-side bottoms.", "swimsuit_w", "High-waist bottom with tummy control. Removable soft cups. Quick-dry fabric."),
            ("Women's Swim Cover-Up Dress", "Women's Fashion", 28.99, 42.99, 10.50, "Temu", None, "Sheer kaftan cover-up with side slits. One size fits most.", "coverup", "Lightweight chiffon. V-neck with tie closure. Knee-length. Packable."),
            ("Men's Quick-Dry Board Shorts — 7 Inch", "Men's Fashion", 28.99, 42.99, 10.50, "Alibaba", None, "Board shorts with mesh lining, zip pocket, and 4-way stretch.", "shorts_m", "7-inch inseam. Zippered side pocket. Mesh brief lining. 4-way stretch polyester."),
            ("Men's Rash Guard — Long Sleeve", "Men's Fashion", 26.99, 39.99, 9.80, "Temu", None, "UPF 50+ long-sleeve rash guard for surfing and swimming.", "shorts_m", "UPF 50+ sun protection. Flatlock seams. Quick-dry. Sizes S–XXL."),
            ("Men's Linen Beach Shirt", "Men's Fashion", 34.99, 49.99, 13.00, "Alibaba", "New", "Breathable linen button-down for beach and resort wear.", "coverup", "100% linen. Relaxed fit. Chest pocket. Machine washable. Sizes S–XXL."),
            ("Kids' Rash Guard & Swim Trunks Set", "Kids' Fashion", 22.99, 34.99, 8.40, "Temu", "Best Seller", "Long-sleeve UPF 50+ rash guard with matching trunks. Sizes 2T–14.", "kids_swim", "UPF 50+ protection. Sizes 2T, 4T, 6, 8, 10, 12, 14. Quick-dry polyester."),
            ("Kids' Swim Goggles — Anti-Fog", "Kids' Fashion", 12.99, 19.99, 4.20, "Alibaba", None, "Adjustable anti-fog swim goggles with UV protection for ages 3–12.", "kids_swim", "Anti-fog coated lenses. UV400 protection. Adjustable split strap. Soft silicone gasket."),
            ("Wide-Brim Sun Hat — Packable UPF 50+", "Accessories", 19.99, 29.99, 6.80, "Alibaba", None, "Packable floppy sun hat with chin strap. One size fits most.", "sun_hat", "UPF 50+ rated. 4.5-inch brim. Adjustable chin cord. Folds flat."),
            ("Polarized Sunglasses — UV400 Metal Frame", "Accessories", 24.99, 39.99, 7.20, "Temu", None, "Polarized lenses with metal frame, hard case, and cleaning cloth.", "sunglasses", "TAC polarized lenses. UV400 protection. Metal alloy frame. Includes case and cloth."),
            ("Waterproof Phone Pouch — 2 Pack", "Accessories", 11.99, 17.99, 3.50, "Temu", None, "IPX8 waterproof phone case for beach and pool. Fits phones up to 7 inches.", "beach_bag", "IPX8 certified to 100ft. Touchscreen compatible. Neck lanyard included. 2-pack."),
            ("Oversized Beach Towel — 35x70 Inches", "Beach Essentials", 26.99, 38.99, 9.50, "Alibaba", None, "Sand-resistant microfiber towel. Absorbs 3x weight, dries in minutes.", "beach", "35x70 inches. Microfiber polyester. Sand shakes off. Includes carry loop."),
            ("Beach Cabana Tent — Pop-Up UPF 50+", "Beach Essentials", 59.99, 89.99, 24.00, "Alibaba", "New", "Instant beach tent with sand pockets and mesh windows. Fits 2–3 people.", "beach_tent", "87x47x49 inches. UPF 50+. Sand pockets and stakes. Foldable carry bag."),
            ("Waterproof Beach Tote with Cooler Pocket", "Beach Essentials", 34.99, 49.99, 13.50, "Temu", None, "Mesh beach bag with insulated cooler compartment and sand-proof bottom.", "beach_bag", "30L capacity. Insulated cooler pocket fits 6 cans. Zippered top pocket."),
            ("Beach Blanket — Sand-Free 79x79", "Beach Essentials", 29.99, 44.99, 10.00, "Alibaba", None, "Waterproof sand-proof picnic blanket with corner stakes.", "beach", "79x79 inches. Waterproof backing. 4 corner stakes. Machine washable."),
            ("Inflatable Pool Lounger with Cup Holders", "Pool Products", 32.99, 49.99, 12.00, "Temu", "Hot", "Extra-large floating lounger with headrest and dual cup holders. 250 lb capacity.", "pool_float", "72x28 inches inflated. Dual cup holders. Headrest pillow. Heavy-duty vinyl."),
            ("Floating Pool Drink Holder — 6 Pack", "Pool Products", 16.99, 24.99, 5.40, "Alibaba", None, "Inflatable drink floats for cans, bottles, and wine glasses.", "pool_toy", "6 assorted colors. Fits standard cans and bottles. 4-inch diameter each."),
            ("Kids' Pool Float with Canopy", "Pool Products", 27.99, 39.99, 9.50, "Temu", None, "Sun-shade canopy float for toddlers with safety seat.", "pool_float", "Built-in sun canopy UPF 50+. Safety seat with leg holes. Ages 1–4, up to 40 lbs."),
            ("Men's Floral Swim Trunks — Quick Dry", "Men's Fashion", 24.99, 36.99, 8.50, "Temu", "New", "Vibrant floral print swim trunks with mesh lining and drawstring.", "shorts_m", "Quick-dry polyester. Mesh lining. Side zip pocket. Sizes S–XXL."),
            ("Women's Straw Beach Tote Bag", "Accessories", 29.99, 44.99, 10.00, "Alibaba", None, "Handwoven straw tote with cotton lining and magnetic snap closure.", "beach_bag", "Natural straw weave. Cotton lining. Interior zip pocket. 16x12x6 inches."),
            ("Beach Paddle Ball Set — 2 Rackets", "Beach Essentials", 18.99, 27.99, 5.50, "Temu", None, "Wooden paddle ball set with 2 paddles and 2 balls in mesh carry bag.", "beach", "Solid wood paddles. High-bounce rubber balls. Mesh storage bag included."),
            ("Foam Pool Noodles — 5 Pack 52 Inch", "Pool Products", 19.99, 29.99, 5.80, "Amazon Wholesale", None, "Flexible foam noodles for swimming, floating, and pool games.", "pool_toy", "52-inch length. 2.5-inch diameter. Assorted colors. Closed-cell foam."),
            ("Kids' Beach Sandals — Adjustable Strap", "Kids' Fashion", 16.99, 24.99, 4.80, "Temu", None, "Lightweight EVA beach sandals with hook-and-loop strap. Sizes 11–3.", "flip_flops", "EVA foam footbed. Non-slip sole. Adjustable hook-and-loop. Sizes toddler through youth."),
        ]
    },
    "site3-arcticflow": {
        "store": {"name": "ArcticFlow", "tagline": "Stay Cool. Stay Comfortable.", "logoHtml": "Arctic<span>Flow</span>",
                  "description": "Portable AC units, personal fans, cooler bags, and cooling accessories for record summer heat.",
                  "email": "cool@arcticflow.com", "phone": "1-800-COOLAIR", "slug": "arcticflow"},
        "theme": {"primary": "#0096c7", "primaryDark": "#0077b6", "accent": "#48cae4"},
        "hero": {"title": "Advanced Cooling for Every Space", "subtitle": "From portable air conditioners to neck fans and insulated coolers.",
                 "badges": ["Heatwave Ready", "Energy Efficient", "14-Day Returns"]},
        "trust": [{"icon": "❄️", "text": "Proven Cooling"}, {"icon": "⚡", "text": "Low Energy Use"}, {"icon": "📦", "text": "Free Ship $75+"}, {"icon": "🛡️", "text": "1-Year Warranty"}],
        "about": {"title": "Engineered for Heat Relief", "paragraphs": ["ArcticFlow stocks cooling products seeing 40%+ demand surges during heatwaves.", "Selected for real-world performance with competitive pricing through direct supplier relationships."],
                  "features": [{"icon": "🏠", "text": "Room & personal cooling"}, {"icon": "🔋", "text": "Rechargeable options"}, {"icon": "🧊", "text": "Insulated coolers"}, {"icon": "📱", "text": "Smart app AC"}]},
        "products": [
            ("Portable Air Conditioner — 8,000 BTU", "Air Conditioning", 299.99, 449.99, 128.00, "Alibaba", "Top Rated", "Cools rooms up to 250 sq ft. Remote, timer, window kit included.", "ac_unit", "8000 BTU. 250 sq ft coverage. Remote control. 24-hour timer. Window vent kit included."),
            ("Mini Evaporative Air Cooler — Desktop", "Air Conditioning", 49.99, 74.99, 18.50, "Temu", None, "3-in-1 cooler, humidifier, and fan. 3 speeds, 7-color LED, USB powered.", "desk_fan", "3-speed fan. 700ml water tank. 7 LED colors. USB powered. Whisper-quiet under 40dB."),
            ("Window AC Foam Seal Kit — Universal", "Air Conditioning", 34.99, 49.99, 12.00, "Amazon Wholesale", None, "Foam seal and weather stripping for 5,000–12,000 BTU window units.", "ac_unit", "High-density foam panels. Adjustable length. Weather stripping tape included."),
            ("Portable AC Exhaust Hose — 5ft", "Air Conditioning", 19.99, 29.99, 6.50, "Temu", None, "Universal 5-inch diameter exhaust hose with window adapter.", "ac_unit", "5ft length. 5-inch diameter. Universal window plate adapter. Insulated foil construction."),
            ("Bladeless Neck Fan — USB Rechargeable", "Personal Fans", 29.99, 44.99, 9.80, "Alibaba", "Trending", "Hands-free bladeless neck fan. 3 speeds, 8-hour battery, under 25dB.", "neck_fan", "Bladeless design. 3 speed settings. 4000mAh battery. 8-hour runtime. USB-C charging."),
            ("High-Velocity Floor Fan — 20 Inch", "Personal Fans", 54.99, 79.99, 22.00, "Amazon Wholesale", None, "Industrial 3-speed metal floor fan with adjustable tilt. 75 ft air throw.", "tower_fan", "20-inch blade. 3 speeds. Adjustable tilt head. Metal construction. 6.5 ft cord."),
            ("Foldable Handheld Fan with Power Bank", "Personal Fans", 19.99, 29.99, 6.50, "Temu", "Best Value", "Compact folding fan doubles as 2000mAh power bank with desk stand.", "hand_fan", "Folds to pocket size. 2000mAh power bank. 3 speeds. Built-in desk stand."),
            ("Tower Fan — 36 Inch Oscillating Remote", "Personal Fans", 64.99, 94.99, 25.00, "Alibaba", None, "36-inch oscillating tower fan with remote, timer, and 3 speed modes.", "tower_fan", "36-inch height. 65° oscillation. Remote control. 7.5-hour timer. 3 speeds."),
            ("Clip-On Stroller Fan — Rechargeable", "Personal Fans", 16.99, 24.99, 5.20, "Temu", None, "360° flexible clip fan for strollers, desks, and treadmills.", "hand_fan", "Flexible gooseneck clip. 3600mAh battery. 3 speeds. USB rechargeable."),
            ("Hard Cooler Box — 52 Quart", "Coolers", 89.99, 129.99, 36.00, "Alibaba", None, "Rotomolded insulation keeps ice 5+ days. Bear-resistant latch.", "cooler_box", "52-quart capacity. Holds 80 cans. 5+ day ice retention. Drain plug and cup holders."),
            ("Insulated Cooler Backpack — 30L", "Coolers", 39.99, 59.99, 15.00, "Temu", None, "Leak-proof cooler backpack holds 36 cans with padded straps.", "cooler", "30L / 36-can capacity. Leak-proof liner. Padded straps. Bottle opener included."),
            ("Electric Cooler/Warmer — 24L Car Plug", "Coolers", 119.99, 169.99, 48.00, "Alibaba", "New", "Thermoelectric cooler: 40°F below ambient or warms to 140°F.", "cooler_box", "24L capacity. Cools to 40°F below ambient. 12V car and 110V home adapter."),
            ("Soft Cooler Bag — 24 Can Collapsible", "Coolers", 27.99, 39.99, 9.80, "Temu", None, "Collapsible soft cooler with welded seams and shoulder strap.", "cooler", "Holds 24 cans. Welded leak-proof seams. Collapses flat. Adjustable shoulder strap."),
            ("Cooling Towel 4-Pack — Instant Relief", "Cooling Accessories", 16.99, 24.99, 5.20, "Temu", None, "Hyper-evaporative towels stay cold for hours. For sports and yard work.", "cooling_towel", "33x12 inches each. Activate with water. Stays cool up to 3 hours. Machine washable."),
            ("Cooling Gel Pillow Insert", "Cooling Accessories", 24.99, 36.99, 8.50, "Alibaba", None, "Gel-infused memory foam pillow insert for hot sleepers.", "cooling_towel", "Gel-infused memory foam. Standard size 24x16 inches. Removable washable cover."),
            ("Portable Ice Maker — 26 lbs/day", "Cooling Accessories", 149.99, 219.99, 62.00, "Alibaba", "Hot", "Countertop ice maker produces 26 lbs of bullet ice per day.", "ice_maker", "26 lbs/24 hours. 9 bullet ice cubes per cycle. 2.2L water tank. Self-cleaning function."),
            ("Car Windshield Sun Shade — Foldable", "Cooling Accessories", 14.99, 22.99, 4.80, "Temu", None, "Reflective accordion sun shade keeps car interior up to 40°F cooler.", "cooling_towel", "63x33 inches. Reflective silver coating. Accordion fold. Storage pouch included."),
            ("Insulated Lunch Cooler Bag — Dual Compartment", "Coolers", 21.99, 32.99, 7.00, "Amazon Wholesale", None, "Dual-compartment lunch bag with leak-proof liner and front pocket.", "cooler", "Holds 12 cans. Dual compartments. Leak-proof PEVA liner. Adjustable shoulder strap."),
            ("Window AC Side Panel Kit — Universal", "Air Conditioning", 27.99, 39.99, 9.50, "Temu", None, "Extendable accordion side panels seal window gaps for AC units.", "ac_unit", "Extends 9–18 inches. Fits most window AC units. Weather-resistant resin."),
            ("Bed Cooling Fan System — Quiet Breeze", "Cooling Accessories", 79.99, 119.99, 28.00, "Alibaba", "New", "Under-sheet fan system circulates cool air for hot sleepers.", "cooling_towel", "Dual quiet fans. Adjustable airflow. Fits queen and king beds. Under 35dB."),
            ("Insulated Water Jug — 1 Gallon", "Coolers", 34.99, 49.99, 12.00, "Amazon Wholesale", None, "Double-wall insulated jug keeps drinks cold 24+ hours. Leak-proof spigot.", "cooler_box", "1-gallon capacity. Stainless interior. Leak-proof spigot. Carry handle."),
            ("Outdoor Misting Fan — Patio 24 Inch", "Personal Fans", 74.99, 109.99, 28.50, "Alibaba", "Hot", "Oscillating misting fan cools patios, decks, and outdoor dining areas.", "tower_fan", "24-inch blade. Built-in misting ring. 3 speeds. Hose connection included."),
            ("Cooling Gel Sleep Mask — Reusable", "Cooling Accessories", 14.99, 21.99, 4.20, "Temu", None, "Gel-filled sleep mask soothes eyes and aids sleep on hot nights.", "cooling_towel", "Refrigerate 20 min for cooling. Soft plush backing. Adjustable elastic strap."),
        ]
    },
    "site4-pawnest": {
        "store": {"name": "PawNest", "tagline": "Summer Comfort for Your Best Friend", "logoHtml": "Paw<span>Nest</span>",
                  "description": "Trending pet summer care — cooling vests, mats, hydration, and outdoor safety gear.",
                  "email": "pets@pawnest.com", "phone": "1-800-PAWNEST", "slug": "pawnest"},
        "theme": {"primary": "#e76f51", "primaryDark": "#264653", "accent": "#f4a261"},
        "hero": {"title": "Keep Your Pet Cool & Happy", "subtitle": "Vet-recommended cooling gear and summer safety products for dogs and cats.",
                 "badges": ["Pet-Safe Materials", "Non-Toxic Fabrics", "14-Day Returns"]},
        "trust": [{"icon": "🐕", "text": "Dogs & Cats"}, {"icon": "🌡️", "text": "Heat Protection"}, {"icon": "💧", "text": "Hydration"}, {"icon": "⭐", "text": "4.9★ Rating"}],
        "about": {"title": "The #1 Trending Pet Niche of 2026", "paragraphs": ["PawNest focuses on summer heat protection — the fastest-growing pet category.", "Non-toxic, breathable materials sourced from verified pet product suppliers."],
                  "features": [{"icon": "❄️", "text": "Instant cooling"}, {"icon": "🐾", "text": "All breed sizes"}, {"icon": "🚗", "text": "Travel-ready"}, {"icon": "♻️", "text": "Machine washable"}]},
        "products": [
            ("Dog Cooling Vest — Evaporative Mesh", "Cooling Gear", 34.99, 49.99, 7.49, "Alibaba", "Trending", "Soak, wring, wear — instant cooling 2–4 hours. Sizes XS–XXL.", "dog", "Evaporative polymer fabric. Soak 2 min, wring, wear. Sizes XS through XXL. Reflective trim."),
            ("Self-Cooling Pet Mat — Gel Insert", "Cooling Gear", 29.99, 44.99, 9.20, "Temu", "Best Seller", "Pressure-activated gel mat. No refrigeration. Sizes S, M, L, XL.", "dog_bed", "Pressure-activated gel. Self-recharging in 20 min. S: 20x16, M: 27x20, L: 35x24, XL: 43x27 inches."),
            ("Cooling Bandana 3-Pack for Dogs", "Cooling Gear", 18.99, 27.99, 6.00, "Temu", None, "Reusable polymer crystal bandanas stay cool for hours.", "dog_outdoor", "Polymer crystal cooling insert. Adjustable snap closure. One size fits most. 3 colors."),
            ("Cat Cooling Mat — Pressure Activated", "Cooling Gear", 24.99, 36.99, 8.00, "Alibaba", None, "Slim gel mat for window sills and cat beds. Self-recharging.", "cat", "Slim 0.5-inch profile. Fits window sills. Self-cooling gel. 24x16 inches."),
            ("Portable Pet Water Bottle with Bowl", "Hydration", 16.99, 24.99, 5.40, "Alibaba", None, "One-hand squeeze dispenser with fold-out bowl. 12 oz leak-proof.", "dog_water", "12 oz capacity. One-hand operation. Fold-out drinking tray. Leak-proof lock."),
            ("Automatic Pet Fountain — 2.5L", "Hydration", 32.99, 47.99, 12.50, "Amazon Wholesale", None, "Circulating filtered water. Ultra-quiet pump, 3 flow modes.", "pet_fountain", "2.5L capacity. Triple filtration. 3 flow modes. Ultra-quiet pump under 40dB."),
            ("Collapsible Travel Water Bowl — 2 Pack", "Hydration", 11.99, 17.99, 3.80, "Temu", None, "Silicone collapsible bowls with carabiner clip. Dishwasher safe.", "dog_water", "Silicone. Collapses to 0.5 inches. Carabiner clip. Dishwasher safe. 2-pack."),
            ("Elevated Outdoor Pet Bed — Mesh", "Outdoor Comfort", 44.99, 64.99, 17.50, "Alibaba", None, "Raised breathable cot keeps pets off hot ground. Holds 100 lbs.", "dog_bed", "Elevated mesh cot. Holds up to 100 lbs. No-tool assembly. 30x22x8 inches."),
            ("Pet Paw Protection Boots — Heat Resistant", "Outdoor Comfort", 22.99, 32.99, 7.80, "Temu", None, "Silicone booties protect paws from hot pavement. Set of 4.", "pet_boots", "Heat-resistant silicone. Reflective straps. Set of 4. Sizes S–XL."),
            ("Pet Cooling Collar — Rechargeable", "Cooling Gear", 19.99, 29.99, 6.50, "Alibaba", "New", "USB rechargeable cooling collar with adjustable temperature.", "dog", "Rechargeable cooling plate. 3 temperature levels. Adjustable nylon collar. 4-hour runtime."),
            ("Car Seat Cooling Cover for Pets", "Travel", 36.99, 52.99, 13.00, "Alibaba", None, "Quilted cooling seat cover with harness openings. Machine washable.", "pet_car", "Quilted cooling fabric. Harness slot openings. Universal back seat fit. Machine washable."),
            ("Pet Travel Carrier — Airline Approved", "Travel", 49.99, 74.99, 18.00, "Amazon Wholesale", None, "Soft-sided airline-approved carrier with mesh ventilation panels.", "pet_car", "17x11x9.5 inches. Airline approved. Mesh panels. Shoulder strap and luggage sleeve."),
            ("Pet Sunscreen Wipes — 50 Count", "Sun Protection", 14.99, 21.99, 4.80, "Temu", None, "Pet-safe SPF 15 wipes for nose, ears, and exposed skin.", "dog", "SPF 15 pet-safe formula. 50 wipes. Fragrance-free. For nose, ears, belly."),
            ("Pet Life Jacket — Reflective XS–XL", "Outdoor Comfort", 27.99, 39.99, 9.50, "Alibaba", None, "Reflective life vest with rescue handle. Sizes XS through XL.", "dog_outdoor", "Reflective strips. Top rescue handle. Adjustable straps. Sizes XS–XL."),
            ("Slow Feeder Bowl — Anti-Gulp", "Hydration", 13.99, 19.99, 4.50, "Temu", None, "Maze-pattern bowl slows eating to prevent bloat. Non-slip base.", "pet_fountain", "Maze pattern slows eating. Non-slip rubber base. BPA-free. 2-cup capacity."),
            ("Pet Grooming Gloves — Deshedding", "Grooming", 14.99, 21.99, 4.80, "Temu", None, "Silicone grooming gloves remove loose fur while petting.", "dog", "Silicone tips. One size fits all. Works wet or dry. Machine washable."),
            ("Pet First Aid Kit — 40 Pieces", "Safety", 24.99, 36.99, 8.50, "Amazon Wholesale", None, "Compact first aid kit with bandages, antiseptic, and tick remover.", "dog_outdoor", "40 pieces. Bandages, antiseptic wipes, tick remover, gauze. Compact case."),
            ("Dog Cooling Bandana — Patriotic 2-Pack", "Cooling Gear", 15.99, 22.99, 5.00, "Temu", None, "Cooling insert bandanas in patriotic prints. Machine washable.", "dog_outdoor", "Cooling polymer insert. Machine washable. Adjustable tie. 2-pack."),
            ("Dog Splash Pad Pool — Foldable 63 Inch", "Outdoor Comfort", 32.99, 47.99, 11.00, "Alibaba", "Trending", "Sprinkler splash pad folds flat for backyard summer fun.", "dog_outdoor", "63-inch diameter. Built-in sprinkler ring. 0.5mm PVC. Folds to compact disc."),
            ("Pet Cooling Mat for Crate — Medium", "Cooling Gear", 26.99, 38.99, 8.00, "Temu", None, "Crate-sized cooling mat fits standard 30-inch dog crates.", "dog_bed", "Fits 30-inch crates. Non-slip bottom. Pressure-activated gel. 24x18 inches."),
            ("Cat Window Perch with Cooling Pad", "Outdoor Comfort", 39.99, 57.99, 14.00, "Alibaba", "New", "Suction-cup window perch with removable cooling insert for cats.", "cat", "Holds up to 35 lbs. Strong suction cups. Removable cooling pad. Machine washable cover."),
            ("Automatic Pet Treat Dispenser — WiFi", "Travel", 44.99, 64.99, 16.00, "Amazon Wholesale", None, "App-controlled treat dispenser with 1080p camera and 2-way audio.", "pet_car", "1080p HD camera. 2-way audio. App scheduling. 1.5L treat hopper."),
            ("Pet Hair Remover Lint Roller — Reusable", "Grooming", 12.99, 18.99, 3.50, "Temu", None, "Self-cleaning reusable roller removes pet hair from furniture and clothes.", "dog", "Self-cleaning base. Reusable gel roller. No refills needed. Travel-size."),
        ]
    },
    "site5-summit-trail": {
        "store": {"name": "Summit Trail Co.", "tagline": "Adventure-Ready Outdoor Gear", "logoHtml": "Summit <span>Trail</span>",
                  "description": "Trending camping and outdoor gear — portable showers, LED lanterns, privacy tents, and bug protection.",
                  "email": "adventure@summittrail.co", "phone": "1-800-SUMMIT", "slug": "summit-trail"},
        "theme": {"primary": "#588157", "primaryDark": "#3a5a40", "accent": "#dad7cd"},
        "hero": {"title": "Gear Up. Get Out There.", "subtitle": "Camping, hiking, and outdoor adventure equipment at expedition-ready prices.",
                 "badges": ["50%+ Category Growth", "Lightweight & Durable", "14-Day Returns"]},
        "trust": [{"icon": "⛺", "text": "Camping Essentials"}, {"icon": "🦟", "text": "Bug Protection"}, {"icon": "💡", "text": "Emergency Light"}, {"icon": "🚿", "text": "Portable Hygiene"}],
        "about": {"title": "Ride the Outdoor Boom", "paragraphs": ["Summit Trail stocks outdoor products with 50%+ search growth in 2026.", "Verified suppliers with U.S. warehouse options for 7–14 day delivery."],
                  "features": [{"icon": "🏕️", "text": "Camping & van life"}, {"icon": "🥾", "text": "Hiking essentials"}, {"icon": "🎣", "text": "Water sports"}, {"icon": "🌲", "text": "Leave No Trace"}]},
        "products": [
            ("Portable Camping Shower — Battery Powered", "Camping", 59.99, 89.99, 14.77, "Alibaba", "Trending", "Rechargeable pump delivers steady shower from any water source. 60-min runtime.", "camping", "2200mAh rechargeable. 60-min runtime. 6.5 ft hose. Suction cup and hook mount."),
            ("Pop-Up Privacy Tent — Changing Room", "Camping", 59.99, 84.99, 14.89, "Alibaba", "50% Growth", "Instant privacy shelter. 6.5 ft tall with carry bag.", "tent", "47x47x78 inches. Instant pop-up. Carry bag included. Ground stakes."),
            ("Ultralight 2-Person Camping Tent", "Camping", 89.99, 139.99, 35.00, "Alibaba", "Hot Deal", "3.5 lb backpacking tent with rainfly and two vestibules.", "tent", "3.5 lbs packed. 2-person. Full rainfly. Aluminum poles. Two vestibules."),
            ("Foldable Camping Cot — Off-Ground Sleep", "Camping", 64.99, 94.99, 24.00, "Temu", None, "Aluminum frame cot supports 300 lbs. Folds to briefcase size.", "camping", "300 lb capacity. 75x26 inches. Aluminum frame. Folds to 36x16x6 inches."),
            ("Mosquito Repeller Fan — Chemical-Free", "Bug Protection", 24.99, 36.99, 3.73, "Temu", "Best Seller", "Holographic blade fan deters mosquitoes without chemicals.", "mosquito", "Chemical-free. USB or 2xAA battery. 360° holographic blades. Quiet operation."),
            ("Insect Bite Venom Extractor Kit", "Bug Protection", 14.99, 22.99, 2.89, "Alibaba", None, "Suction tool removes venom from bites and stings.", "mosquito", "Dual-size suction cups. Compact for first-aid kits. Reusable after cleaning."),
            ("DEET-Free Insect Repellent Spray — 4oz", "Bug Protection", 12.99, 18.99, 3.50, "Amazon Wholesale", None, "Picaridin-based repellent effective up to 8 hours. Family safe.", "mosquito", "20% picaridin. 8-hour protection. DEET-free. 4 oz spray bottle."),
            ("Rechargeable LED Camping Lantern", "Lighting", 29.99, 44.99, 9.50, "Amazon Wholesale", None, "1000-lumen lantern with 4 modes and power bank function.", "lantern", "1000 lumens max. 4 light modes. 5200mAh power bank. IPX4 water resistant."),
            ("Headlamp — 350 Lumen Rechargeable", "Lighting", 19.99, 29.99, 6.50, "Temu", None, "350-lumen headlamp with red night mode and 45-hour runtime.", "lantern", "350 lumens. Red night mode. 45-hour low runtime. USB rechargeable. IPX4."),
            ("Insulated Hiking Backpack — 50L", "Hiking", 54.99, 79.99, 19.50, "Alibaba", None, "Waterproof hiking pack with rain cover and hydration sleeve.", "backpack", "50L capacity. Rain cover included. Hydration bladder sleeve. Padded hip belt."),
            ("Trekking Poles — Carbon Fiber Pair", "Hiking", 39.99, 59.99, 14.00, "Alibaba", None, "Carbon fiber trekking poles with cork grips and quick-lock.", "hiking", "Carbon fiber shafts. Cork grips. Quick-lock adjustment. Includes tips and baskets."),
            ("Portable Camping Stove — Dual Burner", "Cooking", 49.99, 74.99, 17.00, "Amazon Wholesale", "New", "Propane dual-burner with wind guards. 20,000 BTU output.", "camp_stove", "20,000 BTU total. Dual burners. Wind guards. Fits 1-lb propane canisters."),
            ("Camping Cookware Set — 10 Piece", "Cooking", 34.99, 49.99, 11.50, "Temu", None, "Non-stick aluminum pots, pans, and utensils with mesh carry bag.", "camp_stove", "10 pieces. Non-stick aluminum. Folding handles. Mesh storage bag."),
            ("Emergency Survival Kit — 72 Hour", "Safety", 39.99, 59.99, 13.50, "Temu", None, "Compact kit with food bars, water, first aid, and emergency blanket.", "survival", "Food bars, water pouches, first aid, flashlight, whistle, emergency blanket."),
            ("Waterproof Dry Bag Set — 3 Pack", "Hiking", 22.99, 34.99, 7.50, "Alibaba", None, "Roll-top dry bags in 3L, 5L, and 10L sizes. IPX7 waterproof.", "backpack", "3L, 5L, 10L sizes. Roll-top closure. IPX7 waterproof. Shoulder straps."),
            ("Camping Hammock with Mosquito Net", "Camping", 44.99, 64.99, 15.00, "Temu", None, "Parachute nylon hammock with integrated bug net. 500 lb capacity.", "camping", "Parachute nylon. 500 lb capacity. Integrated mosquito net. Tree straps included."),
            ("Portable Power Station — 200Wh", "Power", 129.99, 189.99, 52.00, "Alibaba", "New", "200Wh lithium power station with AC, USB, and DC outputs.", "survival", "200Wh capacity. AC outlet, 2x USB-A, USB-C, DC port. Solar chargeable."),
            ("Foldable Camp Chair — Heavy Duty", "Camping", 36.99, 54.99, 12.00, "Temu", None, "600D Oxford camp chair supports 330 lbs. Cup holder and carry bag.", "camping", "600D Oxford fabric. 330 lb capacity. Cup holder. Carry bag. 19x19x33 inches."),
            ("Sleeping Bag — 3 Season Mummy Style", "Camping", 54.99, 79.99, 19.00, "Alibaba", "New", "Lightweight mummy sleeping bag rated to 32°F for spring through fall.", "camping", "32°F comfort rating. 2.8 lbs. Compression sack included. Water-resistant shell."),
            ("Portable Water Filter Straw — Survival", "Safety", 16.99, 24.99, 4.50, "Temu", None, "Personal water filter straw removes 99.9% bacteria from outdoor water sources.", "survival", "Filters 1,500 liters. Removes 99.9% bacteria. 0.1-micron membrane. 2 oz weight."),
            ("Campfire Grill Grate — Folding Steel", "Cooking", 29.99, 44.99, 9.80, "Alibaba", None, "Folding steel grill grate fits over campfires and fire pits.", "camp_stove", "17x11 inch cooking surface. Folding legs. Chrome-plated steel. 2.2 lbs."),
            ("Waterproof Trekking Gaiters — Pair", "Hiking", 24.99, 36.99, 7.50, "Temu", None, "Breathable gaiters keep mud, snow, and debris out of boots on trails.", "hiking", "600D nylon. Waterproof PU coating. Adjustable top strap. One size fits most."),
            ("Solar Camp Shower Bag — 5 Gallon", "Camping", 19.99, 29.99, 5.20, "Temu", "Best Value", "Solar-heated PVC shower bag warms water in 3 hours of direct sun.", "camping", "5-gallon capacity. Solar heating panel. On/off valve. Hang rope included."),
        ]
    },
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
        "shippingDays": "7-14 business days",
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
        }
        path = os.path.join(ROOT, folder, "products.json")
        with open(path, "w") as f:
            json.dump(out, f, indent=2)
        print(f"Wrote {len(out['products'])} products to {folder}")


if __name__ == "__main__":
    main()