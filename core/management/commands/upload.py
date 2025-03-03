import os
import re
import numpy as np
import pandas as pd
from datetime import datetime
from django.db import IntegrityError


from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import *


class Command(BaseCommand):
    help = "Update articles using .xlsx file"
    
    def process_authors(self, article, authors):
        authors = authors.split(",")

        if len(authors) == 1 and authors[0] == "":
            return
        
        ArticleAuthor.objects.filter(article=article).delete()
        
        for a in authors:            
            split_name = a.lstrip().rstrip().split(" ")
            
            author_name = {
                "article": article,
                "prefix": None,
                "first_name": None,
                "middle_name": None,
                "last_name": None
            }

            author_name["first_name"] = split_name[0]
            del split_name[0]
            
            if len(split_name) > 0:
                author_name["last_name"] = split_name[-1]
                del split_name[-1]
            
            if len(split_name) > 0:
                author_name["middle_name"] = " ".join(split_name)
                
            author = ArticleAuthor.objects.create(**author_name)
            author.save()
            
        return

    def parse_dt(self, dt):
        if not dt:
            return None
        elif type(dt) == str:
            dt = dt.lstrip().rstrip()
            return datetime.strptime(dt, "%d/%m/%y")
        elif type(dt) == pd.Timestamp:
            return dt.to_pydatetime()
        elif type(dt) == datetime:
            return dt
        try:
            return datetime.strptime(dt, "%Y-%m-%d")
        except:
            return None
    
    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "media/data.csv")
        df = pd.read_csv(file_path)
        df = df.fillna(value="")
        
        print(df.columns)
                
        journal = Journal.objects.all().first()
        
        for idx, row in df.iterrows():            
            try:
                volume, _ = Volume.objects.get_or_create(
                    name=f"Volume {row.get('Volume')}",
                    year=row.get("Year")
                )
                # issue_month = row.get("issue_month") if row.get("issue_month") != "#NUM!" else None
                issue, _ = Issue.objects.get_or_create(
                    volume=volume,
                    name=f"Issue {row.get('Issue')}",
                    # month=issue_month
                )
                
                title = row["Article title"]
                # Check for duplicate titles
                articles = Article.objects.filter(title=title)
                if articles.exists():
                    if len(articles) > 1:
                        print(f"MULTIPLE {title}")
                    article = articles.first()
                else:
                    # Create new article if not found
                    article = Article.objects.create(issue=issue, title=title)
                    print(f"CREATED {article.pk} - {article.title}")
                
                # article.keywords = row.get("keywords")
                # article.revised = self.parse_dt(row["revised"]) if not pd.isna(row["revised"]) else None
                # article.accepted = self.parse_dt(row["accepted"]) if not pd.isna(row["accepted"]) else None
                article.article_type = "Research Article"
                article.abstract = row["Abstracts"] if row["Abstracts"] else None               
                article.keywords = row["Keywords"] if row["Keywords"] else None
                article.received = self.parse_dt(row["Received"])
                article.published = self.parse_dt(row["Published"])
                # article.url = row["URL "] if row["URL "] else None

                if row["Page No."]:
                    pages = re.sub(r'[^\d-]', '', row["Page No."]).split("-")
                    article.page_from = int(pages[0]) if pages[0] else None
                    article.page_to = int(pages[1]) if pages[1] else None
                    
                
                if row["PMID"]:
                    pmid = row["PMID"].lstrip().rstrip()
                    article.pmid = pmid
                    article.pmid_link = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmid}"
                
                if row["DOI"]:
                    doi = row["DOI"].lstrip().rstrip()
                    article.doi = doi
                    article.doi_link = f"https://doi.org/{doi}"
                
                article.save()

                self.process_authors(article, row['Author Name'])
                
            except Exception as e:
                print(str(e))
                