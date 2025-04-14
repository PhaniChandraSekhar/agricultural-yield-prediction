# Agricultural Yield Prediction System

A Streamlit-based web application for predicting agricultural crop yields based on various environmental and farm management factors.

## Features

- Predict crop yields for various crops including wheat, rice, maize, and more
- Input environmental factors such as temperature, rainfall, and humidity
- Specify soil parameters including type, pH, and nutrient levels
- Configure farming practices like irrigation methods and fertilizer types
- View detailed analysis of factors influencing yield predictions
- Get recommendations for improving crop yields

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PhaniChandraSekhar/stock-prediction-app.git
   cd stock-prediction-app
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

You can run the application using the provided script:

```bash
python run_app.py
```

Alternatively, you can run it directly with Streamlit:

```bash
streamlit run src/app/main.py
```

The application will start and be available at http://localhost:8501 in your web browser.

## Project Structure

```
├── src/
│   ├── app/              # Streamlit application
│   │   ├── components/   # UI components
│   │   ├── pages/        # Application pages
│   │   ├── services/     # Service classes
│   │   ├── app.py        # Simple app version
│   │   └── main.py       # Main application
│   └── ml/               # Machine learning models
├── data/                 # Data storage (created at runtime)
├── requirements.txt      # Dependencies
└── run_app.py            # Application runner script
```

## Usage

1. Select your crop type and input field parameters
2. Enter environmental conditions for your region
3. Specify soil characteristics and farming practices
4. Click "Predict Yield" to get your prediction
5. Review the results and factor analysis
6. Apply the suggestions to improve yields

## License

This project is licensed under the MIT License - see the LICENSE file for details. 