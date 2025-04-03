from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from schema import schema
import uvicorn

# Create FastAPI app
app = FastAPI(title="GraphQL with Python Demo")

# Create GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to GraphQL with Python Demo",
        "documentation": "/graphql",
        "healthcheck": "/health"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)