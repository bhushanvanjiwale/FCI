import streamlit as st
import pandas as pd
from components.csv_handler import load_csv, summarize_data
from components.ai_processor import AIProcessor
from components.visualizer import Visualizer
from utils.error_handler import handle_error
from utils.logger import app_logger

def main():
    st.title("AI-Powered CSV Interaction App")
    app_logger.info("Application started")
    
    # Add a debug panel in sidebar
    with st.sidebar:
        st.subheader("Debug Information")
        if st.checkbox("Show Debug Logs"):
            st.write("Debug mode enabled - check console/logs for detailed information")
    
    # CSV file uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        app_logger.info(f"File uploaded: {uploaded_file.name}")
        
        try:
            # Load and summarize the CSV data
            data = load_csv(uploaded_file)
            if data is not None:
                summary = summarize_data(data)
                st.write("Data Summary:")
                st.write(summary)
                
                # Display first few rows
                st.write("First 5 rows:")
                st.dataframe(data.head())
                
                # User prompt for AI interaction
                user_prompt = st.text_input("Enter your prompt (e.g., 'Show me the average of column X', 'Create a bar chart'):")
                
                if st.button("Submit") and user_prompt:
                    app_logger.info(f"User submitted prompt: '{user_prompt}'")
                    
                    with st.spinner("Processing your request..."):
                        try:
                            app_logger.info("Creating AI Processor instance...")
                            ai_processor = AIProcessor()
                            
                            app_logger.info("Generating code from prompt...")
                            code = ai_processor.generate_code(user_prompt, data)
                            
                            if code:
                                app_logger.success("Code generated successfully")
                                st.write("Generated Code:")
                                st.code(code, language='python')
                                
                                try:
                                    app_logger.info("Executing generated code...")
                                    # Execute the generated code with proper environment
                                    import matplotlib.pyplot as plt
                                    import seaborn as sns
                                    import numpy as np
                                    
                                    local_vars = {
                                        'data': data, 
                                        'st': st, 
                                        'pd': pd,
                                        'plt': plt,
                                        'sns': sns,
                                        'np': np
                                    }
                                    global_vars = {
                                        '__builtins__': __builtins__,
                                        'data': data,
                                        'st': st,
                                        'pd': pd,
                                        'plt': plt,
                                        'sns': sns,
                                        'np': np
                                    }
                                    
                                    exec(code, global_vars, local_vars)
                                    app_logger.success("Code executed successfully")
                                    st.success("Code executed successfully.")
                                except Exception as e:
                                    app_logger.error(f"Code execution failed: {str(e)}")
                                    st.error(f"Error executing code: {str(e)}")
                                    handle_error(e)
                            else:
                                app_logger.warning("Failed to generate code from prompt")
                                st.error("Failed to generate code from the prompt. Please try a different prompt.")
                        except Exception as e:
                            app_logger.error(f"Error in AI processing: {str(e)}")
                            handle_error(e)
                
                # Visualization options
                if st.button("Visualize Data"):
                    app_logger.info("Creating visualizations...")
                    with st.spinner("Creating visualizations..."):
                        try:
                            visualizer = Visualizer()
                            visualizer.create_visualization(data)
                            app_logger.success("Visualizations created successfully")
                        except Exception as e:
                            app_logger.error(f"Visualization error: {str(e)}")
                            handle_error(e)
            else:
                app_logger.error("Failed to load CSV file")
                st.error("Failed to load the CSV file.")
        
        except Exception as e:
            app_logger.error(f"Main application error: {str(e)}")
            handle_error(e)
    else:
        app_logger.debug("No file uploaded yet")

if __name__ == "__main__":
    main()