# Global Happiness Explorer

Welcome to the Global Happiness Explorer, an interactive dashboard designed to provide comprehensive insights into global happiness metrics. This application leverages data from the World Happiness Report to visualize and analyze happiness scores across different countries and regions.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Using Docker](#using-docker)
  - [Manual Setup](#manual-setup)
- [Usage](#usage)
- [Web Site](#WebSite)
- [Members](#Members)


## Introduction

The Global Happiness Explorer is a data visualization tool that helps users understand the factors contributing to happiness around the world. It provides interactive charts, maps, and filters to explore happiness scores, GDP per capita, life expectancy, and other related metrics.

## Features

- Interactive world map showing happiness scores by country
- Scatter plots to visualize the relationship between GDP per capita and happiness
- Bar charts and pie charts for regional and global trends
- Customizable filters for year, region, and country
- Detailed tooltips and hover information for data points
- Responsive design for desktop and mobile devices

## Installation

### Using Docker

1. **Clone the repository:**
   ```sh
   git clone https://github.com/salah0250/world_happiness
   cd world_happiness/happiness-dashboard
   ```
2. **Build and run the Docker container:**
   ```sh
   docker build -t happiness-dashboard .
   docker run -p 8050:8050 happiness-dashboard
   ```
3. **Access the application:**
Open your web browser and navigate to http://127.0.0.1:8050/

### Manual Setup

1. **Clone the repository:**
   ```sh
    git clone https://github.com/salah0250/world_happiness
    cd world_happiness/happiness-dashboard*
   ```
2. **Create and activate a virtual environment::**

   ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Create and activate a virtual environment::**

   ```sh
    pip install -r requirements.txt
   ```
4. **Run the application:**
   ```sh
    python run.py
   ```

5. **Access the application:**
Open your web browser and navigate to http://127.0.0.1:8050/


## Usage

Once the application is running, you can use the dashboard to explore various aspects of global happiness:

- Select a year to view data for that specific year.
- Use region and country dropdowns to filter your view.
- Adjust the happiness range slider to focus on specific - happiness levels.
- Hover over graphs for more detailed information.
- Click on map elements for country-specific details.

## Web Site

https://happiness-dashboard.onrender.com

 ## Members

 - Salah Eddine ABOULKACIM
 - Zaid LAASRI
 - Marouane TAKI EDINE
 - Abdellah ADANSAR
 - Brahim Saadaoui
