Output phase1.mp4
Require claude

Set Theme "Catppuccin Frappe"
Set FontFamily "FiraCode Nerd Font"
Set Width 1200
Set Height 1200
Set Shell bash

Sleep 500ms
Type "iowarp mcp add slurm -- uv run --with 'git+https://github.com/iowarp/scientific-mcps#subdirectory=Slurm' slurm-mcp"
Enter
Sleep 500ms
Type "iowarp mcp add hardware -- uv run --with 'git+https://github.com/iowarp/scientific-mcps#subdirectory=Node_Hardware' node-hardware-mcp"
Enter
Sleep 500ms
Type "iowarp mcp add lmod -- uv run --with 'git+https://github.com/iowarp/scientific-mcps#subdirectory=lmod' lmod-mcp"
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

Type "Phase 1: Environment Discovery\"
Enter
Type "1. Explore the filesystem to discover available scientific data files\"
Enter
Type "2. Use the slurm MCP to check the current cluster status and available resources of the cluster\"
Enter
Type "3. Use the hardware MCP to query the node hardware specifications\"
Enter
Type "4. Use the lmod MCP to list all available software modules\"
Enter
Type "5. Create initial environment assessment in `environment_discovery.md``
Enter
Sleep 150s

Type "/exit"
Enter
