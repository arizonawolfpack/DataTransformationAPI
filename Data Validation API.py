# Import required libraries
from fastapi import FastAPI, HTTPException, UploadFile, Form
from pydantic import BaseModel, ValidationError, Field
from typing import Optional, List
import pandas as pd
import json
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO
import re

# Initialize the FastAPI app
app = FastAPI(
    title="Unified Data Transformation and Validation API",
    description="An API to transform, validate, and clean data efficiently, saving developers valuable time.",
    version="1.0.0"
)

# Add CORS middleware to enable usage across different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
)

# Define a model for data schema validation using Pydantic
class DataValidationSchema(BaseModel):
    name: str = Field(..., example="John Doe", description="User's full name")
    email: str = Field(..., example="john.doe@example.com", description="User's email address")
    age: Optional[int] = Field(None, example=30, description="User's age")

    # A custom validator for email field
    @staticmethod
    def validate_email(email: str):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")

# Utility function for detecting and validating data schema
def detect_and_validate_schema(data: dict, schema: BaseModel):
    try:
        # Validate data against the schema
        validated_data = schema(**data)
        return validated_data.dict()
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

# Utility function for transforming dates
def transform_date_format(date_str: str, from_format: str, to_format: str):
    try:
        parsed_date = datetime.strptime(date_str, from_format)
        return parsed_date.strftime(to_format)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}")

# Utility function for cleaning missing or corrupted data
def clean_data(data: pd.DataFrame):
    # Fill missing values with defaults
    cleaned_data = data.fillna({
        "name": "Unknown",
        "email": "unknown@example.com",
        "age": 0
    })
    return cleaned_data

# Endpoint: Home
@app.get("/")
def read_root():
    return {"message": "Welcome to the Unified Data Transformation and Validation API"}

# Endpoint: Validate JSON Data
@app.post("/validate")
def validate_data(payload: dict):
    """
    Validate incoming JSON data against a predefined schema.
    """
    validated = detect_and_validate_schema(payload, DataValidationSchema)
    return {"message": "Validation successful", "validated_data": validated}

# Endpoint: Transform Dates
@app.post("/transform-date")
def transform_date(
    date_str: str = Form(..., example="12-15-2024"),
    from_format: str = Form(..., example="%m-%d-%Y"),
    to_format: str = Form(..., example="%Y-%m-%d")
):
    """
    Transform a date string from one format to another.
    """
    transformed_date = transform_date_format(date_str, from_format, to_format)
    return {"message": "Date transformed successfully", "transformed_date": transformed_date}

# Endpoint: Upload and Clean Data
@app.post("/upload-clean")
def upload_and_clean(file: UploadFile):
    """
    Upload a CSV file, clean the data, and return the cleaned result.
    """
    try:
        # Read the CSV file
        content = file.file.read().decode("utf-8")
        data = pd.read_csv(StringIO(content))

        # Clean the data
        cleaned_data = clean_data(data)
        return JSONResponse(
            content={
                "message": "Data cleaned successfully",
                "cleaned_data": cleaned_data.to_dict(orient="records")
            },
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with: uvicorn main:app --reload
"""
API Usage Examples:
1. /validate: POST with JSON data to validate against the schema.
2. /transform-date: POST with a date string and desired formats for transformation.
3. /upload-clean: POST with a CSV file to clean and normalize data.
"""