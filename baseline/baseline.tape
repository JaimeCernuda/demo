Output baseline.mp4
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
Type "iowarp mcp add context7 -- npx -y @upstash/context7-mcp"
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

Type "Hello. Who are you?"
Enter
Sleep 10s
Type "/exit"
Enter
