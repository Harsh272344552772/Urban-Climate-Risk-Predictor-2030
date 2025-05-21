
import os
from datetime import datetime
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Check if model exists, if not use a simple rule-based approach
MODEL_PATH = os.path.join('models', 'climate_model.pkl')

def rule_based_prediction(population, temperature_increase, urban_density, infrastructure):
    """Simple rule-based model for risk prediction."""
    # Base risk
    risk = 20
    
    # Population factor (more people = higher risk)
    if population > 1000000:
        risk += 20
    elif population > 500000:
        risk += 10
    
    # Temperature increase factor
    risk += temperature_increase * 10  # Each degree adds 10 points
    
    # Urban density factor
    if urban_density == 'high':
        risk += 15
    elif urban_density == 'medium':
        risk += 10
    
    # Infrastructure factor
    if infrastructure == 'aging':
        risk += 20
    elif infrastructure == 'moderate':
        risk += 10
    
    # Cap at 100
    return min(risk, 100)

# Functions for generating plots




def generate_rainfall_plot(temperature_increase):
    """Generate rainfall projection plot"""
    plt.figure(figsize=(10, 6))
    years = list(range(2023, 2031))
    base_rainfall = 800  # Base annual rainfall in mm
    
    # Generate rainfall data with some randomness and inverse relationship with temperature
    # As temperature increases, rainfall tends to decrease
    rainfall_data = []
    for i, year in enumerate(years):
        # Decrease rainfall as years progress based on temperature increase
        yearly_rainfall = base_rainfall - (i * 25 * temperature_increase / 2.0)
        # Add some randomness
        yearly_rainfall += (np.random.random() * 50 - 25)
        rainfall_data.append(yearly_rainfall)
    
    # Convert to numpy array for plotting
    rainfall_data = np.array(rainfall_data)
    
    # Create the bar plot
    plt.bar(years, rainfall_data, color='#0d6efd', alpha=0.7)
    
    # Add trend line
    z = np.polyfit(range(len(years)), rainfall_data, 1)
    p = np.poly1d(z)
    plt.plot(years, p(range(len(years))), "r--", color='#0d6efd', linewidth=2)
    
    plt.title('Annual Rainfall Projection (2023-2030)', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Rainfall (mm)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    
    return base64.b64encode(image_png).decode('utf-8')


def generate_risk_plot(risk_score, urban_density, infrastructure, temperature_increase=None):
    """Generate risk projection plot"""
    plt.figure(figsize=(10, 6))
    years = list(range(2023, 2031))
    
    # Base risk increases over time
    risk_values = []
    for i, _ in enumerate(years):
        # Risk increases more rapidly for high density and aging infrastructure
        density_factor = 1.5 if urban_density == 'high' else (1.2 if urban_density == 'medium' else 1.0)
        infra_factor = 1.5 if infrastructure == 'aging' else (1.2 if infrastructure == 'moderate' else 1.0)
        
        # Calculate yearly risk with some randomness
        yearly_risk = min(100, risk_score + (i * 3 * density_factor * infra_factor) + (np.random.random() * 5 - 2.5))
        risk_values.append(yearly_risk)
    
    # Create color gradient based on risk level
    colors = []
    for risk in risk_values:
        if risk >= 70:
            colors.append('#dc3545')  # High risk - red
        elif risk >= 40:
            colors.append('#ffc107')  # Medium risk - yellow
        else:
            colors.append('#198754')  # Low risk - green
    
    plt.bar(years, risk_values, color=colors, alpha=0.7)
    
    # Add threshold lines
    plt.axhline(y=70, color='#dc3545', linestyle='--', alpha=0.7, label='High Risk Threshold')
    plt.axhline(y=40, color='#ffc107', linestyle='--', alpha=0.7, label='Medium Risk Threshold')
    
    plt.title('Climate Risk Projection (2023-2030)', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Risk Score (%)', fontsize=12)
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.legend()
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    
    return base64.b64encode(image_png).decode('utf-8')

def generate_insights(temperature_increase, urban_density, infrastructure, risk_level):
    """Generate risk factors and recommendations based on inputs and risk level."""
    risk_factors = []
    recommendations = []
    
    # Temperature factors
    if temperature_increase > 2.5:
        risk_factors.append("Severe temperature increase")
        recommendations.append("Implement extensive heat mitigation strategies")
    elif temperature_increase > 1.5:
        risk_factors.append("Moderate temperature increase")
        recommendations.append("Develop cooling centers and heat action plans")
    else:
        risk_factors.append("Mild temperature increase")
    
    # Urban density factors
    if urban_density == 'high':
        risk_factors.append("High urban density")
        recommendations.append("Increase green spaces by 30%")
    elif urban_density == 'medium':
        risk_factors.append("Medium urban density")
        recommendations.append("Develop more community green areas")
    
    # Infrastructure factors
    if infrastructure == 'aging':
        risk_factors.append("Aging infrastructure")
        recommendations.append("Prioritize infrastructure updates")
    elif infrastructure == 'moderate':
        risk_factors.append("Moderately aged infrastructure")
        recommendations.append("Plan phased infrastructure improvements")
    
    # General recommendations based on risk level
    if risk_level == 'high':
        recommendations.extend([
            "Develop comprehensive climate action plan",
            "Implement flood defense systems",
            "Create emergency response protocols"
        ])
    elif risk_level == 'medium':
        recommendations.extend([
            "Assess vulnerable infrastructure",
            "Update urban planning guidelines"
        ])
    else:
        recommendations.append("Monitor climate indicators regularly")
    
    return risk_factors, recommendations

def generate_csv_data(city, population, temperature_increase, urban_density, infrastructure, risk_level, risk_score):
    """Generate CSV data for report download"""
    header = "City,Population,Temperature Increase,Urban Density,Infrastructure,Risk Level,Risk Score,Date\n"
    date = datetime.now().strftime('%Y-%m-%d')
    row = f"{city},{population},{temperature_increase},{urban_density},{infrastructure},{risk_level},{risk_score},{date}\n"
    
    # Generate future projections (5 years)
    future_years = list(range(1, 6))  # 1 to 5 years ahead
    current_year = datetime.now().year
    
    # Add projection header
    projection_header = "\n\nYear,Projected Temperature (°C),Projected Rainfall (mm),Projected Risk Score\n"
    
    projection_rows = ""
    for i in future_years:
        future_year = current_year + i
        # Simple projection models:
        # Temperature increases linearly
        future_temp = round(temperature_increase * (1 + i * 0.2), 2)
        # Rainfall decreases with temperature
        future_rainfall = round(800 - (i * 50 * temperature_increase / 2.0))
        # Risk increases
        future_risk = min(100, risk_score + (i * 5))
        
        projection_rows += f"{future_year},{future_temp},{future_rainfall},{future_risk}\n"
    
    return header + row + projection_header + projection_rows

def predict_climate_risk(city, population, temperature_increase, urban_density, infrastructure):
    """
    Predict climate risk based on input parameters.
    
    Args:
        city (str): Name of the city
        population (int): Population of the city
        temperature_increase (float): Projected temperature increase in degrees Celsius
        urban_density (str): Urban density level ('low', 'medium', 'high')
        infrastructure (str): Infrastructure quality ('modern', 'moderate', 'aging')
        
    Returns:
        dict: Dictionary containing risk assessment results
    """
    # Convert population to int if it's a string
    if isinstance(population, str):
        population = int(population.replace(',', ''))
    
    # Convert temperature_increase to float if it's a string
    if isinstance(temperature_increase, str):
        temperature_increase = float(temperature_increase)
    
    # Calculate risk score using rule-based approach
    risk_score = rule_based_prediction(population, temperature_increase, urban_density, infrastructure)
    
    # Determine risk level based on score
    if risk_score >= 70:
        risk_level = 'high'
    elif risk_score >= 40:
        risk_level = 'medium'
    else:
        risk_level = 'low'
    
    # Generate visualizations
    rainfall_plot = generate_rainfall_plot(temperature_increase)
    risk_plot = generate_risk_plot(risk_score, urban_density, infrastructure, temperature_increase)
    
    # Generate insights
    risk_factors, recommendations = generate_insights(temperature_increase, urban_density, infrastructure, risk_level)
    
    # Prepare CSV data for download
    csv_data = generate_csv_data(city, population, temperature_increase, urban_density, infrastructure, risk_level, risk_score)
    
    # Return results
    return {
        'city': city,
        'population': population,
        'temperature_increase': temperature_increase,
        'urban_density': urban_density,
        'infrastructure': infrastructure,
        'risk_level': risk_level,
        'risk_score': risk_score,
        'rainfall_plot': rainfall_plot,
        'risk_plot': risk_plot,
        'risk_factors': risk_factors,
        'recommendations': recommendations,
        'csv_data': csv_data
    }

