# FlightAI - Simple Airline AI Assistant

A simple AI-powered airline assistant built with OpenAI's GPT-4 and Gradio that helps customers get flight ticket prices and travel information.

## Features

- Interactive chat interface powered by Gradio
- Real-time ticket price lookup for major destinations
- OpenAI GPT-4 integration for natural language processing
- Function calling capabilities for dynamic price retrieval

## Supported Destinations

- London: $799
- Paris: $899
- Tokyo: $1400
- Berlin: $499
- Ho Chi Minh City: $1500

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

- "How much is a ticket to Paris?"
- "What's the price for a flight to Tokyo?"
- "I want to travel to London, what's the cost?"

## Project Structure

```
simple-airline-ai-assistant/
├── main.py              # Main application file
├── .env                 # Environment variables (not tracked by git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Configuration

The application uses the following configuration:

- **Model**: GPT-4o-mini (OpenAI)
- **Interface**: Gradio ChatInterface
- **Environment**: Conda environment named 'gradio'

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
   - You can also specify a different port in the Gradio launch configuration

### Getting Help

If you encounter any issues:

1. Check that all dependencies are properly installed
2. Verify your OpenAI API key is valid and has sufficient credits
3. Ensure you're using the correct conda environment

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
