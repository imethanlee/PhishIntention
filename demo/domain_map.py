import pickle


if __name__ == "__main__":
    def add_domain(key, domain_list):
        if key not in domain_map.keys():
            domain_map[key] = domain_list

    with open('./phishintention/src/phishpedia_siamese/domain_map.pkl', 'rb') as handle:    
        domain_map = pickle.load(handle)

    add_domain('DBS Bank', ['dbs'])
    add_domain('Oversea Chinese Banking Corporation', ['ocbc'])
    add_domain('United Overseas Bank', ['uobgroup', 'uob'])
    add_domain('Bank of Singapore', ['bankofsingapore'])
    add_domain('Citi Bank', ['citibank'])
    add_domain('CIC', ['dbs'])
    # add_domain('hsbc', ['hsbc'])
    add_domain('Maybank', ['maybank2u'])
    # add_domain('standard_chartered', ['sc'])
    add_domain('RHB Bank', ['rhbgroup'])


    with open('./phishintention/src/phishpedia_siamese/domain_map.pkl', 'wb') as handle:    
        pickle.dump(domain_map, handle)

    print(domain_map)