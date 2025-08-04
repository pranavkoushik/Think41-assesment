# Customer Order Dashboard

A web application for managing and visualizing customer orders.

## Setup Instructions

1. **Prerequisites**
   - Python 3.8+
   - pip (Python package installer)

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Setup**
   - Create a `src/data` directory
   - Place `users.csv` and `orders.csv` in the `src/data` directory

4. **Initialize Database**
   ```bash
   cd src
   python database.py
   ```

## Project Structure

```
src/
  ├── data/                 # Directory for CSV files
  │   ├── users.csv         # User data
  │   └── orders.csv        # Order data
  ├── database.py          # Database setup and models
  └── requirements.txt     # Python dependencies
```

## Next Steps

- [ ] Add web framework (Flask/Django/FastAPI)
- [ ] Create API endpoints
- [ ] Build frontend components
- [ ] Add data visualization
- [ ] Implement authentication

## Running the Application

To be implemented after setting up the web framework.
