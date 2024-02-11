import matplotlib.pyplot as plt

# Provided data for disk benchmarks
disk_benchmarks = [
    {"file_system": "Minimum", "seq_write": {"minimum_requirement_mibs": 950, "result_percentage": 100}, "rnd_write": {"minimum_requirement_mibs": 420, "result_percentage": 100}},
    {"file_system": "ext4", "seq_write": {"score_mibs": 2410, "result_percentage": 259}, "rnd_write": {"score_mibs": 924, "result_percentage": 220}},
    {"file_system": "xfs", "seq_write": {"score_mibs": 2260, "result_percentage": 244}, "rnd_write": {"score_mibs": 806, "result_percentage": 192}},
    {"file_system": "f2fs", "seq_write": {"score_mibs": 1340, "result_percentage": 145}, "rnd_write": {"score_mibs": 543, "result_percentage": 129}},
    {"file_system": "btrfs", "seq_write": {"score_mibs": 1790, "result_percentage": 193}, "rnd_write": {"score_mibs": 417, "result_percentage": 99}},
    {"file_system": "zfs", "seq_write": {"score_mibs": 3510, "result_percentage": 378}, "rnd_write": {"score_mibs": 246, "result_percentage": 59}},
    {"file_system": "nilfs2", "seq_write": {"score_mibs": 736, "result_percentage": 78}, "rnd_write": {"score_mibs": 327, "result_percentage": 78}}
]

# Extracting data for plotting
file_systems = [fs["file_system"] for fs in disk_benchmarks]
seq_write_percentages = [fs["seq_write"]["result_percentage"] for fs in disk_benchmarks]
rnd_write_percentages = [fs["rnd_write"]["result_percentage"] for fs in disk_benchmarks]
seq_write_scores = [fs["seq_write"].get("score_mibs", fs["seq_write"].get("minimum_requirement_mibs")) for fs in disk_benchmarks]
rnd_write_scores = [fs["rnd_write"].get("score_mibs", fs["rnd_write"].get("minimum_requirement_mibs")) for fs in disk_benchmarks]

# Plotting write performance based on percentage
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
index = range(len(file_systems))

bar1 = ax.bar(index, seq_write_percentages, bar_width, label='Sequential Write', color='orange')
bar2 = ax.bar([p + bar_width for p in index], rnd_write_percentages, bar_width, label='Random Write', color='skyblue')

# Annotating bars with MiB/s values
for i, rect in enumerate(bar1):
    ax.text(rect.get_x() + rect.get_width() / 2., rect.get_height() - 5, f'{seq_write_scores[i]}', ha='center', va='top', color='black', fontsize=8)

for i, rect in enumerate(bar2):
    ax.text(rect.get_x() + rect.get_width() / 2., rect.get_height() - 5, f'{rnd_write_scores[i]}', ha='center', va='top', color='black', fontsize=8)

ax.set_xlabel('File System')
ax.set_ylabel('Performance (%)')
ax.set_title('Write Performance Comparison (Samsung NVMe 990 4TB / Polkadot Benchmark v1.6)')
ax.set_xticks([p + bar_width / 2 for p in index])
ax.set_xticklabels(file_systems, rotation=45)
ax.legend()

plt.tight_layout()
plt.savefig('write_performance.png')
