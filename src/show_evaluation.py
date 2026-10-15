import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

project_name = os.getenv("LANGSMITH_PROJECT")

print(Client().share_dataset(dataset_name=f"{project_name}-eval")["url"])
