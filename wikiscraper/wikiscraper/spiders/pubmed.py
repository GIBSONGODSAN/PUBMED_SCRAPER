import scrapy
import re
from wikiscraper.items import PubItem

class PubMedSpider(scrapy.Spider):
    name = "pubmed"

    def __init__(self, query=None, *args, **kwargs):
        super(PubMedSpider, self).__init__(*args, **kwargs)
        self.query = query

    # custom_settings = {
    #     'FEEDS': {
    #         'scraped_data.json': {'format': 'json', 'overwrite': True},
    #     }
    # }

    def start_requests(self):
        if self.query:
            search_term = '+'.join(self.query.split())
            if "'" in self.query:
                search_term = search_term.replace("'", "%27")
            if " " in self.query:
                search_term = search_term.replace(" ", "%20")

            start_url = f"https://pubmed.ncbi.nlm.nih.gov/?term={search_term}"
            yield scrapy.Request(start_url, callback=self.parse)
        else:
            self.logger.error("No search query provided")

    def parse(self, response):
        # Extract data from the current page
        titles = response.css('a.docsum-title')
        complete_titles = []

        for title in titles:
            title_text = title.css('::text').getall()
            complete_title = ' '.join(title_text).strip()

            if complete_title:
                complete_titles.append(complete_title)

        # Extract other data and store as PubItem objects
        authors = response.css('span.docsum-authors.full-authors::text').getall()
        citations = response.css('span.docsum-journal-citation.full-journal-citation::text').getall()
        pmids = response.css('.docsum-pmid::text').getall()
        free_article = response.css('span.free-resources.spaced-citation-item.citation-part::text').getall()
        reviews = response.css('span.publication-type.spaced-citation-item.citation-part::text').getall()

        # Process and store the extracted data as PubItem objects
        for title, author, citation, pmid, free, review in zip(complete_titles, authors, citations, pmids, free_article, reviews):
            item = PubItem()
            item['title'] = title
            item['author'] = author
            item['citation'] = citation
            item['pmid'] = pmid
            item['free'] = free
            item['review'] = review
            yield item

        # Follow the link to the next page of search results, if available
        # query_params = response.url.split('?')[-1]
        # next_page_input = response.css('.page-number-wrapper input.page-number::attr(value)').get()
        # total_pages_label = response.css('.page-number-wrapper label.of-total-pages::text').get()

        # if next_page_input and total_pages_label:
        #     total_pages = re.search(r'of (\d+(?:,\d+)*)', total_pages_label)
        #     if total_pages:
        #         total_pages = int(total_pages.group(1).replace(',', ''))
        #         current_page = int(next_page_input)
        #         if current_page < total_pages:
        #             next_page_number = current_page + 1
        #             next_page_url = f"{response.url.split('?')[0]}?{query_params}&page={next_page_number}"

        #             yield response.follow(next_page_url, self.parse)
