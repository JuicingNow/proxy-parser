# Free Proxy Parser

This is a script built with Python and `aiohttp`

## Features
- Parse free proxies
- Return huge list of proxies (~10k)
- Quick parse (~8s)

## Conditions
- Python 3.6 and above versions installed on your PC

## Getting Started

1. **Clone this repository to your project:**
    ```bash
   git clone https://github.com/JuicingNow/Proxy-Parser.git
2. **Install dependencies:**
    ```bash
   pip install aiohttp
3. **To get list of free proxies use fetch_proxies():**

   ```python
   proxies = await fetch_proxies()
