Output phase3.mp4
Require claude

Set Theme "Catppuccin Frappe"
Set FontFamily "FiraCode Nerd Font"
Set Width 1200
Set Height 1200
Set Shell bash

Sleep 500ms
Type "iowarp mcp add adios -- uv run --with 'git+https://github.com/iowarp/scientific-mcps#subdirectory=Adios' adios-mcp"
Enter
Sleep 500ms
Type "iowarp mcp add pandas -- uv run --with 'git+https://github.com/iowarp/scientific-mcps#subdirectory=Pandas' pandas-mcp"
Enter
Sleep 500ms

Type "iowarp --dangerously-skip-permissions"
Sleep 500ms

Hide
Enter
Sleep 1s
Type "/clear"
Enter
Show
Sleep 1s

Type "Phase 3: Multi-Format Data Processing\"
Enter
Type "1. Load and analyze the `data/nanoparticles.bp5` ADIOS dataset with the Adios MCP\"
Enter
Type "2. Generate a report of this dataset\"
Enter
Type "3. Load the `data/sensor_data.csv` using the Pandas MCP\"
Enter
Type "4. Generate a summary of this dataset\"
Enter
Type "5. Create a `data_inventory_report.md` file with the report from both datasets`
Enter
Sleep 150s

Type "With the analysis completed, can you:\"
Enter
Type "Plot the trajectory of a single atom over time. The atom of choice should a parameter to the script. The output of the script should a PNG image with the results. Run the script for any single atom"
Enter
Sleep 360s

Type "/exit"
Enter