#!/usr/bin/env python3
"""
DVD Retail Analytics Pipeline Runner

This script orchestrates the streamlined analytics pipeline for data analysis.
"""

import subprocess
import time
import os
import sys
from datetime import datetime

def run_script(script_path, script_name):
    """Run a Python script."""
    start_time = time.time()
    print(f"Starting {script_name}...")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print(f"{script_name} output: {result.stdout}")
        
        elapsed_time = time.time() - start_time
        print(f"Completed {script_name} in {elapsed_time:.2f} seconds")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def main():
    """Run the streamlined analytics pipeline."""
    print("Starting DVD Retail Analytics Pipeline")
    pipeline_start = time.time()
    
    # Check if requirements are installed
    print("Checking and installing required packages...")
    subprocess.run([
        sys.executable, 
        "-m", 
        "pip", 
        "install", 
        "-r", 
        "analytics/requirements.txt"
    ], check=False)
    
    # Define the pipeline steps
    pipeline_steps = [
        {
            "name": "Data Ingestion",
            "script_path": "analytics/scripts/data_ingestion.py"
        },
        {
            "name": "Sentiment Analysis",
            "script_path": "analytics/scripts/sentiment_analysis.py"
        },
        {
            "name": "Business Insights Generation",
            "script_path": "analytics/scripts/business_insights.py"
        }
    ]
    
    # Execute each step in sequence
    pipeline_success = True
    for step in pipeline_steps:
        step_success = run_script(step["script_path"], step["name"])
        if not step_success:
            print(f"Pipeline failed at step: {step['name']}")
            pipeline_success = False
            break
    
    if pipeline_success:
        pipeline_elapsed = time.time() - pipeline_start
        print(f"Pipeline completed successfully in {pipeline_elapsed:.2f} seconds")
    else:
        print("Pipeline failed.")

if __name__ == "__main__":
    main() 