import re

class GenerateCitation:
    def __init__(self, journal, volume, issue, article, authors):
        self.journal = journal
        self.volume = volume
        self.issue = issue
        self.article = article
        self.authors = authors
        self.APA = None
        self.MLA = None
        self.Chicago = None
        self.Vancouver = None
        self.Harvard = None
        
    def get_initial(self, name):
        initials = ""
        try:
            for i in name.split(" "):
                initials += f" {i[0].upper()}."
        except:
            initials = name    
        return initials
    
    def get_initial_without_dot(self, name):
        initials = ""
        try:
            for i in name.split(" "):
                initials += f"{i[0].upper()}"
        except:
            initials = name
        return initials
    
    def extract_num(self, name):
        num = re.findall(r'\d+', name)
        return num[0]
    
    def format_month(self, month):
        return month[:3].capitalize()
    
    def mla(self):
        authors = ""
        for idx, author in enumerate(self.authors):
            if idx == 0:
                authors += f"{author.last_name}, {author.first_name if author.first_name else ''}{self.get_initial(author.middle_name) if author.middle_name else ''}"
            elif len(self.authors) <= 3:
                authors += f"{', ' if idx != len(self.authors) - 1 else ' and '}{author.first_name}{self.get_initial(author.middle_name) if author.middle_name else ''} {author.last_name if author.last_name else ''}"
            else:
                authors += f"{', ' if idx != len(self.authors) - 1 else ' and '}et al"
                break
        text = f'{authors}. "{self.article.title}." <i>{self.journal.name}</i> {self.extract_num(self.volume.name)}.{self.extract_num(self.issue.name)} ({self.volume.year}): {self.article.page_from}-{self.article.page_to}.'
        self.MLA = text

    def apa(self):
        authors = ""
        for idx, author in enumerate(self.authors):
            if idx == 0:
                authors += f"{author.last_name},{self.get_initial(author.first_name) if author.first_name else ''}{self.get_initial(author.middle_name) if author.middle_name else ''}"
            else:
                authors += f"{', ' if idx != len(self.authors) - 1 else ' & '}{author.last_name},{self.get_initial(author.first_name) if author.first_name else ''}{self.get_initial(author.middle_name) if author.middle_name else ''}"
        text = f"{authors} ({self.volume.year}). {self.article.title}. <i>{self.journal.name}, {self.extract_num(self.volume.name)}</i>({self.extract_num(self.issue.name)}), {self.article.page_from}-{self.article.page_to}."
        self.APA =  text

    def chicago(self):
        authors = ""
        for idx, author in enumerate(self.authors):
            if idx == 0:
                authors += f"{author.last_name}, {author.first_name if author.first_name else ''}{self.get_initial(author.middle_name) if author.middle_name else ''}"
            else:
                authors += f"{', ' if idx != len(self.authors) - 1 else ' and '}{author.first_name}{self.get_initial(author.middle_name) if author.middle_name else ''} {author.last_name if author.last_name else ''}"
        text = f'{authors}. "{self.article.title}." <i>{self.journal.name}</i> {self.extract_num(self.volume.name)}, no. {self.extract_num(self.issue.name)} ({self.volume.year}): {self.article.page_from}-{self.article.page_to}.'
        self.Chicago = text

    def harvard(self):
        authors = ""
        for idx, author in enumerate(self.authors):
            if idx == 0:
                authors += f"{author.last_name},{self.get_initial(author.first_name) if author.first_name else ''}{self.get_initial(author.middle_name) if author.middle_name else ''}"
            else:
                authors += f"{', ' if idx != len(self.authors) - 1 else ' and '}{author.last_name},{self.get_initial(author.first_name) if author.first_name else ''}{self.get_initial(author.middle_name) if author.middle_name else ''}"
        text = f"{authors} ({self.volume.year}) '{self.article.title}' <i>{self.journal.name} {self.extract_num(self.volume.name)}</i>({self.extract_num(self.issue.name)}), pp. {self.article.page_from}-{self.article.page_to}."
        self.Harvard = text
    
    def vancouver(self):
        authors = ""
        for idx, author in enumerate(self.authors):
            authors += f"{author.first_name if not author.last_name else author.last_name } {self.get_initial_without_dot(author.first_name) if author.first_name else ''}{self.get_initial_without_dot(author.middle_name) if author.middle_name else ''}{', ' if idx != len(self.authors) - 1 else ''}"
        text = f"{authors}. {self.article.title}. {self.journal.name}. {self.volume.year} {self.format_month(self.issue.month) if self.issue.month else ''};{self.extract_num(self.volume.name)}({self.extract_num(self.issue.name)}):{self.article.page_from}-{self.article.page_to}."
        self.Vancouver = text

    def generate(self):
        self.apa()
        self.mla()
        self.chicago()
        self.harvard()
        self.vancouver()