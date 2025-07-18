Output phase4.mp4

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

Type "iowarp --dangerously-skip-permissions"
Sleep 500ms

Hide
Enter
Sleep 1s
Type "/clear"
Enter
Show
Sleep 1s 

Type "Phase 4: Adaptive Resource Management\"
Enter
Type "1. Explore optimal resource allocation\"
Enter
Type "2. Successfully secure resources via Slurm\"
Enter
Type "3. Generate a hostfile 'jarvis.hostfile' with the selected nodes\"
Enter
Type "4. Document resource management decisions in `resource_allocation.md`"
Enter
Sleep 150s

Type "/exit"
Enter