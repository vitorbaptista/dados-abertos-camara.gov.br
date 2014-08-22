# -*- coding: utf-8 -*-

# Scrapy settings for camaragovbr project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'camaragovbr'

SPIDER_MODULES = ['camaragovbr.spiders']
NEWSPIDER_MODULE = 'camaragovbr.spiders'

# Crawl responsibly by identifying yourself and your website on the user-agent
#USER_AGENT = 'camaragovbr (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'camaragovbr.pipelines.RemoveDuplicateProposicoesPipeline': 300
}
HTTPCACHE_ENABLED = True

FEED_EXPORTERS = {
    'json': 'camaragovbr.exporters.SortedJsonItemExporter'
}
