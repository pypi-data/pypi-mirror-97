
# if a txt file and a query file are given, then index the txt file as in indexer.py and query that output.
# if only a query file is given, then query 'index.txt' in the current directory.





def print_results(queryno,
                  results):  # formats the list of results per query to TREC format for boolean, phrase and proximity queries

    query_results = []
    if len(results) > 0:
        for documentnumber in results:
            output_string = "{} 0 {} 0 1 0".format(queryno, documentnumber)
            query_results.append(output_string)

    return query_results


def print_results_IR(queryno, results):  # formats the list of results per query to TREC format for rank queries

    query_results = []
    results_c = results.copy()
    for doc, score in results_c.items():
        if score == 0.0:
            results.pop(doc)
    results = (sorted(results.items(), key=lambda kv: kv[1], reverse=True))
    for item in results:
        doc, score = item
        output = "{} 0 {} 0 {} 0".format(queryno, doc, round(score, 3))
        query_results.append(output)

    return query_results


# Query in list format, preprocesses

def parsequery(queryno, query):
    results = []  # list of positions
    querytype = "not_ir"  # variable used to decide which print/save method to use for rank or bool/phrase query
    results_string = []

    # check structure of query to send to appropriate search method

    if 'AND' in query or 'OR' in query:
        results = boolean_search(query)

    elif query.startswith('#') and query.endswith(")"):
        results = proximitysearch(query)

    elif query.startswith('"') and query.endswith('"'):
        positions = phrasesearch(1, query)
        t = []
        for p in positions:
            for key in p:
                t.append(key)
        results.extend(list(set(t)))

    elif len(query.split(' ')) == 1:  # single word query
        for item in getpositions(query):
            for key in item.keys():
                results.append(key)
    else:
        querytype = "IR"
        results = rankedir_search(query)

    if querytype == "IR":
        query = preprocess_query(query)
        results_string.append(print_results_IR(queryno, results))
    else:
        results_string.append(print_results(queryno, results))

    return list(chain.from_iterable(results_string))


if __name__ == '__main__':

    print("\nANSWERING QUERIES\n...")

    output = []

    for query in query_file:
        queryno = int(query.split()[0])
        query = query.lstrip(digits).strip()
        results_string = parsequery(queryno, query)

        if len(results_string) > 1000:  # only print out first 1000 queries
            results_string = results_string[:1000]

        if len(results_string) > 0:
            output.append(results_string)

    # save to file

    output = list(chain.from_iterable(output))
    f = open('results.txt', 'w')

    for line in output:
        f.write(line + "\n")
    f.close()

    print("QUERYING COMPLETE\n")