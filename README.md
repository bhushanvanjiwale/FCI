# Streamlit CSV AI Application

This project is an AI-powered application that allows users to interact with CSV files using natural language prompts. It leverages the OpenAI API for code generation and includes features for data visualization, security, and user-friendly error handling.

## Features

- **CSV File Upload**: Users can upload CSV files to analyze and visualize data.
- **Natural Language Processing**: Users can input natural language prompts to generate Python code that manipulates the uploaded data.
- **Data Visualization**: The application provides various visualization options using libraries like Matplotlib, Seaborn, and Plotly.
- **Error Handling**: User-friendly error messages guide users in case of invalid inputs or API issues.
- **Security**: The application securely loads the OpenAI API key to prevent exposure in the codebase.

## Project Structure

```
streamlit-csv-ai-app
├── src
│   ├── app.py                # Main entry point for the Streamlit application
│   ├── components
│   │   ├── csv_handler.py    # Handles CSV file uploads and data summaries
│   │   ├── ai_processor.py    # Interacts with OpenAI API for code generation
│   │   └── visualizer.py      # Generates visualizations based on user prompts
│   ├── utils
│   │   ├── security.py        # Securely loads the OpenAI API key
│   │   └── error_handler.py    # Handles errors and provides user-friendly messages
│   └── config
│       ├── settings.py        # Loads configuration settings
├── requirements.txt           # Lists project dependencies
├── .env.example               # Example for environment variable configuration
├── .gitignore                 # Specifies files to ignore in version control
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit-csv-ai-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key in the `config/settings.py` file.

## Usage

1. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```

2. Upload a CSV file and enter your natural language prompt to interact with the data.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.