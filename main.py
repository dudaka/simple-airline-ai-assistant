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

IMPORTANT: Our system can handle various city name formats. For example:
- Ho Chi Minh City can be called: "Ho Chi Minh", "HCMC", "Saigon", "Sai Gon"
- Always use the get_ticket_price function even if users use alternative city names

Here are some examples of how you should respond:

Example 1:
Customer: "How much is a ticket to Paris?"
Assistant: I'll check the ticket price to Paris for you.
[Tool call: get_ticket_price with destination_city: "Paris"]
Assistant: A return ticket to Paris costs $899.

Example 2:
Customer: "What's the price to Saigon?"
Assistant: I'll check the ticket price to Saigon for you.
[Tool call: get_ticket_price with destination_city: "Saigon"]
Assistant: A return ticket to Ho Chi Minh City (Saigon) costs $1500. Ho Chi Minh City is Vietnam's bustling economic hub with rich cultural heritage!

Example 3:
Customer: "I want to travel somewhere for under $600. What options do I have?"
Assistant: Let me check our available destinations for you. Based on our current prices, Berlin is available for $499, which is under your $600 budget. This is a great European destination with rich history and culture!

Example 4:
Customer: "What's the cheapest destination you offer?"
Assistant: Let me check all our destination prices for you. The most affordable destination we offer is Berlin at $499 for a return ticket.

Example 5:
Customer: "Can you tell me about HCMC?"
Assistant: I'll check the information for HCMC for you.
[Tool call: get_ticket_price with destination_city: "HCMC"]
Assistant: HCMC (Ho Chi Minh City) is available for $1500 for a return ticket. It's Vietnam's bustling economic hub with rich cultural heritage!

Remember to:
- Always use the get_ticket_price function when customers ask about specific destination prices
- Accept alternative city names and let the system normalize them
- Be helpful and suggest alternatives when appropriate
- Acknowledge limitations when you don't have specific information
- Maintain a friendly, professional airline customer service tone
- When a destination is not found, suggest available alternatives"""

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

# City name aliases for flexible user input
city_aliases = {
    # London variations
    "london": "london",
    "london city": "london",
    "greater london": "london",
    
    # Paris variations
    "paris": "paris",
    "paris city": "paris",
    "city of light": "paris",
    
    # Tokyo variations
    "tokyo": "tokyo",
    "tokyo city": "tokyo",
    "tokyo metropolitan": "tokyo",
    
    # Berlin variations
    "berlin": "berlin",
    "berlin city": "berlin",
    
    # Ho Chi Minh City variations
    "hochiminh": "hochiminh",
    "ho chi minh": "hochiminh",
    "ho chi minh city": "hochiminh",
    "hcmc": "hochiminh",
    "saigon": "hochiminh",
    "sai gon": "hochiminh",
    "ho chi minh ville": "hochiminh",
    "thanh pho ho chi minh": "hochiminh"
}

def normalize_city_name(city_input):
    """
    Normalize city name input to match our database keys.
    Handles various spellings and alternative names.
    """
    if not city_input:
        return None
    
    # Convert to lowercase and strip whitespace
    normalized = city_input.lower().strip()
    
    # Remove common prefixes/suffixes
    normalized = normalized.replace(" city", "").replace("city of ", "").strip()
    
    # Check direct matches in aliases
    if normalized in city_aliases:
        return city_aliases[normalized]
    
    # Check for partial matches (useful for typos)
    for alias, canonical in city_aliases.items():
        if normalized in alias or alias in normalized:
            return canonical
    
    # If no match found, return the normalized input
    return normalized

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city' or wants to compare prices. The function can handle various city name formats including alternative names (e.g., 'Saigon' for 'Ho Chi Minh City').",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to. Can be in various formats like 'London', 'Ho Chi Minh City', 'Saigon', etc.",
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
    
    # Normalize the city name to handle various input formats
    normalized_city = normalize_city_name(destination_city)
    
    if normalized_city in ticket_prices:
        price = ticket_prices[normalized_city]
        info = destination_info[normalized_city]
        
        # Get the proper display name for the city
        display_name = destination_city
        if normalized_city == "hochiminh":
            display_name = "Ho Chi Minh City"
        elif normalized_city in ["london", "paris", "tokyo", "berlin"]:
            display_name = normalized_city.title()
            
        return {
            "price": price, 
            "destination": display_name, 
            "normalized_key": normalized_city,
            "info": info,
            "found": True
        }
    else:
        # Try to suggest similar destinations
        suggestions = []
        for city in ticket_prices.keys():
            if city.startswith(normalized_city[:2]) or normalized_city[:2] in city:
                suggestions.append(city.title())
        
        return {
            "price": "Unknown", 
            "destination": destination_city, 
            "normalized_key": normalized_city,
            "info": f"Destination not found. Available destinations: {', '.join([city.title() for city in ticket_prices.keys()])}",
            "suggestions": suggestions,
            "found": False
        }

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
        description="Welcome to FlightAI! I can help you with flight prices and destination information. Try asking me about ticket prices, available destinations, or travel recommendations! I understand various city name formats (e.g., 'Saigon' for Ho Chi Minh City).",
        examples=[
            "How much is a ticket to Paris?",
            "What's the price to Saigon?",
            "Show me all available destinations",
            "I have a budget of $800, what can you recommend?",
            "Tell me about HCMC",
            "What's the cheapest destination?"
        ],
        theme="soft"
    )
    interface.launch(share=False)