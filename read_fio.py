import json
import os
import matplotlib.pyplot as plt

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {file_path}: {e}")
                # Read the beginning of the file for debugging purposes
                file.seek(0)
                print(file.read(100))  # Print first 100 characters to check for issues
                raise
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        raise

# Path to the data directory
data_dir = 'data'
json_files = [f for f in os.listdir(data_dir) if f.startswith('fio_') and f.endswith('.json')]

# Initialize data storage
filesystems = []
iops_values = []
mean_slatencies = []
mean_clatencies = []
latencies_99_99 = []

# Read each JSON file and extract data
for json_file in json_files:
    file_path = os.path.join(data_dir, json_file)
    data = read_json(file_path)
    fs_name = json_file.split('_')[1].split('.')[0]  # Extract filesystem name from filename
    filesystems.append(fs_name.upper())
    
    # Assuming 'read' or 'write' keys are always present and we're interested in 'read' for this scenario
    iops = data['jobs'][0]['read']['iops']
    mean_clatency = data['jobs'][0]['read']['clat_ns']['mean'] / 1000.0  # Convert to microseconds
    mean_slatency = data['jobs'][0]['read']['slat_ns']['mean'] / 1000.0  # Convert to microseconds
    latency_99_99 = data['jobs'][0]['read']['clat_ns']['percentile']['99.990000'] / 1000.0  # Convert to microseconds
    
    iops_values.append(iops)
    mean_clatencies.append(mean_clatency)
    mean_slatencies.append(mean_slatency)
    latencies_99_99.append(latency_99_99)

# Function to create the bar plot for IOPS and latency
def plot_iops_and_latency(filesystems, iops, mean_clat, mean_slat, lat_99_99):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Create bar plot for IOPS
    bars = ax1.bar(filesystems, iops, color='skyblue', width=0.4, label='IOPS')
    ax1.set_xlabel('File System')
    ax1.set_ylabel('IOPS', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Annotate IOPS bars with their numerical values
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval, int(yval), verticalalignment='bottom', ha='center', color='black')

    # Create a second y-axis for the latency
    ax2 = ax1.twinx()
    ax2.set_yscale('log')  # Set the y-axis to a logarithmic scale
    mean_line, = ax2.plot(filesystems, mean_clat, color='g', marker='o', label='Mean Completion Latency (us)')
    mean_line, = ax2.plot(filesystems, mean_slat, color='orange', marker='o', label='Mean Submission Latency (us)')
    lat_99_99_line, = ax2.plot(filesystems, lat_99_99, color='pink', marker='x', label='99.99% Latency (us)')
    ax2.set_ylabel('Latency log(us)', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Annotate latency lines with their numerical values
    for i, txt in enumerate(mean_clat):
        ax2.annotate(f'{txt:.2f}', (filesystems[i], mean_clat[i]), textcoords="offset points", xytext=(0,10), ha='center')
    for i, txt in enumerate(mean_slat):
        ax2.annotate(f'{txt:.2f}', (filesystems[i], mean_slat[i]), textcoords="offset points", xytext=(0,10), ha='center')
    for i, txt in enumerate(lat_99_99):
        ax2.annotate(f'{txt:.2f}', (filesystems[i], lat_99_99[i]), textcoords="offset points", xytext=(0,-15), ha='center')

    # Adding legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    # Set title
    plt.title('Read IOPS and Latency(Samsung 990 4TB / fio 4k random read)')

    # Save the plot as an image file
    plt.savefig('./read_performance.png')

# Call the plotting function with the data
plot_iops_and_latency(filesystems, iops_values, mean_clatencies, mean_slatencies, latencies_99_99)
