# Source history

Same scanner rules and pinned SDK reference for every point in this series.
Historical points use the last first-parent main commit in each available UTC day, rescanned with today's rules.
Live points use the latest main revision observed that UTC day. Missing days are not interpolated measurements.
Previous coordinator-table totals are not included. Body counts do not prove correctness or compatibility.

Rules: `6831fdc6034af242`. [Pinned reference](https://raw.githubusercontent.com/microsoft/DirectX-Headers/61c7718954ec73dbdd43c723240fe1a0452a3724/include/directx/d3d12.h).

| UTC day | Bodies | Partial | No-op | Stubs | Total | Source | Measurement |
|---|---:|---:|---:|---:|---:|---|---|
| 2026-11-21 | 60 | 8 | 11 | 128 | 207 | [4abd5457](https://github.com/ItsNotRexed/Leonida/commit/4abd54571b6efa02d97eda4711792fa00b455dc3) | rescanned |
| 2026-11-22 | 74 | 14 | 12 | 107 | 207 | [67204bf8](https://github.com/ItsNotRexed/Leonida/commit/67204bf8c0471335d9046890288b33e8d5e2875b) | observed |

## Unmeasured historical trees

These commits could not be measured with the current adapter. They are not treated as zero.

- 2026-11-20 (bd2dd1c8): Generated D3D12 interface list not found in runtime/CMakeLists.txt
