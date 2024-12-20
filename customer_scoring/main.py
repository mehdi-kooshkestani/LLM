from math import sqrt
from typing import Dict, List
from autogen import ConversableAgent
import sys
import os

def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    # TODO
    # This function takes in a restaurant name and returns the reviews for that restaurant. 
    # The output should be a dictionary with the key being the restaurant name and the value being a list of reviews for that restaurant.
    # The "data fetch agent" should have access to this function signature, and it should be able to suggest this as a function call. 
    # Example:
    # > fetch_restaurant_data("Applebee's")
    # {"Applebee's": ["The food at Applebee's was average, with nothing particularly standing out.", ...]}
    # Read the file and process each line
    restaurant_dict = {}

    with open("restaurant-data.txt", "r", encoding="utf-8") as file:
        for line in file:
            # Split the line at the first dot (.)
            restaurant, comment = line.split('.', 1)
            restaurant = restaurant.strip()
            comment = comment.strip()

            # Append the comment to the restaurant's list in the dictionary
            if restaurant in restaurant_dict:
                restaurant_dict[restaurant].append(comment)
            else:
                restaurant_dict[restaurant] = [comment]

    # Output the dictionary
    # print(restaurant_dict[restaurant_name])
    return {restaurant_name: restaurant_dict[restaurant_name]}

    # pass


def calculate_overall_score(restaurant_name: str, food_scores: List[int], customer_service_scores: List[int]) -> Dict[str, float]:
    # TODO
    # This function takes in a restaurant name, a list of food scores from 1-5, and a list of customer service scores from 1-5
    # The output should be a score between 0 and 10, which is computed as the following:
    # SUM(sqrt(food_scores[i]**2 * customer_service_scores[i]) * 1/(N * sqrt(125)) * 10
    # The above formula is a geometric mean of the scores, which penalizes food quality more than customer service. 
    # Example:
    # > calculate_overall_score("Applebee's", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    # {"Applebee's": 5.048}
    # NOTE: be sure to that the score includes AT LEAST 3  decimal places. The public tests will only read scores that have 
    # at least 3 decimal places.
    # Ensure both lists have the same length
    if len(food_scores) != len(customer_service_scores):
        raise ValueError("Food scores and customer service scores must have the same length.")

    # Number of scores
    N = len(food_scores)

    # Calculate the overall score
    score_sum = sum(sqrt(food_scores[i] ** 2 * customer_service_scores[i]) for i in range(N))
    normalized_score = score_sum / (N * sqrt(125)) * 10

    # Return the result as a dictionary
    return {restaurant_name: round(normalized_score, 3)}
    # pass

def get_data_fetch_agent_prompt(restaurant_query: str) -> str:
    # TODO
    # It may help to organize messages/prompts within a function which returns a string. 
    # For example, you could use this function to return a prompt for the data fetch agent 
    # to use to fetch reviews for a specific restaurant.
    # pass
    """
    Generates a prompt string for the data fetch agent to fetch reviews for a specific restaurant.

    Args:
        restaurant_query (str): The name of the restaurant to query.

    Returns:
        str: A prompt string instructing the data fetch agent to fetch reviews for the restaurant.
    """
    return (
        f"Please fetch detailed reviews and customer feedback for the restaurant named '{restaurant_query}'. "
        "Include information about food quality, customer service, ambiance, and overall experience. "
        "Ensure the data is comprehensive and includes both positive and negative reviews for balanced insight."
    )

# TODO: feel free to write as many additional functions as you'd like.

