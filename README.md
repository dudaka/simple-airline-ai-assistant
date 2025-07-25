# FlightAI - Enhanced Airline AI Assistant

A sophisticated AI-powered airline assistant built with OpenAI's GPT-4 and Gradio that helps customers get flight ticket prices, destination information, and travel recommendations using advanced multishot prompting techniques.

## Features

- **Interactive Chat Interface** powered by Gradio with example prompts
- **Real-time Ticket Price Lookup** for major destinations
- **Comprehensive Destination Information** with cultural context
- **Budget-based Recommendations** for cost-conscious travelers
- **OpenAI GPT-4 Integration** with advanced function calling
- **Multishot Prompting** for enhanced conversational AI
- **Error Handling & Fallbacks** for robust user experience

## Supported Destinations & Prices

| Destination          | Price | Description                                                                |
| -------------------- | ----- | -------------------------------------------------------------------------- |
| **London**           | $799  | A vibrant European capital with rich history and culture                   |
| **Paris**            | $899  | The City of Light, famous for art, fashion, and cuisine                    |
| **Tokyo**            | $1400 | A modern metropolis blending traditional and contemporary Japanese culture |
| **Berlin**           | $499  | Germany's capital with fascinating history and vibrant arts scene          |
| **Ho Chi Minh City** | $1500 | Vietnam's bustling economic hub with rich cultural heritage                |

## AI Capabilities

### Advanced Function Calls

- `get_ticket_price()` - Get specific destination pricing with cultural context
- `get_all_destinations()` - Compare all available destinations and prices

### Flexible City Name Recognition

The AI assistant can understand various city name formats and alternative names:

| Official Name | Alternative Names Supported |
|---------------|----------------------------|
| **London** | London City, Greater London |
| **Paris** | Paris City, City of Light |
| **Tokyo** | Tokyo City, Tokyo Metropolitan |
| **Berlin** | Berlin City |
| **Ho Chi Minh City** | Ho Chi Minh, HCMC, Saigon, Sai Gon, Ho Chi Minh Ville |

### Multishot Prompting Examples

The AI assistant has been trained with specific examples to handle:

- Direct price inquiries with flexible city names
- Budget-based travel recommendations  
- Destination comparisons and suggestions
- Cultural information requests
- Graceful handling of unknown information

## Prerequisites

- Python 3.13.5 (or compatible version)
- Conda package manager
- OpenAI API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/dudaka/simple-airline-ai-assistant.git
cd simple-airline-ai-assistant
```

### 2. Create and activate conda environment

```bash
# Create a new conda environment named 'gradio' with Python 3.13.5
conda create -n gradio python=3.13.5

# Activate the environment
conda activate gradio
```

### 3. Install required packages

```bash
# Install the required Python packages
pip install openai gradio python-dotenv
```

### 4. Set up environment variables

Create a `.env` file in the project root directory:

```bash
# Create .env file
touch .env
```

Add your OpenAI API key to the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

**Important:** Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Usage

### Running the Application

1. Make sure your conda environment is activated:

```bash
conda activate gradio
```

2. Run the application:

```bash
python main.py
```

3. Open your web browser and navigate to the URL shown in the terminal (typically `http://127.0.0.1:7860`)

4. Start chatting with the FlightAI assistant!

### Example Conversations

**Price Inquiry:**

- User: "How much is a ticket to Paris?"
- Assistant: "I'll check the ticket price to Paris for you. A return ticket to Paris costs $899. Paris is the City of Light, famous for art, fashion, and cuisine!"

**Alternative City Names:**

- User: "What's the price to Saigon?"
- Assistant: "I'll check the ticket price to Saigon for you. A return ticket to Ho Chi Minh City (Saigon) costs $1500. Ho Chi Minh City is Vietnam's bustling economic hub with rich cultural heritage!"

**Budget Shopping:**

- User: "I have a budget of $800, what can you recommend?"
- Assistant: "Based on your $800 budget, I can recommend London at $799 or Berlin at $499. Berlin is particularly great value - it's Germany's capital with fascinating history and a vibrant arts scene!"

**Destination Discovery:**

- User: "Show me all available destinations"
- Assistant: "Here are all our available destinations: London ($799), Paris ($899), Tokyo ($1400), Berlin ($499), and Ho Chi Minh City ($1500). Would you like more details about any of these destinations?"

**Comparison Shopping:**

- User: "What's the cheapest destination?"
- Assistant: "The most affordable destination we offer is Berlin at $499 for a return ticket. It's Germany's capital with fascinating history and a vibrant arts scene!"

## Project Structure

```
simple-airline-ai-assistant/
├── main.py              # Main application with enhanced AI features
├── .env                 # Environment variables (not tracked by git)
├── .gitignore          # Git ignore rules (includes Gradio files)
└── README.md           # This documentation
```

## Technical Architecture

### Multishot Prompting Implementation

The system uses sophisticated prompt engineering with:

- **Example-driven learning**: Pre-defined conversation examples
- **Context-aware responses**: Cultural and destination information
- **Graceful degradation**: Proper handling of unknown queries
- **Professional tone**: Consistent airline customer service approach

### Function Calling System

```python
# Two main functions available to the AI:
get_ticket_price(destination_city)      # Individual price lookup with city name normalization
get_all_destinations()                  # Complete destination catalog

# City name normalization handles variations like:
normalize_city_name("Saigon") → "hochiminh"
normalize_city_name("HCMC") → "hochiminh" 
normalize_city_name("Ho Chi Minh City") → "hochiminh"
```

## Configuration

The application uses the following configuration:

- **AI Model**: GPT-4o-mini (OpenAI) with temperature 0.7
- **Interface**: Gradio ChatInterface with enhanced UI
- **Environment**: Conda environment named 'gradio' (Python 3.13.5)
- **Prompting**: Advanced multishot prompting with examples
- **Functions**: Two AI-callable functions for dynamic data retrieval
- **Theme**: Soft theme with example prompts for user guidance

## Environment Management

### Deactivating the environment

```bash
conda deactivate
```

### Removing the environment (if needed)

```bash
conda env remove -n gradio
```

### Listing conda environments

```bash
conda env list
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key not found**

   - Ensure your `.env` file exists and contains `OPENAI_API_KEY=your_key_here`
   - Check that the `.env` file is in the same directory as `main.py`

2. **Import errors**

   - Make sure the conda environment is activated: `conda activate gradio`
   - Verify all packages are installed: `pip list`

3. **Port already in use**

   - The application will automatically find an available port
   - Interface launches at `http://127.0.0.1:7860` by default

4. **Function calling errors**

   - Check OpenAI API credits and permissions
   - Verify the model supports function calling (GPT-4o-mini does)

5. **Gradio interface not loading**
   - Try refreshing the browser
   - Check console for JavaScript errors
   - Ensure Gradio is properly installed: `pip install gradio`

### Advanced Features

**Multishot Prompting Benefits:**

- More contextually aware responses
- Better handling of edge cases
- Consistent professional tone
- Enhanced user experience

**Function Calling Improvements:**

- Structured data responses
- Multiple query types supported
- Error handling and fallbacks
- Rich destination information

### Getting Help

If you encounter any issues:

1. Check that all dependencies are properly installed
2. Verify your OpenAI API key is valid and has sufficient credits
3. Ensure you're using the correct conda environment
4. Review the console output for detailed error messages

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- OpenAI for providing the GPT-4 API
- Gradio team for the excellent UI framework
- Python community for the amazing ecosystem
