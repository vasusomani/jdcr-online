import re
import os
import xml.etree.ElementTree as ET

from pathlib import Path
from datetime import datetime
from django.core.files import File


class GenXML:
    def __init__(self, article, journal, publisher=None):
        self.article = article
        self.journal = journal
        self.publisher = publisher
        self.root = ET.Element(
            "article",
            attrib={
                "xmlns:mml": "http://www.w3.org/1998/Math/MathML",
                "xmlns:xlink": "http://www.w3.org/1999/xlink",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "article-type": self.article.article_type,
                "dtd-version": "1.0",
            },
        )
        self.filename = None
        self.filepath = None

    def journal_meta(self, front):
        if self.journal:
            _ = ET.SubElement(front, "journal-meta")
            ET.SubElement(_, "journal-id", attrib={"journal-id-type": "pmc"}).text = (
                self.journal.url.lower()
            )
            ET.SubElement(
                _, "journal-id", attrib={"journal-id-type": "pubmed"}
            ).text = self.journal.url.upper()
            ET.SubElement(
                _, "journal-id", attrib={"journal-id-type": "publisher"}
            ).text = self.journal.url.upper()
            ET.SubElement(_, "issn").text = self.journal.issn_online

            # publisher
            if self.publisher:
                publisher = ET.SubElement(_, "publisher")
                ET.SubElement(publisher, "publisher-name").text = self.publisher.name

    def contrib_group_and_aff(self, article_meta):
        from core.models import ArticleAuthor

        if self.article.authors.all:
            affiliations = {}
            aff_counter = 97
            for author in ArticleAuthor.objects.filter(article=self.article):
                if author.affiliation not in affiliations:
                    affiliations.update({author.affiliation: f"aff-{chr(aff_counter)}"})
                    aff_counter += 1
            authors = []
            for author in ArticleAuthor.objects.filter(article=self.article):
                temp = author.__dict__
                temp.update(
                    {
                        "first_name": author.first_name,
                        "middle_name": author.middle_name,
                        "last_name": author.last_name,
                        "author_affiliation_id": (
                            affiliations.get(author.affiliation)
                            if author.affiliation
                            else None
                        ),
                    }
                )
                authors.append(temp)
            for author in authors:
                _ = ET.SubElement(article_meta, "contrib-group")
                contrib = ET.SubElement(_, "contrib", attrib={"contrib-type": "author"})
                name = ET.SubElement(contrib, "name")
                if author.get("first_name") or author.get("middle_name"):
                    ET.SubElement(name, "given-names").text = (
                        f"{author.get('first_name')} {author.get('middle_name')}"
                    )
                if author.get("last_name"):
                    ET.SubElement(name, "surname").text = author.get("last_name")

                if author.get("author_affiliation_id"):
                    ET.SubElement(
                        _,
                        "xref",
                        attrib={
                            "ref-type": "aff",
                            "rid": author.get("author_affiliation_id"),
                        },
                    )

            for (
                k,
                v,
            ) in affiliations.items():
                ET.SubElement(article_meta, "aff-id", attrib={"id": v}).text = k

    def article_meta(self, front):
        title = self.article.title
        abstract = self.article.abstract
        authors = self.article.authors.all()

        if self.article:
            _ = ET.SubElement(front, "article-meta")

            # article-id
            if self.article.doi:
                ET.SubElement(_, "article-id", attrib={"pub-id-type": "doi"}).text = (
                    self.article.doi
                )
            if self.article.pmid:
                ET.SubElement(_, "article-id", attrib={"pub-id-type": "pmid"}).text = (
                    self.article.pmid
                )

            # title-group
            title_group = ET.SubElement(_, "title-group")
            ET.SubElement(title_group, "article-title").text = self.article.title

        self.contrib_group_and_aff(_)

        abstract_element = ET.SubElement(_, "abstract")
        abstract_element.text = re.sub(r"<.*?>", "", self.article.abstract)

    def extract_references(self):
        from core.models import ArticleSection

        references = ArticleSection.objects.filter(
            article=self.article, heading__icontains="Reference"
        ).first()
        if references:

            # Remove <ol> and <li> tags
            # cleaned_string = re.sub(r'<ol>|</ol>|<li>|</li>', '', references)

            # Wrap the cleaned string with a root element for parsing
            xml_string = f"<root>{references.content}</root>"

            # Parse the XML string
            root = ET.fromstring(xml_string)

            # Extract text content from each <li> and store in a list
            references = [li.text for li in root.findall(".//li")]

            return references
        else:
            return []

    def generate_references(self, back):
        # Create the root element

        references = self.extract_references()

        if references:
            ref_list = ET.SubElement(back, "ref-list")

            for idx, ref in enumerate(references, start=1):
                _ref = ET.SubElement(ref_list, "ref", attrib={"id": f"B{idx}"})
                ET.SubElement(_ref, "label").text = str(idx)

                year_match = re.search(r"\((\d{4})\)", ref)
                if year_match:
                    year = year_match.group(1)
                    parts = ref.split(f"({year})")

                    if len(parts) == 2:
                        element_citation = ET.SubElement(
                            _ref,
                            "element-citation",
                            attrib={"publication-type": "journal"},
                        )
                        ET.SubElement(
                            element_citation, "year", attrib={"iso-8601-date": year}
                        )

                        # authors
                        try:
                            authors = "".join(parts[0].strip().split("&"))
                        except:
                            authors = authors.split(",")
                        if type(authors) == list:
                            split_authors = [
                                f"{parts[i]}, {parts[i+1]}"
                                for i in range(0, len(authors), 2)
                            ]
                        else:
                            split_authors = [authors]

                        if split_authors:
                            person_group = ET.SubElement(
                                element_citation,
                                "person-group",
                                attrib={"person-group-type": "author"},
                            )
                            for p in split_authors:
                                name = ET.SubElement(person_group, "name")
                                surname = p.split(",")[0].lstrip().rstrip()
                                given_name = p.split(",")[1].rstrip().lstrip()
                                if surname:
                                    ET.SubElement(name, "surname").text = surname
                                if given_name:
                                    ET.SubElement(name, "given-name").text = given_name

                        # article info
                        info = parts[1].strip()

    def generate_jats_xml(self):

        front = ET.SubElement(self.root, "front")

        self.journal_meta(front)
        self.article_meta(front)

        body_element = ET.SubElement(self.root, "body")
        body_element.text = body_element

        back_element = ET.SubElement(self.root, "back")
        self.generate_references(back_element)

        self.xml_string = ET.tostring(self.root, encoding="utf-8").decode("utf-8")

    def write_xml(self):
        if not Path("media").is_dir():
            os.mkdir("media")
        
        self.filename = f"{self.article.pk}.xml"
        self.filepath = self.filename

        with open(self.filepath, "w+") as f:
            f.write(self.xml_string)
            self.article.xml = File(f)

            # reset generate flag
            self.article.generate_xml = False

            self.article.save()

        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def update_model(self):
        with open(self.filepath, "rb") as f:
            self.article.xml = File(f)

        self.article.generate_xml = False
        self.article.save()

    def run(self):
        self.generate_jats_xml()
        self.write_xml()
        # self.update_model()
