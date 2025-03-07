# backend_takehome_using_python

[tool.poetry]
name = "pubmed-fetcher"
version = "0.1.0"
description = "A command-line tool to fetch research papers from PubMed."
authors = ["Your Name <your.email@example.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.26.0"

[tool.poetry.scripts]
pubmed-fetcher = "pubmed_fetcher:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# README.md content
def generate_readme():
    readme_content = """
# PubMed Fetcher

A command-line tool to fetch research papers from PubMed and extract relevant author affiliations.

## Features
- Fetches research papers using PubMed API
- Supports full PubMed query syntax
- Identifies non-academic authors affiliated with pharmaceutical or biotech companies
- Outputs results in CSV format
- Command-line options: `-h`, `-d`, `-f`

## Installation

1. Install [Poetry](https://python-poetry.org/docs/)
2. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/pubmed-fetcher.git
   cd pubmed-fetcher
   ```
3. Install dependencies:
   ```sh
   poetry install
   ```

## Usage

Run the program using:
```sh
poetry run pubmed-fetcher "cancer treatment" -f output.csv -d
```

## Dependencies
- Python 3.8+
- Requests library
- Poetry for dependency management

## License
MIT License
"""
    with open("README.md", "w") as f:
        f.write(readme_content)

# Generate README on script execution
generate_readme()


