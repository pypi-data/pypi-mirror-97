

class Claim:
    def __init__(self, claim_soup):
        self.soup = claim_soup
        print(claim_soup)
        self.id = self.soup.get('id')
        self.number = self.soup.get('num')
        claim_ref = self.soup.find('claim-ref')
        if claim_ref:
            self.parent_id = claim_ref.get('idref')
        self.text = self.soup.text





