# GraphQL with Python and Streamlit

Python application showcasing GraphQL vs REST APIs using Kaggle datasets. Features Strawberry GraphQL backend with Streamlit frontend for interactive data exploration and visualization.

## Project Structure

```
graphql-streamlit-project/
├── README.md
├── .gitignore
├── requirements.txt
├── data/                    # Dataset files
├── backend/
│   ├── app.py               # Main GraphQL server
│   ├── schema.py            # GraphQL schema definitions
│   ├── resolvers.py         # Query resolvers
│   ├── models.py            # Data models
│   └── database.py          # Data loading/processing
└── frontend/
    ├── app.py               # Streamlit application
    ├── components/          # Reusable UI components
    ├── graphql_client.py    # GraphQL client setup
    └── pages/               # Different pages of the app
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/shanojpillai/graphql-streamlit-project.git
   cd graphql-streamlit-project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the GraphQL server:
   ```
   cd backend
   python app.py
   ```

5. In a new terminal, start the Streamlit app:
   ```
   cd frontend
   streamlit run app.py
   ```

## Kaggle Dataset

[Description of the dataset you choose will go here]

## Features

- GraphQL API with queries and mutations
- Interactive Streamlit frontend
- Data visualizations
- Query comparison (GraphQL vs REST)

## License

[Your license choice]
