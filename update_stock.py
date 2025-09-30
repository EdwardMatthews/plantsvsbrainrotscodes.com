#!/usr/bin/env python3
"""
Plants vs Brainrots Stock Tracker Updater
Fetches stock data from API and updates stock.html
"""

import requests
from datetime import datetime, timezone
import sys
import re
from typing import Dict, List, Any
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for Python < 3.9
    from backports.zoneinfo import ZoneInfo

# Configuration
API_URL = "https://plantsvsbrainrots.com/api/latest-message"
STOCK_HTML_PATH = "stock.html"

# Rarity mapping for styling
RARITY_MAP = {
    "Common": "common",
    "Uncommon": "uncommon",
    "Rare": "rare",
    "Epic": "epic",
    "Legendary": "legendary",
    "Mythic": "mythic",
    "Secret": "secret"
}

def fetch_stock_data() -> List[Dict[str, Any]]:
    """Fetch latest stock data from API"""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock data: {e}")
        sys.exit(1)

def parse_stock_description(description: str) -> Dict[str, Any]:
    """Parse the stock description text into structured data"""
    lines = description.split('\n')
    seeds = []
    gear = []
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for section headers
        if line == '**Seeds**':
            current_section = 'seeds'
            continue
        elif line == '**Gear**':
            current_section = 'gear'
            continue
        elif line.startswith('<:clock:'):
            # Discord timestamp line, skip
            break

        # Parse item lines (format: "Item Name xCount")
        if current_section and ' x' in line:
            match = re.match(r'^(.+?)\s*x(\d+)$', line)
            if match:
                item_name = match.group(1).strip()
                stock = int(match.group(2))

                item = {
                    'name': item_name,
                    'stock': stock,
                    'available': stock > 0
                }

                if current_section == 'seeds':
                    seeds.append(item)
                elif current_section == 'gear':
                    gear.append(item)

    return {
        'seeds': seeds,
        'gear': gear
    }

def determine_rarity(item_name: str) -> str:
    """Determine item rarity based on name patterns"""
    name_lower = item_name.lower()

    # Secret tier
    if any(word in name_lower for word in ['divine', 'celestial', 'quantum', 'infinity']):
        return "secret"

    # Mythic tier
    if any(word in name_lower for word in ['shadow', 'eclipse', 'void', 'cosmic', 'plasma']):
        return "mythic"

    # Legendary tier
    if any(word in name_lower for word in ['golden', 'diamond', 'crystal', 'sun god', 'mega']):
        return "legendary"

    # Epic tier
    if any(word in name_lower for word in ['winter', 'ice', 'fire', 'electric', 'storm']):
        return "epic"

    # Rare tier
    if any(word in name_lower for word in ['gatling', 'repeater', 'twin', 'triple']):
        return "rare"

    # Uncommon tier
    if any(word in name_lower for word in ['grape', 'eggplant', 'watermelon', 'frost blower']):
        return "uncommon"

    # Default to common
    return "common"

def get_stock_indicator(stock: int) -> tuple:
    """Get stock level indicator class and icon"""
    if stock >= 3:
        return "stock-high", "✓"
    elif stock >= 2:
        return "stock-medium", "!"
    else:
        return "stock-low", "⚠"

def format_price(item_name: str) -> str:
    """Estimate price based on rarity"""
    rarity = determine_rarity(item_name)
    prices = {
        "common": "$100",
        "uncommon": "$250",
        "rare": "$500",
        "epic": "$1,000",
        "legendary": "$5,000",
        "mythic": "$10,000",
        "secret": "$50,000"
    }
    return prices.get(rarity, "$100")

def generate_stock_item_html(item: Dict[str, Any]) -> str:
    """Generate HTML for a single stock item"""
    name = item.get('name', 'Unknown')
    stock = item.get('stock', 0)
    available = item.get('available', False)

    rarity = determine_rarity(name)
    rarity_class = f"rarity-{rarity}"
    stock_class, _ = get_stock_indicator(stock)

    out_of_stock_class = "" if available and stock > 0 else "out-of-stock"

    html = f"""
            <div class="stock-item {out_of_stock_class}">
                <div class="item-header">
                    <span class="item-name">{name}</span>
                    <span class="item-rarity {rarity_class}">{rarity.title()}</span>
                </div>
                <div class="item-details">
                    <div class="detail-row">
                        <span class="detail-label">Stock:</span>
                        <div class="stock-count">
                            <span class="stock-indicator {stock_class}"></span>
                            <span class="detail-value">{stock if stock > 0 else 'Out of Stock'}</span>
                        </div>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Status:</span>
                        <span class="detail-value" style="color: {'#00DC82' if available and stock > 0 else '#FF006E'};">
                            {'Available' if available and stock > 0 else 'Sold Out'}
                        </span>
                    </div>
                </div>
            </div>"""
    return html

