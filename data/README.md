# Data Directory

Place CIC-IDS2017 CSV files in `data/raw/`.

Expected examples include files such as:

- `Monday-WorkingHours.pcap_ISCX.csv`
- `Tuesday-WorkingHours.pcap_ISCX.csv`
- `Wednesday-workingHours.pcap_ISCX.csv`
- `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`
- `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv`
- `Friday-WorkingHours-Morning.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`
- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`

The pipeline does not require all files to be present for development tests:
it loads every `.csv` file found in `data/raw/`. For a complete CIC-IDS2017
experiment, use the full CSV set above.

The repository intentionally does not include CIC-IDS2017 because it is large.
Use `data/sample/sample_cicids_like.csv` only for smoke tests and demonstrations.
