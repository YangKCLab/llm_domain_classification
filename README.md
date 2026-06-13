# LLM Domain Classification project

![logo](logo.png)

## Overview

As LLMs increasingly help curate and filter information in search engines, chatbots, and recommendation systems, their ability to accurately evaluate news sources directly impacts the quality and reliability of information they provide to users.
This project evaluates how well Large Language Models (LLMs) can assess the credibility and categorize news sources.

See our [dashboard](https://yangkclab.github.io/llm_domain_classification/) for the results and methods.

## Citation

If you find this project useful, please cite it as follows:

```bibtex
@inproceedings{yang2025accuracy,
    author = {Yang, Kai-Cheng and Menczer, Filippo},
    title = {Accuracy and Political Bias of News Source Credibility Ratings by Large Language Models},
    year = {2025},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3717867.3717903},
    doi = {10.1145/3717867.3717903},
    booktitle = {Proceedings of the 17th ACM Web Science Conference 2025},
    pages = {127–137},
    numpages = {11},
    series = {Websci '25}
}
```

# Technical Details

## Project Structure

```
project_root/
├── README.md
├── LICENSE
├── .gitignore
├── .env                          # API keys (NOT committed)
├── data/                         # Raw + processed model outputs
│   ├── source/                   # Source files
│   ├── intermediate/             # Intermediate files
│   └── processed/                # Analyzed and formatted data
├── backend/                      # Backend code
├── frontend/                     # Vue 3 + Vite app for the dashboard
└── .github/
    └── workflows/
        └── deploy-pages.yml      # build + push gh pages
```

## Backend

See [backend](backend) for details.

## Frontend

See [frontend](frontend) for details.

## Contributing

You are welcome to contribute to the project by opening an issue or a pull request.
Questions and requests can be sent to [Kai-Cheng Yang](mailto:yang3kc@gmail.com).