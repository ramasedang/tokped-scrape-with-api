# Tokopedia Product Scraper

A comprehensive web scraping solution for extracting product data from Tokopedia, one of Indonesia's largest e-commerce platforms. This scraper supports both keyword-based and category-based product collection with concurrent processing and BigQuery integration.

## Features

- **Multi-mode Scraping**: Support for both keyword-based and category-based product searches
- **Concurrent Processing**: High-performance scraping with configurable thread pools
- **Data Validation**: Built-in error handling and data validation mechanisms
- **BigQuery Integration**: Direct data streaming to Google BigQuery for analytics
- **Discord Notifications**: Real-time webhook notifications for scraping status
- **Extensible Architecture**: Modular design with separate components for easy maintenance

## Architecture

```
tokopedia-scraper/
├── src/                          # Core application modules
│   ├── __init__.py
│   ├── allreq.py                 # API request handlers
│   ├── service.py                # Business logic and data processing
│   └── utils.py                  # Utility functions
├── scripts/                      # Main execution scripts
│   ├── main.py                   # Primary application entry point
│   ├── task.py                   # Configuration definitions
│   ├── push.py                   # BigQuery integration
│   └── T_shopee_sender.py        # Database operations
├── docs/                         # Reference implementations
│   ├── catscrap.js               # JavaScript category scraper
│   ├── keywordscrap.js           # JavaScript keyword scraper
│   ├── reqCategory.py            # Request templates
│   ├── reqGet.py                 # GET request examples
│   └── reqProduct.py             # Product request examples
├── data/                         # Data storage and mapping
│   ├── key.json                  # Google Cloud credentials
│   └── mapping/                  # Category mapping files
│       ├── catmapping.csv
│       └── catmapping_filtered.csv
└── export/                       # Output directory
    └── bycat/                    # Category-based exports
```

## Installation

### Prerequisites

- Python 3.7+
- Google Cloud credentials (`data/key.json`)
- Node.js (for JavaScript components)

### Dependencies

```bash
pip install requests pandas google-cloud-bigquery concurrent.futures
npm install csvtojson p-map jsonrawtoxlsx write-json-file
```

## Configuration

### Environment Setup

1. Place your Google Cloud credentials as `data/key.json`
2. Configure Discord webhook URL in `scripts/main.py`
3. Set up your category mappings in `data/mapping/catmapping.csv`

### Scraping Configuration

Edit `scripts/task.py` to configure:

```python
byKeyword = {
    "brand_name": {
        "datatable": "target_table",
        "list_keywords": ["keyword1", "keyword2", ...]
    }
}

byCategory = {
    "category_name": {
        "datatable": "target_table", 
        "cat": "cat3",
        "lis_category": ["Category1", "Category2", ...]
    }
}
```

## Usage

### Command Line Interface

```bash
# Scrape all configured keywords
python scripts/main.py -k all

# Scrape specific keyword configuration
python scripts/main.py -k lions

# Scrape all configured categories
python scripts/main.py -c all

# Scrape specific category configuration
python scripts/main.py -c blueband
```

### Programmatic Usage

```python
from src.service import getLstProduct, getCat

# Keyword-based scraping
products = getLstProduct("search keyword", "table_name")

# Category-based scraping
category_data = getCat("category_type", category_list, "table_name")
```

## Data Schema

The scraper collects the following product attributes:

- `marketplace`: Platform identifier ("tokopedia")
- `itemid`: Unique product identifier
- `shopid`: Unique shop identifier  
- `product_link`: Direct product URL
- `product_title`: Product name
- `brand`: Product brand (if available)
- `store_type`: Official/Unofficial store status
- `store_name`: Shop name
- `store_link`: Shop URL
- `store_location`: Shop geographical location
- `price`: Product price
- `rating`: Average rating
- `historical_sold`: Total units sold
- `review_count`: Number of reviews
- `view_count`: Page view count
- `datescrap`: Scraping timestamp
- `cat_slug`: Category identifier

## Performance Optimization

- **Concurrent Requests**: Configurable thread pools for parallel processing
- **Retry Logic**: Automatic retry with exponential backoff
- **Cookie Management**: Dynamic cookie rotation for request reliability
- **Rate Limiting**: Built-in delays to respect platform limits

## Monitoring & Notifications

The system integrates with Discord webhooks to provide:

- Real-time scraping progress updates
- Completion notifications with elapsed time
- Error alerts and troubleshooting information

## Security Considerations

- User-Agent rotation for request anonymization
- Request header randomization
- Timeout handling and error recovery
- Secure credential management via environment variables

## BigQuery Integration

Data is automatically streamed to Google BigQuery with:

- Batch processing for optimal performance
- Data type validation and conversion
- Automatic error handling and retry logic
- Configurable table destinations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes with proper error handling
4. Add appropriate documentation
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for ensuring compliance with Tokopedia's terms of service and applicable laws regarding web scraping.

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Review the reference implementations in the `docs/` directory
- Check Discord webhook notifications for real-time error reporting