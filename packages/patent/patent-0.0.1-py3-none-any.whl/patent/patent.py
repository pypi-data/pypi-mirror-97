
import requests
from bs4 import BeautifulSoup
from .claim import Claim


class Patent:
    def __init__(self, number, language='en'):
        self.number = number
        self.language = language
        self.soup = BeautifulSoup(
            requests.get('https://patents.google.com/patent/' + self.number + '/' + self.language).text,
            'html.parser'
        )
        # Meta Data
        self.head = self.soup.find('head')
        self.title = self.head.find('meta', {'name': 'DC.title'}).get('content')
        self.submission_date = self.head.find('meta', {'name': 'DC.date', 'scheme': 'dateSubmitted'}).get('content')
        self.issue_date = self.head.find('meta', {'name': 'DC.date', 'scheme': 'issue'}).get('content')
        self.description = self.head.find('meta', {'name': 'DC.description'}).get('content')
        self.contributors = [contributor.get('content') for contributor in
                             self.head.find_all('meta', {'name': 'DC.contributor'})]
        self.inventors = [inventor.get('content') for inventor in
                          self.head.find_all('meta', {'name': 'DC.contributor', 'scheme': 'inventor'})]
        self.current_assignee = self.head.find('meta', {'name': 'DC.contributor', 'scheme': 'assignee'}).get('content')
        self.patent_citations = [patent_citation.get('content') for patent_citation in
                                 self.head.find_all('meta', {'name': 'DC.relation', 'scheme': 'references'})]
        self.non_patent_citations = [non_patent_citation.get('content') for non_patent_citation in
                                     self.head.find_all('meta', {'name': 'citation_reference', 'scheme': 'references'})]

        # Claims
        self.claims = {}
        dependent_claim_soups = [dependent_claim_holder.find('div', {'class': 'claim'}) for dependent_claim_holder in
                                 self.soup.find_all('div', {'class': 'claim-dependent'})]
        dependent_claim_soups.sort(key=lambda claim_soup: claim_soup.get('num'), reverse=True)
        for dependent_claim_soup in dependent_claim_soups:
            if dependent_claim_soup.get('id') not in self.claims.keys():
                self.claims[dependent_claim_soup.get('id')] = Claim(dependent_claim_soup)

        independent_claim_ids = []
        independent_claim_soups = []
        for claim in self.claims.values():
            if claim.parent_id not in self.claims.keys():
                if claim.parent_id not in independent_claim_ids:
                    independent_claim_soup = self.soup.find('div', {'id': claim.parent_id, 'class': 'claim'})
                    independent_claim_soups.append(independent_claim_soup)
                    independent_claim_ids.append(claim.parent_id)

        for independent_claim_soup in independent_claim_soups:
            self.claims[independent_claim_soup.get('id')] = Claim(independent_claim_soup)

    def get_cited_patents(self):
        return [Patent(patent_citation) for patent_citation in self.patent_citations]




