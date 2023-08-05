# scrapyx-stormproxies

Stormproxies middleware for Scrapy (http://scrapy.org/)

Required
--------

    python version >= 2.7


Install
--------

Checkout the source and run

    python setup.py install

Or

    pip install scrapyx-stormproxies


settings.py
-----------

    # Activate the middleware
    STORMPROXIES_ENABLED = True
    
    # The Stormproxies URL
    STORMPROXIES_URL = 'http://x.x.x.x:13080'

    DOWNLOADER_MIDDLEWARES = {
        'scrapyx_stormproxies.StormProxyMiddleware': 610,
    }
