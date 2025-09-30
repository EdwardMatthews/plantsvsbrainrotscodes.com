# Plants vs Brainrots Stock Tracker

## Overview
Automated stock tracking system for George's Shop in Plants vs Brainrots. Updates every 5 minutes with the latest seed and gear inventory from the game.

## Features
- ✅ Real-time stock monitoring
- ✅ Automatic updates every 5 minutes via GitHub Actions
- ✅ Static HTML generation (no client-side API calls)
- ✅ Rarity-based color coding
- ✅ Stock level indicators
- ✅ Mobile-responsive design
- ✅ Integrated with existing site navigation

## System Architecture

### Components
1. **stock.html** - Static HTML page template with placeholders
2. **update_stock.py** - Python script that fetches API data and generates HTML
3. **GitHub Action Workflow** - Automated scheduler running every 5 minutes
4. **External API** - https://plantsvsbrainrotsstocktracker.com/api/stock

### Data Flow
1. GitHub Action triggers every 5 minutes (cron: `*/5 * * * *`)
2. Python script fetches latest data from API
3. Script processes JSON response and generates HTML content
4. Updates stock.html with current inventory
5. Commits and pushes changes to repository
6. Website serves updated static HTML file

## API Integration

### Endpoint
```
https://plantsvsbrainrotsstocktracker.com/api/stock?since=0
```

### Response Structure
```json
{
  "timestamp": "2025-09-30T04:35:05.266Z",
  "source": "discord-bot-pvbr",
  "data": [
    {
      "name": "Dragon Fruit",
      "stock": 1,
      "available": true,
      "category": "SEEDS",
      "type": "seed",
      "lastUpdated": "2025-09-30T04:35:05.266Z"
    }
  ]
}
```

## Rarity System

### Tiers
- **Common** - Gray (#94a3b8)
- **Uncommon** - Blue (#00B4D8)
- **Rare** - Green (#00DC82)
- **Epic** - Purple (#a855f7)
- **Legendary** - Yellow (#FFD23F)
- **Mythic** - Pink (#FF006E)
- **Secret** - Gradient (Pink to Green)

### Detection Logic
Rarity is determined by analyzing item names for specific keywords:
- Secret: divine, celestial, quantum, infinity
- Mythic: shadow, eclipse, void, cosmic, plasma
- Legendary: golden, diamond, crystal, sun god, mega
- Epic: winter, ice, fire, electric, storm
- Rare: gatling, repeater, twin, triple
- Uncommon: snow, split, wall
- Common: default for all others

## Stock Indicators

### Levels
- **High Stock (3+)** - Green indicator ✓
- **Medium Stock (2)** - Yellow indicator !
- **Low Stock (1)** - Red indicator ⚠
- **Out of Stock (0)** - Grayed out with overlay

## GitHub Action Configuration

### Schedule
```yaml
on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
```

### Manual Trigger
The workflow can also be triggered manually from GitHub Actions tab.

### Workflow Steps
1. Checkout repository
2. Setup Python 3.11
3. Install dependencies (requests)
4. Run update_stock.py
5. Check for changes
6. Commit and push if changed

## Local Testing

### Prerequisites
```bash
pip install requests
```

### Run Update Script
```bash
python update_stock.py
```

### Test Output
```
🔄 Fetching stock data from API...
📝 Updating stock.html...
✅ Stock page updated successfully at September 30, 2025 at 04:35 AM UTC
   - Seeds: 5 items
   - Gear: 3 items
✨ Stock tracker update completed!
```

## File Structure
```
/
├── stock.html                          # Stock tracker page
├── update_stock.py                     # Update script
├── requirements.txt                    # Python dependencies
├── .github/
│   └── workflows/
│       └── update-stock.yml           # GitHub Action workflow
└── sitemap.xml                        # Updated with stock page
```

## Navigation Integration
Stock link added to all pages between Wiki and Script menu items:
```html
<li><a href="/wiki">Wiki</a></li>
<li><a href="/stock">Stock</a></li>
<li><a href="/script">Script</a></li>
```

## SEO Configuration

### Meta Tags
- Title: "Plants vs Brainrots Stock Tracker - Live Seed Inventory"
- Description: "Real-time Plants vs Brainrots stock tracker for George's shop..."
- Keywords: plants vs brainrots stock, pvb stock tracker, george shop

### Sitemap Entry
```xml
<url>
  <loc>https://plantsvsbrainrotscodes.com/stock</loc>
  <lastmod>2025-09-30</lastmod>
  <changefreq>hourly</changefreq>
  <priority>0.9</priority>
</url>
```

## Maintenance

### Updating Rarity Detection
Edit the `determine_rarity()` function in update_stock.py to add new keyword patterns.

### Adjusting Update Frequency
Modify the cron schedule in `.github/workflows/update-stock.yml`. Current setting is every 5 minutes.

### Price Adjustments
Update the `format_price()` function in update_stock.py to change pricing tiers.

## Troubleshooting

### Common Issues
1. **API Timeout** - Script has 10-second timeout, may fail if API is slow
2. **GitHub Action Limits** - Free tier allows 2000 minutes/month
3. **No Changes Detected** - Action skips commit if stock hasn't changed

### Debug Commands
```bash
# Check API directly
curl https://plantsvsbrainrotsstocktracker.com/api/stock?since=0

# Test Python script
python update_stock.py

# View GitHub Action logs
# Navigate to Actions tab in GitHub repository
```

## Future Enhancements
- [ ] Add historical stock tracking
- [ ] Implement alert system for rare items
- [ ] Create stock statistics dashboard
- [ ] Add price trend analysis
- [ ] Include estimated restock times

## License
Part of Plants vs Brainrots Codes website project.