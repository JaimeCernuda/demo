Set Theme "Catppuccin Frappe"
Set Width 1200
Set Height 1200
Set Shell bash

Type "claude --dangerously-skip-permissions"
Enter
Sleep 5s
Show

Type "Load and analyze the BP5 dataset from @bp5-dataset-collection/InCompact3d/Pipe-Flow/data.bp5 and perform comprehensive fluid dynamics visualization. "
Type "Context: This is a computational fluid dynamics dataset containing pressure and velocity field data from a pipe flow simulation. "
Type "Steps: "
Type "1. Load the BP5 dataset and examine available fields and data structure. "
Type "2. Create an isosurface visualization for pressure (pp) field at value 0.1 with appropriate color mapping. "
Type "3. Create three orthogonal slice planes for comprehensive flow analysis: "
Type "   - Y-normal slice (horizontal plane) at origin "
Type "   - Z-normal slice (vertical plane) at origin "
Type "   - X-normal slice (front view) at origin "
Type "4. Create an isosurface for velocity magnitude using ux field at value 0.5 with distinct coloring. "
Enter
Sleep 240s