import pandas as pd
import os

def analyze_csv(file_path, sample_size=5):
    """Analyze a CSV file and return its structure and sample data."""
    print(f"\nAnalyzing {os.path.basename(file_path)}...")
    print("=" * 50)
    
    # Get basic file info
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # in MB
    print(f"File size: {file_size:.2f} MB")
    
    # Read the first few rows to get column info
    df = pd.read_csv(file_path, nrows=sample_size)
    
    # Display basic info
    print("\nColumns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col} ({df[col].dtype})")
    
    # Display sample data
    print("\nSample data:")
    print(df.head(sample_size).to_markdown(index=False))
    
    # Get row count (for larger files, we'll skip this as it can be slow)
    if file_size < 100:  # Only count rows for files smaller than 100MB
        row_count = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1  # subtract header
        print(f"\nTotal rows: {row_count:,}")
    else:
        print("\nSkipping row count for large file...")
    
    return df.columns.tolist(), df.dtypes.to_dict()

def main():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'archive')
    
    if not os.path.exists(data_dir):
        print(f"Error: Directory not found: {data_dir}")
        return
    
    # Analyze users.csv
    users_file = os.path.join(data_dir, 'users.csv')
    if os.path.exists(users_file):
        user_columns, user_dtypes = analyze_csv(users_file)
    else:
        print(f"File not found: {users_file}")
    
    # Analyze orders.csv
    orders_file = os.path.join(data_dir, 'orders.csv')
    if os.path.exists(orders_file):
        order_columns, order_dtypes = analyze_csv(orders_file)
    else:
        print(f"File not found: {orders_file}")
    
    # Analyze other CSV files if needed
    other_files = [f for f in os.listdir(data_dir) 
                  if f.endswith('.csv') and f not in ['users.csv', 'orders.csv']]
    
    if other_files:
        print("\nOther CSV files found:")
        for file in other_files:
            print(f"- {file}")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
