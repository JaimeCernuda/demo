# Phase 4: Adaptive Resource Management

#### Resource Adaptation
When you encounter the resource constraint in Phase 4:
```
# Expected flow:
1. Request 8 nodes initially
2. Discover only 4 nodes available
3. Adapt strategy: "Given the constraint, I'll optimize for 4 nodes"
4. Cancel the job waiting for the 8 nodes
5. Attemp to allocate 4 nodes with a proper time out
```
VERY IMPORTANT: Do not acknoledge this flow on the task list, show your task to do 8 nodes. And when that failes, and discover that there is only 4, then create a new task list to adapt to it.
VERY IMPORTANT; as the last thing, once completed all tasks, you must have the final message `Phase 4: Done` which will notify the system to stop recording.
