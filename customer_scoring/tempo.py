# restaurant_dict = {}
#
# with open("restaurant-data.txt", "r", encoding="utf-8") as file:
#     for line in file:
#         # Split the line at the first dot (.)
#         restaurant, comment = line.split('.', 1)
#         restaurant = restaurant.strip()
#         comment = comment.strip()
#
#         # Append the comment to the restaurant's list in the dictionary
#         if restaurant in restaurant_dict:
#             restaurant_dict[restaurant].append(comment)
#         else:
#             restaurant_dict[restaurant] = [comment]
#
# # Output the dictionary
# print(restaurant_dict)
# print("-----------------------------------------------")
# print(restaurant_dict["McDonald's"])
# print(len(restaurant_dict["McDonald's"]))
# restaurant_name="Applebee's"
# print({restaurant_name: restaurant_dict[restaurant_name]})

# from math import sqrt
# from typing import List, Dict
#
#
# def calculate_overall_score(restaurant_name: str, food_scores: List[int], customer_service_scores: List[int]) -> Dict[
#     str, float]:
#     # Ensure both lists have the same length
#     if len(food_scores) != len(customer_service_scores):
#         raise ValueError("Food scores and customer service scores must have the same length.")
#
#     # Number of scores
#     N = len(food_scores)
#
#     # Calculate the overall score
#     score_sum = sum(sqrt(food_scores[i] ** 2 * customer_service_scores[i]) for i in range(N))
#     normalized_score = score_sum / (N * sqrt(125)) * 10
#
#     # Return the result as a dictionary
#     return {restaurant_name: round(normalized_score, 3)}
#
#
# # Example usage
# result = calculate_overall_score("Applebee's", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
# print(result)  # Output: {"Applebee's": 5.048}
