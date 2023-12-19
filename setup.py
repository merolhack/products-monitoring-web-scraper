from setuptools import setup 
  
setup( 
    name='products_monitoring_web_scraper', 
    version='0.1', 
    description='Web Scraper', 
    author='Lenin Meza', 
    author_email='merolhack@gmail.com', 
    packages=['products_monitoring_web_scraper'], 
    install_requires=[ 
        'flask', 
        'selenium',
        'dotenv',
    ], 
) 
