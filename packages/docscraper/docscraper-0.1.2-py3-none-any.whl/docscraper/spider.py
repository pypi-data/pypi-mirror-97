from datetime import datetime
import os
from urllib.parse import urlparse
from uuid import uuid4

import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DocLinkExtractor(LinkExtractor):  # lgtm [py/missing-call-to-init]

    def __init__(self, extensions, *args, **kwargs):
        """ Custom link extractor to extract document links.

        :param extensions: a list of file extensions for extraction
        :type extensions: list

        """

        super(DocLinkExtractor, self).__init__(*args, **kwargs)
        # Keep the default values in deny_extensions except the ones we want
        self.deny_extensions = [e for e in self.deny_extensions if
                                e not in extensions]


class DocSpider(CrawlSpider):

    name = "DocScraper"

    def __init__(self, allowed_domains, start_urls, directory='./output',
                 extensions=['.pdf', '.doc', '.docx'], **kwargs):
        """ The Spider to crawl site(s) for documents.

        :param allowed_domains: A list of allowed domains for the crawl
        :type allowed_domains: list
        :param start_urls: A list of the start urls for the crawl
        :type start_urls: list
        :param directory: The directory path to which to save documents
        :type directory: str
        :param extensions: A list of document extensions
                           (e.g., [".pdf", ".doc", ".docx"])
        :type extensions: list, optional

        """

        self.files = []
        self.allowed_domains = allowed_domains
        self.start_urls = start_urls
        self.directory = directory
        self.extensions = extensions
        self.rules = (Rule(DocLinkExtractor(extensions), follow=True,
                           callback="parse_item"),)
        super(DocSpider, self).__init__(**kwargs)

        # Raise exception if directory for file downloads is not empty.
        dirpath = os.path.abspath(self.directory)
        if os.path.exists(dirpath) and len(dirpath) > 0:
            raise Exception("Directory is not empty. Please provide an empty "
                            "or non-existent directory path.")

    def parse_item(self, response):
        """ Download document and save metadata to files attribute. """
        f = response.url.split("/")[-1]
        filename, ext = os.path.splitext(f)
        if ext in self.extensions:
            url = response.url
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

            domain = urlparse(url).netloc
            filename = "{}-ST-{}{}".format(filename, uuid4(), ext)
            relative_path = "/".join([domain, filename])

            self.logger.info("Saving file {}".format(url))
            os.makedirs("{}/{}".format(self.directory, domain),
                        exist_ok=True)

            with open("{}/{}".format(self.directory, relative_path),
                      "wb") as file:
                file.write(response.body)

            self.files.append(dict(
                domain=domain,
                url=url,
                relative_path=relative_path,
                scraped_at=timestamp,
                filename=filename
            ))

    def closed(self, reason):
        """ Save a MS Excel file listing document when crawl ends. """
        df = pd.DataFrame().from_records(self.files)
        df.to_excel("{}/file-listing.xlsx".format(self.directory), index=False)


def crawl(allowed_domains, start_urls, directory="./output",
          extensions=[".pdf", ".docx", ".doc"]):
    process = CrawlerProcess()
    process.crawl(DocSpider, allowed_domains, start_urls,
                  directory=directory, extensions=extensions)
    process.start()
