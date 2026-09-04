import re
import uuid
from typing import Dict, Any, List

# Catalog with distinct Categories and Brands
CATALOG: List[Dict[str, Any]] = [
    # ============ SMARTPHONES (Budget: Under 10k) ============
    {"id": "p1", "name": "POCO C65 (4GB RAM, 128GB)", "category": "smartphone", "brand": "poco", "price": 7499.0, "rating": 4.2},
    {"id": "p2", "name": "Samsung Galaxy M14 5G (4GB RAM, 128GB)", "category": "smartphone", "brand": "samsung", "price": 9490.0, "rating": 4.1},
    {"id": "p3", "name": "Redmi 13C 5G (4GB RAM, 128GB)", "category": "smartphone", "brand": "redmi", "price": 9999.0, "rating": 4.3},
    {"id": "p3a", "name": "Realme Narzo 70 (6GB RAM, 128GB)", "category": "smartphone", "brand": "realme", "price": 8999.0, "rating": 4.1},
    {"id": "p3b", "name": "Itel A70 (4GB RAM, 64GB)", "category": "smartphone", "brand": "itel", "price": 5499.0, "rating": 3.9},
    
    # ============ SMARTPHONES (Mid-Range: 10k - 25k) ============
    {"id": "p4", "name": "Samsung Galaxy M34 5G (8GB RAM, 128GB)", "category": "smartphone", "brand": "samsung", "price": 18999.0, "rating": 4.3},
    {"id": "p5", "name": "iQOO Z9 5G (8GB RAM, 128GB)", "category": "smartphone", "brand": "iqoo", "price": 19999.0, "rating": 4.4},
    {"id": "p6", "name": "OnePlus Nord CE 4 Lite 5G", "category": "smartphone", "brand": "oneplus", "price": 19999.0, "rating": 4.4},
    {"id": "p7", "name": "Redmi Note 13 Pro 5G", "category": "smartphone", "brand": "redmi", "price": 23999.0, "rating": 4.5},
    {"id": "p8", "name": "Realme 12 Pro+ 5G", "category": "smartphone", "brand": "realme", "price": 24999.0, "rating": 4.6},
    {"id": "p8a", "name": "Vivo Y100 (8GB RAM, 256GB)", "category": "smartphone", "brand": "vivo", "price": 22999.0, "rating": 4.2},
    {"id": "p8b", "name": "Oppo A78 5G (8GB RAM, 128GB)", "category": "smartphone", "brand": "oppo", "price": 21999.0, "rating": 4.1},
    
    # ============ SMARTPHONES (Premium: 25k - 50k) ============
    {"id": "p9", "name": "Samsung Galaxy S23 FE 5G", "category": "smartphone", "brand": "samsung", "price": 38999.0, "rating": 4.5},
    {"id": "p10", "name": "OnePlus 12R (8GB RAM, 128GB)", "category": "smartphone", "brand": "oneplus", "price": 39999.0, "rating": 4.6},
    {"id": "p11", "name": "iPhone 14 (128GB)", "category": "smartphone", "brand": "apple", "price": 47999.0, "rating": 4.7},
    {"id": "p11a", "name": "Google Pixel 7a", "category": "smartphone", "brand": "google", "price": 43999.0, "rating": 4.4},
    {"id": "p11b", "name": "Motorola Edge 50 Pro", "category": "smartphone", "brand": "motorola", "price": 44999.0, "rating": 4.3},
    
    # ============ SMARTPHONES (Flagship: 50k+) ============
    {"id": "p12", "name": "iPhone 15 Pro (256GB)", "category": "smartphone", "brand": "apple", "price": 99999.0, "rating": 4.9},
    {"id": "p13", "name": "Samsung Galaxy S24 Ultra", "category": "smartphone", "brand": "samsung", "price": 124999.0, "rating": 4.8},
    {"id": "p14", "name": "OnePlus 12 (12GB RAM, 256GB)", "category": "smartphone", "brand": "oneplus", "price": 64999.0, "rating": 4.7},

    # ============ LAPTOPS (Budget: 30k - 60k) ============
    {"id": "l1", "name": "Lenovo IdeaPad Slim 3", "category": "laptop", "brand": "lenovo", "price": 45000.0, "rating": 4.2},
    {"id": "l1a", "name": "HP Pavilion 15 (Intel Core i5)", "category": "laptop", "brand": "hp", "price": 55000.0, "rating": 4.1},
    {"id": "l1b", "name": "Dell Inspiron 15 (AMD Ryzen 5)", "category": "laptop", "brand": "dell", "price": 50000.0, "rating": 4.3},
    
    # ============ LAPTOPS (Mid-Range: 60k - 100k) ============
    {"id": "l2", "name": "HP Pavilion 15 (Intel i7)", "category": "laptop", "brand": "hp", "price": 62000.0, "rating": 4.4},
    {"id": "l2a", "name": "ASUS VivoBook 15", "category": "laptop", "brand": "asus", "price": 65000.0, "rating": 4.5},
    {"id": "l2b", "name": "Lenovo ThinkBook 15", "category": "laptop", "brand": "lenovo", "price": 75000.0, "rating": 4.6},
    
    # ============ LAPTOPS (Premium: 100k+) ============
    {"id": "l3", "name": "Apple MacBook Air M2 (256GB)", "category": "laptop", "brand": "apple", "price": 94900.0, "rating": 4.8},
    {"id": "l3a", "name": "Apple MacBook Pro 14 M3", "category": "laptop", "brand": "apple", "price": 149999.0, "rating": 4.9},
    {"id": "l3b", "name": "Dell XPS 13 Plus", "category": "laptop", "brand": "dell", "price": 119999.0, "rating": 4.7},

    # ============ TABLETS ============
    {"id": "t1", "name": "iPad (10th Generation)", "category": "tablet", "brand": "apple", "price": 34999.0, "rating": 4.5},
    {"id": "t2", "name": "Samsung Galaxy Tab S9 FE", "category": "tablet", "brand": "samsung", "price": 28999.0, "rating": 4.2},
    {"id": "t3", "name": "OnePlus Pad", "category": "tablet", "brand": "oneplus", "price": 39999.0, "rating": 4.4},
    {"id": "t4", "name": "Redmi Pad SE", "category": "tablet", "brand": "redmi", "price": 16999.0, "rating": 4.1},

    # ============ TVs (32-inch) ============
    {"id": "tv1", "name": "Samsung 32\" M14 HD Ready Smart TV", "category": "tv", "brand": "samsung", "price": 13990.0, "rating": 4.1},
    {"id": "tv2", "name": "LG 32\" HD Ready Smart TV", "category": "tv", "brand": "lg", "price": 13490.0, "rating": 4.3},
    {"id": "tv3", "name": "Mi 32\" HD Ready Smart TV", "category": "tv", "brand": "mi", "price": 13999.0, "rating": 4.2},
    {"id": "tv4", "name": "OnePlus 32\" HD Ready Smart TV", "category": "tv", "brand": "oneplus", "price": 14999.0, "rating": 4.2},

    # ============ TVs (43-inch) ============
    {"id": "tv5", "name": "Samsung 43\" Full HD Smart TV", "category": "tv", "brand": "samsung", "price": 31999.0, "rating": 4.3},
    {"id": "tv6", "name": "LG 43\" Full HD Smart TV", "category": "tv", "brand": "lg", "price": 33999.0, "rating": 4.4},
    {"id": "tv7", "name": "OnePlus 50\" 4K Smart TV", "category": "tv", "brand": "oneplus", "price": 32999.0, "rating": 4.2},
    {"id": "tv8", "name": "Mi 50\" 4K Smart TV", "category": "tv", "brand": "mi", "price": 29999.0, "rating": 4.1},

    # ============ TVs (55-inch & 65-inch) ============
    {"id": "tv9", "name": "Samsung 55\" 4K Ultra HD Smart TV", "category": "tv", "brand": "samsung", "price": 49999.0, "rating": 4.5},
    {"id": "tv10", "name": "LG 55\" 4K OLED Smart TV", "category": "tv", "brand": "lg", "price": 89999.0, "rating": 4.7},
    {"id": "tv11", "name": "Sony 65\" 4K Bravia Smart TV", "category": "tv", "brand": "sony", "price": 119999.0, "rating": 4.8},

    # ============ HDMI CABLES (For TVs) ============
    {"id": "hdmi1", "name": "AmazonBasics HDMI Cable 3-Foot (1.2m)", "category": "accessory", "brand": "generic", "price": 219.0, "rating": 4.4},
    {"id": "hdmi2", "name": "Tizum High Speed HDMI Cable 1.5m", "category": "accessory", "brand": "generic", "price": 199.0, "rating": 4.2},
    {"id": "hdmi3", "name": "boAt HDMI 2.0 Cable 4K 60Hz 2m", "category": "accessory", "brand": "boat", "price": 399.0, "rating": 4.5},
    
    # ============ CHARGING CABLES & ADAPTERS ============
    {"id": "a1", "name": "Type-C Fast Charging Cable (1m)", "category": "accessory", "brand": "generic", "price": 299.0, "rating": 4.4},
    {"id": "a1a", "name": "Micro USB Charging Cable (1m)", "category": "accessory", "brand": "generic", "price": 199.0, "rating": 4.2},
    {"id": "a2", "name": "Apple MFi Certified Lightning Cable", "category": "accessory", "brand": "apple", "price": 399.0, "rating": 4.5},
    {"id": "a3", "name": "USB-C to USB-C Cable (2m)", "category": "accessory", "brand": "generic", "price": 499.0, "rating": 4.6},
    {"id": "a4", "name": "Samsung Original 25W Type-C Adapter", "category": "accessory", "brand": "samsung", "price": 1299.0, "rating": 4.6},
    {"id": "a5", "name": "Anker PowerPort 65W Adapter", "category": "accessory", "brand": "anker", "price": 2499.0, "rating": 4.7},
    {"id": "a6", "name": "OnePlus 100W SuperVOOC Charger", "category": "accessory", "brand": "oneplus", "price": 3999.0, "rating": 4.8},

    # ============ SCREEN PROTECTORS & CASES ============
    {"id": "a7", "name": "Spigen Tempered Glass Screen Protector", "category": "accessory", "brand": "generic", "price": 699.0, "rating": 4.5},
    {"id": "a8", "name": "Nillkin Matte Screen Protector", "category": "accessory", "brand": "generic", "price": 599.0, "rating": 4.4},
    {"id": "a9", "name": "Spigen Rugged Armor Case", "category": "accessory", "brand": "generic", "price": 899.0, "rating": 4.6},
    {"id": "a10", "name": "OtterBox Defender Series Case", "category": "accessory", "brand": "generic", "price": 1499.0, "rating": 4.7},
    {"id": "a11", "name": "Ringke Fusion Case", "category": "accessory", "brand": "generic", "price": 599.0, "rating": 4.3},

    # ============ AUDIO DEVICES (Headphones) ============
    {"id": "au1", "name": "boAt Rockerz 450 Wireless Headphones", "category": "audio", "brand": "boat", "price": 2499.0, "rating": 4.1},
    {"id": "au2", "name": "Sony WH-CH720 Wireless Headphones", "category": "audio", "brand": "sony", "price": 7990.0, "rating": 4.5},
    {"id": "au3", "name": "JBL Tune 770NC Noise Cancelling", "category": "audio", "brand": "jbl", "price": 12999.0, "rating": 4.6},
    {"id": "au4", "name": "Apple AirPods Pro (2nd Gen)", "category": "audio", "brand": "apple", "price": 18999.0, "rating": 4.8},
    {"id": "au5", "name": "Sennheiser Momentum 4 Wireless", "category": "audio", "brand": "sennheiser", "price": 24999.0, "rating": 4.7},

    # ============ AUDIO DEVICES (Earbuds) ============
    {"id": "au6", "name": "OnePlus Nord Buds 2", "category": "audio", "brand": "oneplus", "price": 2999.0, "rating": 4.2},
    {"id": "au7", "name": "Samsung Galaxy Buds2", "category": "audio", "brand": "samsung", "price": 4999.0, "rating": 4.4},
    {"id": "au8", "name": "Nothing Ear Buds", "category": "audio", "brand": "nothing", "price": 5999.0, "rating": 4.3},
    {"id": "au9", "name": "Apple AirPods (3rd Gen)", "category": "audio", "brand": "apple", "price": 16999.0, "rating": 4.6},
    
    # ============ AUDIO DEVICES (Speakers) ============
    {"id": "au10", "name": "boAt Stone 650 Bluetooth Speaker", "category": "audio", "brand": "boat", "price": 2499.0, "rating": 4.0},
    {"id": "au11", "name": "JBL Go 3 Portable Speaker", "category": "audio", "brand": "jbl", "price": 3999.0, "rating": 4.4},
    {"id": "au12", "name": "Sony SRS-XE300 Portable Speaker", "category": "audio", "brand": "sony", "price": 16990.0, "rating": 4.6},
    {"id": "au13", "name": "Bose SoundLink Max", "category": "audio", "brand": "bose", "price": 32999.0, "rating": 4.8},

    # ============ WEARABLES (Smartwatches) ============
    {"id": "w1", "name": "Noise ColorFit Ultra Smartwatch", "category": "wearable", "brand": "noise", "price": 4999.0, "rating": 4.1},
    {"id": "w2", "name": "Samsung Galaxy Watch5 (40mm)", "category": "wearable", "brand": "samsung", "price": 24999.0, "rating": 4.5},
    {"id": "w3", "name": "Apple Watch Series 8", "category": "wearable", "brand": "apple", "price": 41900.0, "rating": 4.7},
    {"id": "w4", "name": "Garmin Fenix 6 Pro", "category": "wearable", "brand": "garmin", "price": 49999.0, "rating": 4.8},

    # ============ WEARABLES (Fitness Bands) ============
    {"id": "w5", "name": "Mi Band 7", "category": "wearable", "brand": "mi", "price": 2999.0, "rating": 4.2},
    {"id": "w6", "name": "Fitbit Inspire 3", "category": "wearable", "brand": "fitbit", "price": 9999.0, "rating": 4.4},
    {"id": "w7", "name": "Garmin Vivosmart 5", "category": "wearable", "brand": "garmin", "price": 15999.0, "rating": 4.5},

    # ============ STORAGE DEVICES (USB Pen Drives) ============
    {"id": "st1", "name": "SanDisk Cruzer Blade 32GB", "category": "storage", "brand": "sandisk", "price": 499.0, "rating": 4.2},
    {"id": "st2", "name": "Kingston DataTraveler 70 64GB", "category": "storage", "brand": "kingston", "price": 799.0, "rating": 4.3},
    {"id": "st3", "name": "SanDisk Extreme 128GB", "category": "storage", "brand": "sandisk", "price": 1999.0, "rating": 4.5},
    {"id": "st4", "name": "Samsung Bar Plus 256GB", "category": "storage", "brand": "samsung", "price": 3999.0, "rating": 4.6},

    # ============ STORAGE DEVICES (External HDD) ============
    {"id": "st5", "name": "Seagate Expansion 1TB", "category": "storage", "brand": "seagate", "price": 4999.0, "rating": 4.3},
    {"id": "st6", "name": "WD My Passport 2TB", "category": "storage", "brand": "wd", "price": 7999.0, "rating": 4.5},
    {"id": "st7", "name": "Seagate Backup Plus 4TB", "category": "storage", "brand": "seagate", "price": 12999.0, "rating": 4.4},

    # ============ STORAGE DEVICES (SSD) ============
    {"id": "st8", "name": "Samsung 870 EVO 500GB SSD", "category": "storage", "brand": "samsung", "price": 4499.0, "rating": 4.6},
    {"id": "st9", "name": "WD Green 1TB SSD", "category": "storage", "brand": "wd", "price": 6999.0, "rating": 4.4},
    {"id": "st10", "name": "Samsung 980 Pro 1TB NVMe", "category": "storage", "brand": "samsung", "price": 11999.0, "rating": 4.7},

    # ============ NETWORKING DEVICES ============
    {"id": "net1", "name": "TP-Link TL-WN725N WiFi Adapter", "category": "networking", "brand": "tplink", "price": 499.0, "rating": 4.2},
    {"id": "net2", "name": "TP-Link Archer C6 WiFi Router", "category": "networking", "brand": "tplink", "price": 3999.0, "rating": 4.4},
    {"id": "net3", "name": "Asus RT-AX88U WiFi 6 Router", "category": "networking", "brand": "asus", "price": 18999.0, "rating": 4.6},
    {"id": "net4", "name": "Netgear Nighthawk AXE300 WiFi 6E", "category": "networking", "brand": "netgear", "price": 24999.0, "rating": 4.7},

    # ============ SMART HOME DEVICES ============
    {"id": "sh1", "name": "Google Nest Mini", "category": "smart_home", "brand": "google", "price": 4999.0, "rating": 4.3},
    {"id": "sh2", "name": "Amazon Echo Dot (5th Gen)", "category": "smart_home", "brand": "amazon", "price": 4499.0, "rating": 4.2},
    {"id": "sh3", "name": "Google Nest Hub Max", "category": "smart_home", "brand": "google", "price": 12999.0, "rating": 4.5},
    {"id": "sh4", "name": "Amazon Echo Studio", "category": "smart_home", "brand": "amazon", "price": 19999.0, "rating": 4.6},

    # ============ CAMERAS ============
    {"id": "cam1", "name": "GoPro Hero 11 Black", "category": "camera", "brand": "gopro", "price": 44999.0, "rating": 4.7},
    {"id": "cam2", "name": "DJI Osmo Action 4", "category": "camera", "brand": "dji", "price": 26999.0, "rating": 4.5},
    {"id": "cam3", "name": "Canon EOS M50 Mark II", "category": "camera", "brand": "canon", "price": 59999.0, "rating": 4.6},
    {"id": "cam4", "name": "Sony A6400", "category": "camera", "brand": "sony", "price": 69999.0, "rating": 4.8},
]

