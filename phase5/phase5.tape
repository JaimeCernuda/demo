Output phase5.mp4

Require iowarp

Set Theme "Catppuccin Frappe"
Set Width 1200
Set Height 1200
Set Shell bash

Sleep 500ms
Type "iowarp mcp add adios -- uv run --with 'git+https://github.com/iowarp/scientific-mcps#subdirectory=Jarvis' jarvis-mcp"
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

Type "Phase 5: Computational Workflow Execution:\"
Enter
Type "1. Initialize Jarvis pipeline.\"
Enter
Type "2. Configure it for the available node allocation with the `jarvis.hostfile`.\"
Enter
Type "3. Build the jarvis enviornment.\"
Enter
Type "4. Append the Gray Scott application.\"
Enter
Type "5. Configure Gray Scott for a small run with 5 steps and a grid size of 8 with the outputs stored in the current folder.\"
Enter
Type "6. Run the job.\"
Enter
Type "7. Document the location of the results."
Enter
Sleep 150s

Type "/exit"
Enter