import os
import json

from dotenv import load_dotenv

from openai import OpenAI
import gradio as gr

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-4o-mini"
openai = OpenAI()

system_message = """You are a helpful assistant for an Airline called FlightAI. 
You help customers with flight information, ticket prices, and travel-related questions.
Give courteous and helpful answers. Always be accurate. If you don't know the answer, say so.

Here are some examples of how you should respond:

Example 1:
Customer: "How much is a ticket to Paris?"
Assistant: I'll check the ticket price to Paris for you.
[Tool call: get_ticket_price with destination_city: "Paris"]
Assistant: A return ticket to Paris costs $899.

Example 2:
Customer: "I want to travel somewhere for under $600. What options do I have?"
Assistant: Let me check our available destinations for you. Based on our current prices, Berlin is available for $499, which is under your $600 budget. This is a great European destination with rich history and culture!

Example 3:
Customer: "What's the cheapest destination you offer?"
Assistant: Let me check all our destination prices for you. The most affordable destination we offer is Berlin at $499 for a return ticket.

Example 4:
Customer: "Can you tell me about Tokyo?"
Assistant: I'd be happy to help! Tokyo is one of our destinations with return tickets priced at $1400. However, I don't have detailed travel information about Tokyo. For specific details about attractions, weather, or travel requirements, I'd recommend checking with our travel specialists or official travel guides.

Remember to:
- Always use the get_ticket_price function when customers ask about specific destination prices
- Be helpful and suggest alternatives when appropriate
- Acknowledge limitations when you don't have specific information
- Maintain a friendly, professional airline customer service tone"""

ticket_prices = {
    "london": "$799", 
    "paris": "$899", 
    "tokyo": "$1400", 
    "berlin": "$499", 
    "hochiminh": "$1500"
}

# Additional context for destinations
destination_info = {
    "london": "A vibrant European capital with rich history and culture",
    "paris": "The City of Light, famous for art, fashion, and cuisine", 
    "tokyo": "A modern metropolis blending traditional and contemporary Japanese culture",
    "berlin": "Germany's capital with fascinating history and vibrant arts scene",
    "hochiminh": "Vietnam's bustling economic hub with rich cultural heritage"
}

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city' or wants to compare prices.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

# New function to get all available destinations and prices
destinations_function = {
    "name": "get_all_destinations",
    "description": "Get all available destinations with their prices. Use this when customers ask about available destinations, want to compare multiple prices, or ask for the cheapest/most expensive options.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
}

tools = [
    {"type": "function", "function": price_function},
    {"type": "function", "function": destinations_function}
]

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    price = ticket_prices.get(city, "Unknown")
    info = destination_info.get(city, "No additional information available")
    return {"price": price, "destination": destination_city, "info": info}

def get_all_destinations():
    print("Tool get_all_destinations called")
    destinations = []
    for city, price in ticket_prices.items():
        destinations.append({
            "city": city.title(),
            "price": price,
            "info": destination_info.get(city, "No additional information available")
        })
    return {"destinations": destinations}

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    if function_name == "get_ticket_price":
        city = arguments.get('destination_city')
        result = get_ticket_price(city)
        response = {
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        }
        return response, city
    
    elif function_name == "get_all_destinations":
        result = get_all_destinations()
        response = {
            "role": "tool", 
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        }
        return response, "all destinations"
    
    else:
        response = {
            "role": "tool",
            "content": json.dumps({"error": "Unknown function"}),
            "tool_call_id": tool_call.id
        }
        return response, "unknown"

def chat(message, history):
    # Convert gradio history format to OpenAI messages format if needed
    messages = [{"role": "system", "content": system_message}]
    
    for msg in history:
        if isinstance(msg, dict):
            messages.append(msg)
        else:
            # Handle gradio format [user_msg, assistant_msg]
            if len(msg) >= 2:
                messages.append({"role": "user", "content": msg[0]})
                if msg[1]:  # Only add assistant message if it exists
                    messages.append({"role": "assistant", "content": msg[1]})
    
    messages.append({"role": "user", "content": message})
    
    try:
        response = openai.chat.completions.create(
            model=MODEL, 
            messages=messages, 
            tools=tools,
            temperature=0.7
        )

        if response.choices[0].finish_reason == "tool_calls":
            message_with_tool_call = response.choices[0].message
            tool_response, context = handle_tool_call(message_with_tool_call)
            
            messages.append(message_with_tool_call)
            messages.append(tool_response)
            
            # Get final response after tool call
            final_response = openai.chat.completions.create(
                model=MODEL, 
                messages=messages,
                temperature=0.7
            )
            return final_response.choices[0].message.content
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error in chat function: {e}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again later."


if __name__ == "__main__":
    print("Starting FlightAI Assistant...")
    interface = gr.ChatInterface(
        fn=chat, 
        type="messages",
        title="✈️ FlightAI Assistant",
        description="Welcome to FlightAI! I can help you with flight prices and destination information. Try asking me about ticket prices, available destinations, or travel recommendations!",
        examples=[
            "How much is a ticket to Paris?",
            "What's the cheapest destination?", 
            "Show me all available destinations",
            "I have a budget of $800, what can you recommend?",
            "Tell me about Tokyo"
        ],
        theme="soft"
    )
    interface.launch(share=False)