def parse_user_query(query: str) -> Dict[str, Any]:
    query_lower = query.lower()
    
    # Budget Extraction (e.g. 25k -> 25000, 10000 -> 10000)
    k_match = re.search(r'(\d+(?:\.\d+)?)\s*k\b', query_lower)
    if k_match:
        max_budget = float(k_match.group(1)) * 1000.0
    else:
        num_match = re.search(r'(?:₹|rs\.?|inr)?\s*(\d{4,7})', query_lower)
        max_budget = float(num_match.group(1)) if num_match else 25000.0

    # Detect Target Brand
    detected_brand = None
    known_brands = ["samsung", "apple", "iphone", "oneplus", "redmi", "realme", "poco", "iqoo", "lg", "sony", "mi", "hp", "lenovo", "dell", "asus", "acer", "boat", "nothing", "garmin", "fitbit", "noise"]
    for b in known_brands:
        if b in query_lower:
            detected_brand = "apple" if b == "iphone" else b
            break

    # Detect Target Category
    phone_terms = ["mobile", "mobiles", "phone", "phones", "smartphone", "smartphones"]
    laptop_terms = ["laptop", "laptops", "macbook", "notebook"]
    tv_terms = ["tv", "television", "smart tv", "hdmi", "4k tv", "oled", "ultra hd"]
    tablet_terms = ["tablet", "ipad"]
    audio_terms = ["headphone", "earbuds", "speaker", "earphone", "headset", "wireless"]
    
    if any(term in query_lower for term in tv_terms):
        primary_category = "tv"
    elif any(term in query_lower for term in tablet_terms):
        primary_category = "tablet"
    elif any(term in query_lower for term in audio_terms):
        primary_category = "audio"
    elif any(term in query_lower for term in laptop_terms):
        primary_category = "laptop"
    elif any(term in query_lower for term in phone_terms):
        primary_category = "smartphone"
    elif detected_brand in ["samsung", "apple", "oneplus", "redmi", "realme", "poco", "iqoo"]:
        # If only brand mentioned without category, default to smartphone
        primary_category = "smartphone"
    else:
        primary_category = "smartphone"

    return {
        "primary_category": primary_category,
        "target_brand": detected_brand,
        "max_budget": max_budget
    }

