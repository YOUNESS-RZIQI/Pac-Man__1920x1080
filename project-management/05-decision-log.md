# 05 Decision Log

| ID | Decision | Context | Reason | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **D-001** | Backend/Frontend separation | We needed to parallelize work. | Easier development, clearer ownership, easier debugging. | Team |
| **D-002** | Direct MLX usage | The subject allowed MLX or equivalents. | Avoiding compatibility uncertainty and gaining low-level graphical control. | Team |
| **D-003** | Dataclasses for structured state | Internal maze logic relies on bit logic. | Prevented raw, confusing numeric values from proliferating in the codebase, improving readability. | Amelhach |
| **D-004** | Shared grid representation | Frontend needed game states efficiently. | Reduced manual value-passing overhead; frontend queries state directly. | Amelhach / Yrziqi |
| **D-005** | Addition of power-ups and cheats | Team wanted a standout project. | Enhanced gameplay depth and provided debug utilities. | Team |
| **D-006** | Integrated Sound System | Silent gameplay felt incomplete. | Increased immersion and overall entertainment value. | Team |
| **D-007** | Use PyInstaller for packaging | Needed a distributable executable. | Ensures reviewers can play without complex local Python setups. | Amelhach |
