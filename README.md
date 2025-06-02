# Streamlit Car Reviews Dashboard

This project is a Streamlit application that provides a user-friendly dashboard for visualizing car reviews stored in an SQLite database. The application connects to a database specified in the `.env.vars` file and retrieves data to display various insights about car brands and models.

## Project Structure

```
streamlit-dashboard
├── src
│   ├── app.py            # Main entry point for the Streamlit application
│   └── db
│       └── database.py   # Database connection and query functions
├── .env.vars             # Environment variables including DB_PATH
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd streamlit-dashboard
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure the database path**:
   Ensure that the `.env.vars` file contains the correct path to your SQLite database:
   ```
   DB_PATH=/path/to/your/auto_reviews.db
   ```

## Usage

To run the Streamlit application, execute the following command:
```
streamlit run src/app.py
```

## Features

- **Data Visualization**: The dashboard displays various insights and statistics about car reviews.
- **Interactive Interface**: Users can interact with the dashboard to filter and explore different car brands and models.
- **Database Integration**: The application retrieves data from an SQLite database, ensuring that the information is up-to-date.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you'd like to add.