from PIL import ImageMode
import os
import dotenv
from google import genai
from google.genai.errors import APIError
#Setup & Environment
dotenv.load_dotenv()
client = genai.Client()

#Pricing
INPUT_RATE_PER_M = 0.30
OUTPUT_RATE_PER_M = 2.50

#Cost Calculation Function
def cost_Calculation(in_tokens: int, Out_tokens: int) -> float:
    input_cost = (in_tokens / 1000000) * INPUT_RATE_PER_M
    output_cost = (Out_tokens / 1000000) * OUTPUT_RATE_PER_M
    return input_cost + output_cost

#Multi turn chat session
chat = client.chats.create(model="gemini-2.5-flash")
print("Gemini Chatbot initialized. Type 'quit' to exit.\n" + "-" * 40)

#interaction
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    if not user_input:
        continue

    try:
        print("Gemini: thinking...", end="\r")
        
        response = chat.send_message(user_input)

        #Get Token usage
        usage = response.usage_metadata
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        total_tokens = usage.total_token_count

        #Calculate cost
        estimated_cost = cost_Calculation(input_tokens, output_tokens)

        #Display response
        print("\n" + "="*40)
        print("Gemini: " + response.text)
        print("="*40)
        print("\n" + "Token Statistics:")
        print(f"- Input tokens: {input_tokens}")
        print(f"- Output tokens: {output_tokens}")
        print(f"- Total tokens: {total_tokens}")
        print(f"- Estimated cost: ${estimated_cost:.8f}")

    except APIError as e:
        print(f"\nAPI Error: {e}")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")

print("\n" + "-"*40)