def generate_stock_section(title: str, icon: str, items: List[Dict[str, Any]]) -> str:
    """Generate HTML for a stock section"""
    if not items:
        return f"""
        <div class="stock-section">
            <h3>{icon} {title}</h3>
            <div class="empty-state">
                <h4>No {title.lower()} currently in stock</h4>
                <p>Check back soon - George restocks every 5 minutes!</p>
            </div>
        </div>"""

    # Add rarity to items
    for item in items:
        item['rarity'] = determine_rarity(item['name'])

    # Sort items by stock (low stock first) and then by name
    items.sort(key=lambda x: (x.get('stock', 999), x.get('name', '')))

    items_html = "\n".join([generate_stock_item_html(item) for item in items])

    return f"""
        <div class="stock-section">
            <h3>{icon} {title}</h3>
            <div class="stock-items">
{items_html}
            </div>
        </div>"""

def generate_history_html(api_data: List[Dict[str, Any]]) -> str:
    """Generate HTML for stock history section"""
    if len(api_data) < 2:
        return ""  # Don't show history if only current entry exists

    history_items = []
    # Skip the first entry (current stock) and show the next entries
    for entry in api_data[1:5]:  # Show up to 4 history entries
        # Parse timestamp
        timestamp = entry.get('createdAt', '')
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

        # Convert to US Eastern Time for default display
        dt_eastern = dt.astimezone(ZoneInfo('America/New_York'))
        formatted_time = dt_eastern.strftime('%I:%M %p')
        formatted_date = dt_eastern.strftime('%b %d')

        # Keep UTC ISO format for JS conversion
        iso_timestamp = dt.isoformat()

        # Parse stock data
        description = entry.get('embeds', [{}])[0].get('description', '')
        stock_data = parse_stock_description(description)
        seeds = stock_data.get('seeds', [])
        gear = stock_data.get('gear', [])

        # Calculate totals
        total_items = len(seeds) + len(gear)
        total_stock = sum(item['stock'] for item in seeds) + sum(item['stock'] for item in gear)

        # Create item badges with rarity
        seed_items = []
        for seed in seeds:
            rarity = determine_rarity(seed['name'])
            rarity_class = f"rarity-{rarity}"
            seed_items.append(f'<span class="history-item-badge {rarity_class}">{seed["name"]} ({seed["stock"]})</span>')

        gear_items = []
        for g in gear:
            rarity = determine_rarity(g['name'])
            rarity_class = f"rarity-{rarity}"
            gear_items.append(f'<span class="history-item-badge {rarity_class}">{g["name"]} ({g["stock"]})</span>')

        # Join all items for display
        all_seeds = ' '.join(seed_items) if seed_items else '<span class="empty-history">No seeds</span>'
        all_gear = ' '.join(gear_items) if gear_items else '<span class="empty-history">No gear</span>'

        history_html = f"""
        <div class="history-entry">
            <div class="history-header">
                <span class="history-time" data-utc="{iso_timestamp}">
                    <strong class="time-value">{formatted_time}</strong>
                    <small class="date-value">{formatted_date}</small>
                </span>
                <span class="history-stats">
                    <span class="stat-badge">📦 {total_items} items</span>
                    <span class="stat-badge">∑ {total_stock} stock</span>
                </span>
            </div>
            <div class="history-content">
                <div class="history-category">
                    <span class="category-label">🌱 Seeds ({len(seeds)}):</span>
                    <div class="history-items">
                        {all_seeds}
                    </div>
                </div>
                <div class="history-category">
                    <span class="category-label">⚔️ Gear ({len(gear)}):</span>
                    <div class="history-items">
                        {all_gear}
                    </div>
                </div>
            </div>
        </div>"""

        history_items.append(history_html)

    if not history_items:
        return ""

    return f"""
        <section class="history-section">
            <h2>📜 Recent Stock History</h2>
            <p class="history-description">Last {len(history_items)} stock updates from George's shop</p>
            <div class="history-container">
                {''.join(history_items)}
            </div>
        </section>"""

