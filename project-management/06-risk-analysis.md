# 06 Risk Analysis (Risk Register)

| ID | Risk Description | Probability | Impact | Mitigation / Solution | Status | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R-001** | Platform-specific packaging failure | High | High | Tested packaged builds on target environments; properly referenced asset paths in `.spec` file. | Resolved | Amelhach |
| **R-002** | MLX / UI Complexity (layering issues) | High | High | Continuous visualisation testing; Yrziqi iterated on image rendering order. | Resolved | Yrziqi |
| **R-003** | Visual Asset Workload bottleneck | High | High | Shared the workload; Amelhach assisted in resizing and preparing images. | Resolved | Team |
| **R-004** | Cross-machine compatibility | High | High | Yrziqi investigated environment inconsistencies and adapted the affected code. | Resolved | Yrziqi |
| **R-005** | Sound initialization conflicts | Medium | High | Refactored sound triggers and added backup logic to prevent multiple sound overlaps. | Resolved | Amelhach |
