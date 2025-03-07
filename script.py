import requests
import csv
import re
import argparse

def fetch_research_papers(query, max_results=10, debug=False):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print("Error fetching data from PubMed API.")
        return []
    
    data = response.json()
    
    if debug:
        print("ESearch Response:", data)
    
    paper_ids = data.get("esearchresult", {}).get("idlist", [])
    if not paper_ids:
        return []
    
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json"
    }
    summary_response = requests.get(fetch_url, params=fetch_params)
    if summary_response.status_code != 200:
        print("Error fetching summary data from PubMed API.")
        return []
    
    summary_data = summary_response.json()
    
    if debug:
        print("ESummary Response:", summary_data)
    
    papers = []
    for paper_id in paper_ids:
        result = summary_data.get("result", {}).get(paper_id, {})
        title = result.get("title", "N/A")
        pub_date = result.get("pubdate", "N/A")
        authors = result.get("authors", [])
        
        non_academic_authors = []
        company_affiliations = []
        corresponding_author_email = "N/A"
        
        if not isinstance(authors, list):
            authors = []
        
        for author in authors:
            affil = author.get("affiliation", "").lower() if author.get("affiliation") else ""
            if re.search(r"(pharma|biotech|therapeutics|biosciences|laboratories|scientific)", affil):
                non_academic_authors.append(author.get("name", "Unknown"))
                company_affiliations.append(author.get("affiliation", "Unknown"))
            
            if "corresponding author" in affil:
                corresponding_author_email = author.get("email", "N/A")
        
        papers.append([paper_id, title, pub_date, ", ".join(non_academic_authors) if non_academic_authors else "N/A", ", ".join(company_affiliations) if company_affiliations else "N/A", corresponding_author_email])
    
    return papers

def save_to_csv(papers, filename, debug=False):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["PubMed ID", "Title", "Publication Date", "Non-Academic Author", "Company Affiliation", "Corresponding Author Email"])
        writer.writerows(papers)
    
    if debug:
        print(f"Successfully saved {len(papers)} papers to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed based on a query.")
    parser.add_argument("query", type=str, help="PubMed query string")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, default="research_papers.csv", help="Specify output CSV file name")
    args = parser.parse_args()
    
    results = fetch_research_papers(args.query, max_results=20, debug=args.debug)
    save_to_csv(results, args.file, debug=args.debug)
    print("CSV file has been successfully generated.")

if __name__ == "__main__":
    main()