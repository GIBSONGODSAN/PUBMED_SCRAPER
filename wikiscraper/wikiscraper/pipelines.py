# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import mysql.connector 

class WikiscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        adapter['title'] = self.clean_title(adapter['title'])
        adapter['author'] = self.clean_author(adapter['author'])
        adapter['citation'] = self.clean_citation(adapter['citation'])
        adapter['pmid'] = self.clean_pmid(adapter['pmid'])
        adapter['free'] = self.clean_free(adapter['free'])
        adapter['review'] = self.clean_review(adapter['review'])


        return item

    def clean_title(self, title):
        # Clean the title here (if needed)
        return title.strip()

    def clean_author(self, author):
        # Clean the author here (if needed)
        return author.strip()

    def clean_citation(self, citation):
        # Clean the citation here (if needed)
        return citation.strip()

    def clean_pmid(self, pmid):
        # Clean the PMID here (if needed)
        return re.sub(r'\D', '', pmid)  # Remove non-digit characters

    def clean_free(self, free):
        # Clean the free here (if needed)
        return free.strip()

    def clean_review(self, review):
        # Clean the review here (if needed)
        return review.strip()

class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='scraping'
        )

        self.curr = self.conn.cursor()

        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS ScrapedData (
                id INT NOT NULL auto_increment,
                title VARCHAR(255),
                author VARCHAR(255),
                citation VARCHAR(255),
                pmid VARCHAR(255),
                free VARCHAR(200),
                review VARCHAR(100),
                PRIMARY KEY (id)
            )
        """)

    def process_item(self, item, spider):
        self.curr.execute("""
            INSERT INTO ScrapedData (
                title,
                author,
                citation,
                pmid,
                free,
                review
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            item["title"],
            item["author"],
            item["citation"],
            item["pmid"],
            item["free"],
            item["review"],
        ))

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.curr.close()
        self.conn.close()
