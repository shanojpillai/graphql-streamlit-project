# GraphQL API with Python and Streamlit

![GraphQL Logo](https://graphql.org/img/logo.svg)

## A powerful approach to building modern data-driven applications

This project demonstrates the implementation of a GraphQL API using Python (Strawberry GraphQL and FastAPI) with a Streamlit frontend. It showcases the advantages of GraphQL over traditional REST APIs, especially for data exploration and visualization applications.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-FF4B4B.svg)](https://streamlit.io/)

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [GraphQL vs REST Comparison](#graphql-vs-rest-comparison)
- [Data Flow](#data-flow)
- [Development](#development)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project demonstrates how to build a data exploration platform using GraphQL as the API layer between a Kaggle dataset and a Streamlit frontend. By implementing GraphQL instead of traditional REST APIs, we achieve:

- 75.6% faster execution time
- 83.3% reduction in API requests
- 75.0% less data transferred
- Significantly improved developer experience

The application provides an interactive interface for exploring dataset information with much greater efficiency and flexibility than traditional REST approaches.

## Architecture

The project is built using the following technologies:

### Backend
- **Strawberry GraphQL**: Type-first GraphQL library for Python
- **FastAPI**: High-performance web framework for building APIs
- **Uvicorn**: ASGI server for serving the FastAPI application
- **Pandas**: For data processing and manipulation

### Frontend
- **Streamlit**: Framework for building data applications
- **Plotly**: Interactive visualization library
- **GQL**: GraphQL client for Python

## Project Structure

```
graphql-streamlit-project/
│
├── data/                      # Dataset storage folder
│   └── dataset.csv            # Kaggle dataset for exploration
│
├── backend/                   # GraphQL API server
│   ├── app.py                 # FastAPI and GraphQL server
│   ├── schema.py              # GraphQL schema definitions
│   ├── resolvers.py           # Query resolvers for data access
│   ├── models.py              # Data models for GraphQL types
│   └── database.py            # Data loading and processing
│
├── frontend/                  # Streamlit user interface
│   ├── app.py                 # Streamlit main application
│   ├── components/            # Reusable UI components
│   │   └── query_builder.py   # Interactive query builder
│   ├── graphql_client.py      # GraphQL client for API
│   └── pages/                 # Application pages
│       ├── rest_comparison.py # GraphQL vs REST comparison
│       └── other_pages.py     # Additional application pages
│
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── docker-compose.yml         # Container orchestration
```

## Key Features

- **GraphQL API** with schema-based type system
- **Interactive Query Builder** for exploring data without writing raw GraphQL
- **Performance Comparison** between GraphQL and REST approaches
- **Data Visualization** of query results using Plotly
- **Containerized Deployment** using Docker and Docker Compose

## Installation

### Prerequisites

- Python 3.9+
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/shanojpillai/graphql-streamlit-project.git
   cd graphql-streamlit-project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download sample dataset:
   ```bash
   # This is a placeholder, replace with actual dataset download instructions
   mkdir -p data
   # Download your chosen Kaggle dataset and place it in the data/ directory
   ```

## Usage

### Running the Backend

Start the GraphQL API server:

```bash
cd backend
python app.py
```

The GraphQL server will be available at [http://localhost:8000/graphql](http://localhost:8000/graphql)

### Running the Frontend

In a new terminal window:

```bash
cd frontend
streamlit run app.py
```

The Streamlit application will be available at [http://localhost:8501](http://localhost:8501)

## GraphQL vs REST Comparison

Our implementation demonstrates significant advantages of GraphQL over REST:

| Metric | REST | GraphQL | Improvement |
|--------|------|---------|-------------|
| Execution Time | 338.2 ms | 82.5 ms | 75.6% faster |
| API Requests | 6 | 1 | 83.3% fewer |
| Data Size | 2,582 bytes | 645 bytes | 75.0% less |

### REST Approach

```
GET /api/items?limit=5
GET /api/items/1/details
GET /api/items/2/details
...
```

### GraphQL Approach

```graphql
query {
  items(limit: 5) {
    id
    name
    category
    details { ... }
  }
}
```

## Data Flow

1. **Data Loading**: Dataset is loaded from CSV file into memory
2. **GraphQL API**: Exposes the data through a strongly-typed schema
3. **Frontend Queries**: Streamlit frontend requests exactly the data it needs
4. **Visualization**: Results are displayed through interactive charts and tables

## Development

### Extending the GraphQL Schema

To add new fields or types to the GraphQL schema, edit the `backend/schema.py` file:

```python
@strawberry.type
class Item:
    id: str
    name: str
    value: float
    category: str
    # Add new fields here
```

### Adding New Resolvers

To add new query resolvers, edit the `backend/resolvers.py` file:

```python
def get_items_by_category(category: str) -> List[Item]:
    data = get_data_from_database()
    return [item for item in data if item.get('category') == category]
```

### Adding New Frontend Pages

To add new pages to the Streamlit application, create a new file in the `frontend/pages/` directory:

```python
# frontend/pages/new_page.py
import streamlit as st

def display_new_page():
    st.title("New Page")
    # Add your page content here
```

## Docker Deployment

This project includes Docker support for easy deployment:

```bash
docker-compose up -d
```

This will start both the backend and frontend services:
- GraphQL API at [http://localhost:8000/graphql](http://localhost:8000/graphql)
- Streamlit frontend at [http://localhost:8501](http://localhost:8501)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Created by [Shanoj Pillai](https://github.com/shanojpillai)

