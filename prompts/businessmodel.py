import google.generativeai as genai

genai.configure(api_key="AIzaSyBZhIcMakEwzjtkUgv1gV096tHlsEoxWfc")

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

message = f"""Product: Organic Food, Target Customer Demographic: Teenagers, Initial Investment: 25,000 rupees, Goals of the Company: Well Rounded Diet, Tendency of taking Risk: Very Likely."""

message2 = f"""Interests: Gym, Diet, Yoga, Healthy Living, Concerns: Low Salary """

convo = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    """As a business analyst/mentor, you will be provided with information on Product, Target Customer Demographic, Initial Investment, Goals of the Company, and Likelihood of taking Risk. 
                    Provide a brief business report where each element is as specified:
                    A: 1 line on a general comment about overall business, include if budget is enough or too much. If insufficient budget, provide a more realistic budget. (datatype = string).
                    B: Many different possible Risks involved in this business (datatype = list).
                    C: Names of existing competitors, if any. If not, then mention that it is an innovative idea (datatype = list).
                    D: Existing Techonology that could help aid the business (datatype = list).
                    E: Effective Marketing Strategy for the business (datatype = list).
                    
                    OUTPUT FORMAT: [A,B,C,D,E]
                                        
                    If any data is NOT AVAILABLE, ignore it and provide feedback on the rest.
                    Provide very innovative suggestions if tendency of taking risk is high."""
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Okay, provide me with the company information. I will provide in the format required as to my best knowledge."
                ],
            },
            {
                "role": "user",
                "parts": [
                    """
                    "Product: Shampoo for colored hair, Target Customer Demographic: Young Women, Initial Investment: 25,000 rupees, Goals of the Company: Make Best Shampoo for Damage Free Hair, Tendency of taking Risk: Unlikely."
                    """
                ],
            },
            {
                "role": "model",
                "parts": [
                    """[This business venture appears to NOT have great potential as it is a saturated market and budget is also quite low, [Market competition, Product differentiation, Ingredient costs, Lack of brand awareness], [Tresemme, L'Oréal, Olaplex, Pantene, Dove, Redken], [Customer relationship management (CRM) systems, E-commerce platforms, Ingredient analysis software], [Target specific hair salons, Influencer marketing, Discounts and Promotions, Create a loyalty program]]"""
                ],
            },
            {
                "role": "user",
                "parts": [
                    """
                    "Product: Baby food, Target Customer Demographic: Young Women, Initial Investment: 2,50,000 rupees, Goals of the Company: Make Healthiest Baby Food, Tendency of taking Risk: Likely."
                    """
                ],
            },
            {
                "role": "model",
                "parts": [
                    """[This business venture appears to have good potential for success and the budget seems sufficient, but there are some risks to consider., ['Market competition', 'Product differentiation', 'Changes in Consumer Preference', 'Fluctuating Product Costs'], ['Gerber', 'Earth's Best', 'Beech-Nut'], ['Automated inventory management systems', 'Nutritional analysis software', 'Online ordering platforms', 'Customer relationship management (CRM) systems', 'E-commerce platforms'], ['Social media marketing to reach young mothers','Partnerships with healthcare professionals','Target specific baby stores', 'Influencer marketing']]"""
                ],
            }
        ]
)

convo.send_message(message)
print(convo.last.text)

convo_career = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    """Based on the interests and concerns of the user, provide career advice suitable for them."""
                ]
            },
            {
                "role": "model",
                "parts": [
                    """Okay, provide me with the information. I will provide the required suggestions to the best of my knowledge."""
                ],
            }
        ]
)

convo_career.send_message(message2)
print(convo_career.last.text)