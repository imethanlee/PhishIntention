import dnstwist
import json
import os


class TypoSquatting:
    def __init__(self) -> None:
        self.main_path = os.path.join(os.getcwd(), "demo")
        self.json_path = os.path.join(self.main_path, "typo_squatting.json")
        # print(self.main_path)
        self.result = {}

    def _run_one_domain(self, domain_name, domain_url_list):
        data = []
        for domain_url in domain_url_list:
            data += dnstwist.run(domain=domain_url, registered=True, format='null')
        self.result[domain_name] = data

    def run(self, domain_dict):
        for key in domain_dict.keys():
            self._run_one_domain(domain_name=key, domain_url_list=domain_dict[key])
        self.save_to_json()

    def save_to_json(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.result, f, indent=4)

    def read_from_json(self):
        with open(self.json_path, 'r') as f:
            self.result = json.load(f)
        return self.result

    def get_typosquatting_domains(self, domain):
        """
        TODO: generate typosquatting domains result from a single legit domain input
        """
        data = dnstwist.run(domain=domain, registered=True, format='null')
        


if __name__ == "__main__":
    domain_dict = {
        "DBS Group": ["https://www.dbs.com.sg/"],
        "Overseas Chinese Banking Corporation": ["https://www.ocbc.com/"],
        "United Overseas Bank": ["https://www.uobgroup.com/", "https://www.uob.com.sg/"],
        "Bank of Singapore": ["https://www.bankofsingapore.com/"],
        "Citibank Singapore":  ["https://www.citibank.com.sg/"],
        "CIC Singapore": ["https://www.cic.asia/"],
        "HSBC Singapore": ["https://www.hsbc.com.sg/"],
        "Maybank Singapore": ["https://www.maybank2u.com.sg/"],
        "Standard Chartered Bank": ["https://www.sc.com/sg/"],
        "RHB Bank": ["https://rhbgroup.com.sg/"],
    }

    # ts = TypoSquatting()
    # ts.run(domain_dict)
    # js = ts.read_from_json()

    # for key in js.keys():
    #     for item in js[key]:
    #         print(item)