def update_stock_html(api_data: List[Dict[str, Any]]):
    """Update stock.html with latest data and history"""
    try:
        # Read the template
        with open(STOCK_HTML_PATH, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Get current stock (first entry)
        if not api_data:
            print("No data received from API")
            sys.exit(1)

        current_entry = api_data[0]

        # Get timestamp
        timestamp = current_entry.get('createdAt', datetime.now(timezone.utc).isoformat())
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

        # Convert to US Eastern Time for default display
        from zoneinfo import ZoneInfo
        dt_eastern = dt.astimezone(ZoneInfo('America/New_York'))
        formatted_time = dt_eastern.strftime('%B %d, %Y at %I:%M %p EST')

        # Keep UTC ISO format for JS conversion
        iso_timestamp = dt.isoformat()

        # Parse current stock
        description = current_entry.get('embeds', [{}])[0].get('description', '')
        stock_data = parse_stock_description(description)
        seeds = stock_data.get('seeds', [])
        gear = stock_data.get('gear', [])

        # Generate sections
        stock_sections = []

        # Add seeds section if there are seeds
        if seeds:
            stock_sections.append(generate_stock_section("Seeds", "🌱", seeds))

        # Add gear section if there is gear
        if gear:
            stock_sections.append(generate_stock_section("Gear", "⚔️", gear))

        # If no items at all
        if not stock_sections:
            stock_sections.append("""
        <div class="stock-section">
            <h3>📦 George's Shop Status</h3>
            <div class="empty-state">
                <h4>Shop is currently empty</h4>
                <p>George restocks every 5 minutes with random seeds and gear.</p>
                <p>This page automatically updates - check back soon!</p>
            </div>
        </div>""")

        stock_content = "\n".join(stock_sections)

        # Generate history HTML
        history_html = generate_history_html(api_data)

        # Replace placeholders with timestamp data attribute
        # Find and replace the update time with data attribute
        # Pattern matches both with and without data-utc attribute
        update_time_pattern = r'<div class="update-time"[^>]*>[^<]+</div>'
        update_time_replacement = f'<div class="update-time" data-utc="{iso_timestamp}">Last Updated: {formatted_time}</div>'
        html_content = re.sub(update_time_pattern, update_time_replacement, html_content)

        # Handle stock content - use a more robust replacement method
        # Find and replace everything between stock-grid opening and its proper closing
        stock_pattern = r'<div class="stock-grid">.*?(?=<section class="history-section">|<section class="content-section">|\Z)'
        replacement = f'<div class="stock-grid">\n{stock_content}\n        </div>\n\n        '
        html_content = re.sub(stock_pattern, replacement, html_content, flags=re.DOTALL)

        # Handle history section - replace existing or add new
        history_pattern = r'<section class="history-section">.*?</section>\s*(?=<section class="content-section">)'
        if re.search(history_pattern, html_content, re.DOTALL):
            html_content = re.sub(history_pattern, history_html + '\n\n        ', html_content, flags=re.DOTALL)
        else:
            # Find the position before content section
            content_pos = html_content.find('<section class="content-section">')
            if content_pos != -1:
                # Insert history before content section
                html_content = (
                    html_content[:content_pos] +
                    history_html + '\n\n        ' +
                    html_content[content_pos:]
                )

        # Write updated HTML
        with open(STOCK_HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Stock page updated successfully at {formatted_time}")
        print(f"   - Seeds: {len(seeds)} items")
        print(f"   - Gear: {len(gear)} items")
        print(f"   - History entries: {len(api_data) - 1}")

    except Exception as e:
        print(f"Error updating HTML: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main execution function"""
    print("🔄 Fetching stock data from API...")
    api_data = fetch_stock_data()

    print(f"📊 Processing {len(api_data)} stock entries...")

    print("📝 Updating stock.html...")
    update_stock_html(api_data)

    print("✨ Stock tracker update completed!")

if __name__ == "__main__":
    main()