# Do not modify the signature of the "main" function.
def main(user_query: str):
    entrypoint_agent_system_message = "You are the entry point agent responsible for coordinating with other agents to answer user queries about restaurants. When a user asks about a restaurant, ensure to fetch relevant reviews, analyze them, and calculate an overall score." # TODO
    # example LLM config for the entrypoint agent
    # llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("sk-4eCk0A2z8GHw2h9R123aAB12CDE3FgH4J1K2")}]}
    # the main entrypoint/supervisor agent
    entrypoint_agent = ConversableAgent("entrypoint_agent", 
                                        system_message=entrypoint_agent_system_message, 
                                        llm_config=llm_config)
    entrypoint_agent.register_for_llm(name="fetch_restaurant_data", description="Fetches the reviews for a specific restaurant.")(fetch_restaurant_data)
    entrypoint_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)

    # TODO
    # Create more agents here.
    # Define review analyzer agent system message
    review_analyzer_system_message = (
        "You are a review analysis agent. Your task is to analyze restaurant reviews and extract two scores from each review: "
        "'food_score' and 'customer_service_score'. Use the following guidelines: "
        "1: awful, horrible, disgusting; 2: bad, unpleasant, offensive; 3: average, uninspiring, forgettable; "
        "4: good, enjoyable, satisfying; 5: awesome, incredible, amazing."
    )

    # Create the review analyzer agent
    review_analyzer_agent = ConversableAgent(
        "review_analyzer_agent",
        system_message=review_analyzer_system_message,
        llm_config=llm_config,
    )

    # Define scoring agent system message
    scoring_agent_system_message = (
        "You are a scoring agent responsible for calculating the overall score for a restaurant based on extracted food and customer service scores. "
        "Use the calculate_overall_score function to compute the final score."
    )

    # Create the scoring agent
    scoring_agent = ConversableAgent(
        "scoring_agent",
        system_message=scoring_agent_system_message,
        llm_config=llm_config,
    )

    # Register the scoring function with the scoring agent
    scoring_agent.register_for_execution(name="calculate_overall_score")(calculate_overall_score)

    
    # TODO
    # Fill in the argument to `initiate_chats` below, calling the correct agents sequentially.
    # If you decide to use another conversation pattern, feel free to disregard this code.
    
    # Uncomment once you initiate the chat with at least one agent.
    # result = entrypoint_agent.initiate_chats([{}])
    # Initiate chats sequentially between agents
    result = entrypoint_agent.initiate_chats([
        {
            "agent": review_analyzer_agent,
            "arguments": {
                "restaurant_query": user_query,
                "fetch_reviews": {
                                    "function_name": "fetch_restaurant_data",
                                    "args": {"restaurant_name": user_query},
                                 },
            },
        },
        {
            "agent": scoring_agent,
            "arguments": {
                "restaurant_name": user_query,
                "food_scores": "{context: food_scores from review_analyzer_agent}",
                "customer_service_scores": "{context: customer_service_scores from review_analyzer_agent}",
            },
        },
    ])
    print(result)
    
# DO NOT modify this code below.
if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query for some restaurant when executing main."
    main(sys.argv[1])


 ########################################################################
# def main(user_query: str):
    # # Entry point agent system message
    # entrypoint_agent_system_message = (
    #     "You are the entry point agent responsible for coordinating with other agents to answer user queries about restaurants. "
    #     "When a user asks about a restaurant, ensure to fetch relevant reviews, analyze them, and calculate an overall score."
    # )

    # # LLM configuration for agents
    # llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}

    # # Create the main entrypoint agent
    # entrypoint_agent = ConversableAgent(
    #     "entrypoint_agent",
    #     system_message=entrypoint_agent_system_message,
    #     llm_config=llm_config,
    # )

    # # Register the data fetching function
    # entrypoint_agent.register_for_llm(name="fetch_restaurant_data", description="Fetches the reviews for a specific restaurant.")(fetch_restaurant_data)
    # entrypoint_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)

    # # Define review analyzer agent system message
    # review_analyzer_system_message = (
    #     "You are a review analysis agent. Your task is to analyze restaurant reviews and extract two scores from each review: "
    #     "'food_score' and 'customer_service_score'. Use the following guidelines: "
    #     "1: awful, horrible, disgusting; 2: bad, unpleasant, offensive; 3: average, uninspiring, forgettable; "
    #     "4: good, enjoyable, satisfying; 5: awesome, incredible, amazing."
    # )

    # # Create the review analyzer agent
    # review_analyzer_agent = ConversableAgent(
    #     "review_analyzer_agent",
    #     system_message=review_analyzer_system_message,
    #     llm_config=llm_config,
    # )

    # # Define scoring agent system message
    # scoring_agent_system_message = (
    #     "You are a scoring agent responsible for calculating the overall score for a restaurant based on extracted food and customer service scores. "
    #     "Use the calculate_overall_score function to compute the final score."
    # )
    #
    # # Create the scoring agent
    # scoring_agent = ConversableAgent(
    #     "scoring_agent",
    #     system_message=scoring_agent_system_message,
    #     llm_config=llm_config,
    # )

    # # Register the scoring function with the scoring agent
    # scoring_agent.register_for_execution(name="calculate_overall_score")(calculate_overall_score)

    # # Initiate chats sequentially between agents
    # result = entrypoint_agent.initiate_chats([
    #     {
    #         "agent": review_analyzer_agent,
    #         "arguments": {
    #             "restaurant_query": user_query,
    #             "fetch_reviews": entrypoint_agent.initiate_chat(
    #                 {"function_name": "fetch_restaurant_data", "args": {"restaurant_name": user_query}}
    #             ),
    #         },
    #     },
    #     {
    #         "agent": scoring_agent,
    #         "arguments": {
    #             "restaurant_name": user_query,
    #             "food_scores": "{context: food_scores from review_analyzer_agent}",
    #             "customer_service_scores": "{context: customer_service_scores from review_analyzer_agent}",
    #         },
    #     },
    # ])

    # print(result)
