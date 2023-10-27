from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.openai_functions import create_openai_fn_chain

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

database = [
    {"name": "Salami", "price": 9.99},
    {"name": "Margherita", "price": 8.99},
    {"name": "Pepperoni", "price": 10.99},
    {"name": "Hawaiian", "price": 11.49},
    {"name": "Veggie Supreme", "price": 10.49},
]


def get_pizza_info(pizza_name: str) -> dict:
    """Retrieve information about a specific pizza from the database.

    Args:
        pizza_name (str): Name of the pizza.

    Returns:
        dict: A dictionary containing the pizza's name and price or a message indicating the pizza wasn't found.
    """
    for pizza in database:
        if pizza["name"] == pizza_name:
            return pizza
    return {"message": f"No pizza found with the name {pizza_name}."}


def add_pizza(pizza_name: str, price: float) -> dict:
    """Add a new pizza to the database.

    Args:
        pizza_name (str): Name of the new pizza.
        price (float): Price of the new pizza.

    Returns:
        dict: A message indicating the result of the addition.
    """
    for pizza in database:
        if pizza["name"] == pizza_name:
            return {"message": f"Pizza {pizza_name} already exists in the database."}

    database.append({"name": pizza_name, "price": price})
    return {"message": f"Pizza {pizza_name} added successfully!"}


llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)

template = """You are an AI chatbot having a conversation with a human.

Human: {human_input}
AI: """
prompt = PromptTemplate(input_variables=["human_input"], template=template)


chain = create_openai_fn_chain([get_pizza_info, add_pizza], llm, prompt, verbose=True)


# result1 = chain.run("I want to add the pizza 'Jumbo' for 13.99")
# print(result1)
result2 = chain.run("Who are the main characters of the A-Team?")
print(result2)

# result3 = chain.run("How much does the Jumbo pizza cost?")
# print(result3)