def cart_pilot_agent(query: str) -> Dict[str, Any]:
    parsed = parse_user_query(query)
    max_budget = parsed["max_budget"]
    primary_cat = parsed["primary_category"]
    target_brand = parsed["target_brand"]

    # 1. Filter Primary Devices under budget
    candidates = [
        item for item in CATALOG 
        if item["category"] == primary_cat and item["price"] <= max_budget
    ]

    # Filter by target brand if specified
    if target_brand:
        brand_candidates = [item for item in candidates if item["brand"] == target_brand]
        if brand_candidates:
            candidates = brand_candidates

    if not candidates:
        return {
            "status": "failed",
            "message": f"No {primary_cat} options found under ₹{max_budget:,.0f}.",
            "query": query
        }

    # Sort to pick the device that best maximizes budget utilization and rating
    candidates.sort(key=lambda x: (x["price"], x["rating"]), reverse=True)
    
    selected_items = []
    current_total = 0.0

    # Select Primary Item First
    main_item = candidates[0]
    selected_items.append(main_item)
    current_total += main_item["price"]

    # 2. Optionally Add Compatible Accessory if budget permits
    remaining_budget = max_budget - current_total
    
    # Recommend compatible accessories based on category
    compatible_accessories = {
        "tv": ["hdmi"],  # HDMI cables for TVs (prioritize HDMI)
        "smartphone": ["charger", "charging", "cable", "adapter", "screen", "protector", "case"],  # Phone chargers & protection
        "laptop": ["adapter", "charger", "cooling", "pad"],  # Laptop chargers
        "tablet": ["charger", "charging", "cable"],  # Tablet chargers
        "audio": ["cable", "adapter"],  # Audio cables/adapters
        "wearable": ["charger", "strap"],  # Wearable chargers
        "camera": ["cable", "card", "battery"],  # Camera accessories
        "storage": ["cable", "adapter"],  # Storage cables
        "networking": ["cable", "adapter"],  # Networking cables
        "smart_home": ["cable", "adapter"],  # Smart home accessories
    }
    
    if primary_cat in compatible_accessories and remaining_budget >= 199.0:
        search_keywords = compatible_accessories[primary_cat]
        accessories = [
            a for a in CATALOG 
            if a["category"] == "accessory" 
            and a["price"] <= remaining_budget
            and any(keyword in a["name"].lower() for keyword in search_keywords)
        ]

        # Prevent Apple accessories from pairing with Android devices
        if main_item["brand"] != "apple":
            accessories = [
                a for a in accessories 
                if a["brand"] != "apple" and "lightning" not in a["name"].lower()
            ]
        elif main_item["brand"] == "apple":
            # For Apple devices, prioritize Apple accessories but allow others
            apple_accs = [a for a in accessories if a["brand"] == "apple" or "mfi" in a["name"].lower()]
            if apple_accs:
                accessories = apple_accs

        if accessories:
            accessories.sort(key=lambda x: x["rating"], reverse=True)
            acc = accessories[0]
            selected_items.append(acc)
            current_total += acc["price"]

    categories_matched = list(set([item["category"] for item in selected_items]))
    reserve_token = f"rzp_agentic_reserve_{uuid.uuid4().hex[:12]}"

    return {
        "status": "success",
        "query": query,
        "parsed_intent": {
            "categories": categories_matched,
            "target_brand": target_brand or "any"
        },
        "selected_items": selected_items,
        "total_cost": current_total,
        "max_budget": max_budget,
        "reserve_token": reserve_token
    }