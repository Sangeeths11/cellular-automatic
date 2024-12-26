import pandas as pd
import matplotlib.pyplot as plt

def main():
    user_input = input("Enter the names of the CSV files separated by commas: ").split(',')
    file_list = [file.strip() for file in user_input]
    data = read_and_combine_csv(file_list)
    plotData(data)

def read_and_combine_csv(file_list):
    dataframes = []
    for file in file_list:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
        except FileNotFoundError:
            print(f"Error: File '{file}' not found.")
    return pd.concat(dataframes, ignore_index=True)

def plotData(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['pedestrianDensity'], data['flowRate'], color='blue')
    plt.title('Flow Rate')
    plt.xlabel('Pedestrian Density')
    plt.ylabel('Flow Rate')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()