from openai import OpenAI
from utils.security import load_api_key
from utils.logger import app_logger

class AIProcessor:
    def __init__(self):
        app_logger.info("Initializing AI Processor...")
        try:
            self.api_key = load_api_key()
            self.client = OpenAI(api_key=self.api_key)
            app_logger.success("AI Processor initialized successfully with API key")
        except Exception as e:
            app_logger.error(f"Failed to initialize AI Processor: {str(e)}")
            raise

    def generate_code(self, prompt, dataframe):
        app_logger.info(f"Generating code for prompt: '{prompt[:50]}...'")
        app_logger.debug(f"DataFrame shape: {dataframe.shape}, columns: {list(dataframe.columns)}")
        
        try:
            # Get sample data for context
            sample_data = dataframe.head(3).to_dict()
            
            # Create a detailed prompt for code generation
            enhanced_prompt = f"""
            You have access to a pandas DataFrame named 'data' that is already loaded in memory.
            
            DataFrame information:
            - Columns: {list(dataframe.columns)}
            - Data types: {dataframe.dtypes.to_dict()}
            - Shape: {dataframe.shape}
            - Sample data (first 3 rows): {sample_data}
            
            User request: {prompt}
            
            Generate Python code that works with the existing DataFrame named 'data'.
            DO NOT try to read any CSV files - the data is already loaded.
            Use streamlit (st) for displaying results.
            Only import libraries if absolutely necessary.
            
            Example format:
            # Calculate something with the data
            result = data['column_name'].mean()
            st.write(f"Result: {{result}}")
            """
            
            app_logger.info("Sending request to OpenAI API...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful Python programming assistant. Generate clean, executable Python code that works with an existing pandas DataFrame named 'data'. Never try to read CSV files."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            app_logger.success("Received response from OpenAI API")
            
            code = response.choices[0].message.content.strip()
            # Remove markdown code block markers if present
            if code.startswith('```python'):
                code = code[9:]
            if code.endswith('```'):
                code = code[:-3]
            
            cleaned_code = code.strip()
            app_logger.info(f"Generated code length: {len(cleaned_code)} characters")
            app_logger.debug(f"Generated code: {cleaned_code}")
            
            return cleaned_code
            
        except Exception as e:
            app_logger.error(f"Error generating code: {str(e)}")
            return None

    def execute_code(self, code, dataframe):
        local_vars = {'data': dataframe, 'st': __import__('streamlit'), 'pd': __import__('pandas'), 'plt': __import__('matplotlib.pyplot'), 'sns': __import__('seaborn')}
        try:
            exec(code, {}, local_vars)
            return local_vars
        except Exception as e:
            return {"error": str(e)}