import pandas as pd
import matplotlib.pyplot as plt

def plot_price_history(filename='prices.csv'):
    try:
        # Read the CSV with Timestamp parsed as datetime
        df = pd.read_csv(filename, parse_dates=['Timestamp'])

        # Plot the price over time
        plt.figure(figsize=(10, 5))
        plt.plot(df['Timestamp'], df['Price'], marker='o', linestyle='-', color='blue')

        # Styling
        plt.title('Bitcoin Price Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Price (USD)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show plot
        plt.show()

    except FileNotFoundError:
        print(f"{filename} not found. Make sure you have logged some prices first.")
    except Exception as e:
        print("Error plotting:", e)

# Optional test run
if __name__ == "__main__":
    plot_price_history()
