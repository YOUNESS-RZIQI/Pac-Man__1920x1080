# 09 Testing and Quality

The testing approach was highly iterative and manual, driven by continuous integration between the frontend and backend.

## Process
1. **Implementation**: A feature is developed (e.g., magnet power-up).
2. **Local Testing**: The implementing developer tests it locally.
3. **Integration**: Backend triggers and frontend visualizations are connected.
4. **Joint Testing**: Both teammates run the build. If unexpected behavior occurs (visual glitches, incorrect logic), they discuss the root cause.
5. **Fix & Retest**: The owner of the bug fixes it, and the game is re-tested.

## Scope of Testing
- **Functional Testing**: Movement, collisions, scores, level progression, power-ups.
- **Visual Testing**: UI rendering, instruction screens, highscores screen.
- **Integration Testing**: Ensuring `config.json` loads correctly, sounds trigger at the right time.

*(Evidence: Frequent commits in Git history fixing specific edge cases.)*
