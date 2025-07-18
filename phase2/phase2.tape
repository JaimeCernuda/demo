Output arxviv.mp4
Require claude

Set Width 1200
Set Height 1200
Set Shell bash

Sleep 500ms
Type "iowarp mcp add arxiv -- uv run --with 'git+https://github.com/iowarp/scientific-mcps#subdirectory=Arxiv' arxiv-mcp"
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

Type "Phase 2: Literature Context Gathering\"
Enter
Type "Using the ArXiv mcp server. Can you:\"
Enter
Type "1. Search ArXiv for "Gray-Scott model" papers from 2024-2025\"
Enter
Type "2. Filter to top 5 most recent papers\"
Enter
Type "3. Extract abstracts and key methodologies\"
Enter
Type "4. Write them down on `literature_aummary.md`\"
Enter
Type "5. Download the found papers to a 'literature' folder"
Enter

Sleep 150s

Type "/exit"
Enter