import asyncio
import json
import random
from datetime import datetime

# Placeholder for Phase 0: Data Acquisition
# This script will eventually use Playwright or API calls to fetch data

def mock_crawl():
    """Generates mock data for testing the pipeline"""
    sources = ["Facebook Group A", "Zalo Group B", "TikTok User C"]
    templates = [
        "Cần xe đi {dest} gấp, hàng {commodity}",
        "Tìm xe {truck_type} bốc hàng từ {origin} đi {dest}",
        "Kẹt xe ở {location} quá các bác ơi",
    ]
    locations = ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Cần Thơ", "Lạng Sơn", "Quảng Trị", "Nam Định"]
    commodities = ["lúa gạo", "thanh long", "vải thiều", "phân bón"]
    
    data = []
    for _ in range(10):
        origin = random.choice(locations)
        dest = random.choice(locations)
        text = random.choice(templates).format(
            origin=origin,
            dest=dest,
            location=origin,
            truck_type="8 tấn",
            commodity=random.choice(commodities)
        )
        
        entry = {
            "source": random.choice(sources),
            "timestamp": datetime.now().isoformat(),
            "content": text,
            "url": "https://example.com/post/123"
        }
        data.append(entry)
    
    return data

def main():
    print("Starting Crawler Job...")
    # Real logic: logic to crawl FB/Zalo
    # Mock logic:
    data = mock_crawl()
    
    output_file = "raw_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Crawled {len(data)} items. Saved to {output_file}")

if __name__ == "__main__":
    main()
