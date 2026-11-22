# Leonida tracker evidence

Checked: 2026-11-22 03:01 UTC

No game, runtime or GPU tests run by this tracker. Not a game-completion estimate.

## Code measurement

[Upstream main revision 67204bf8c047](https://github.com/ItsNotRexed/Leonida/commit/67204bf8c0471335d9046890288b33e8d5e2875b).
Scanned 30 production C++ files. Rules: `6831fdc6034af242`.
[Pinned Microsoft SDK reference](https://raw.githubusercontent.com/microsoft/DirectX-Headers/61c7718954ec73dbdd43c723240fe1a0452a3724/include/directx/d3d12.h); SHA-256 `773657b07955f7cdd526fb77049c1d8c5d23679e8cbe9ede90443cd2c93d3fab`.
The denominator follows CMake's generated-stub interfaces and their SDK inheritance chains, excluding IUnknown.
Bodies, partial paths, simple no-ops, and stubs are classified statically; none is a correctness claim.

## Optional coordination sources

- [Issue #313](https://github.com/ItsNotRexed/Leonida/issues/313); source updated 2026-11-22T02:58:02Z.
- [Issue #634](https://github.com/ItsNotRexed/Leonida/issues/634); source updated 2026-11-22T03:00:53Z.

Coordination timestamps include comments and do not prove that task tables were reconciled.
Code measurements do not depend on coordinator-reported method totals.

## D3D12 source scan

Static source classification. Body presence does not establish correct behavior or GPU verification.

| Group | Total | Body present | Partial / unsupported | No-op / constant | Stub / missing |
|---|---:|---:|---:|---:|---:|
| ID3D12GraphicsCommandList8 | 79 | 18 | 2 | 1 | 58 |
| ID3D12Device11 | 77 | 25 | 12 | 4 | 36 |
| ID3D12CommandQueue | 16 | 7 | 0 | 1 | 8 |
| ID3D12Resource | 12 | 8 | 0 | 2 | 2 |
| ID3D12Fence1 | 9 | 7 | 0 | 1 | 1 |
| ID3D12DescriptorHeap | 8 | 6 | 0 | 1 | 1 |
| ID3D12CommandAllocator | 6 | 3 | 0 | 2 | 1 |

## Open contribution tasks

Current coordination tables only. Tasks leaving these tables are not assumed complete.

| Group | Total | Active / claimed | Available | Blocked | Unclear |
|---|---:|---:|---:|---:|---:|
| D3D12 / Vulkan | 63 | 51 | 2 | 10 | 0 |
| Shader translator | 43 | 40 | 2 | 1 | 0 |
| Tests / CI | 28 | 22 | 5 | 1 | 0 |
| Build / tools | 23 | 23 | 0 | 0 | 0 |
| Assets / formats | 17 | 12 | 2 | 3 | 0 |
| Runtime | 11 | 7 | 0 | 4 | 0 |
| Contributor process | 5 | 5 | 0 | 0 | 0 |
| Fuzzing | 4 | 3 | 0 | 1 | 0 |

## Named method evidence

| Interface | Method | Classification | Reason | Source |
|---|---|---|---|---|
| ID3D12CommandAllocator | GetDevice | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:109](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L109) |
| ID3D12CommandAllocator | GetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:51](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L51) |
| ID3D12CommandAllocator | Reset | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_com.cpp:61](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L61) |
| ID3D12CommandAllocator | SetName | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_com_object.h:77](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L77) |
| ID3D12CommandAllocator | SetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:67](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L67) |
| ID3D12CommandAllocator | SetPrivateDataInterface | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:52](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L52) |
| ID3D12CommandQueue | BeginEvent | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:457](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L457) |
| ID3D12CommandQueue | CopyTileMappings | Stub / missing | Explicit unsupported/logging-only body | [runtime/shims/d3d12_com.cpp:501](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L501) |
| ID3D12CommandQueue | EndEvent | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:457](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L457) |
| ID3D12CommandQueue | ExecuteCommandLists | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:473](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L473) |
| ID3D12CommandQueue | GetClockCalibration | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:457](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L457) |
| ID3D12CommandQueue | GetDesc | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:471](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L471) |
| ID3D12CommandQueue | GetDevice | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:109](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L109) |
| ID3D12CommandQueue | GetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:51](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L51) |
| ID3D12CommandQueue | GetTimestampFrequency | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:457](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L457) |
| ID3D12CommandQueue | SetMarker | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:457](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L457) |
| ID3D12CommandQueue | SetName | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_com_object.h:77](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L77) |
| ID3D12CommandQueue | SetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:67](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L67) |
| ID3D12CommandQueue | SetPrivateDataInterface | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:457](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L457) |
| ID3D12CommandQueue | Signal | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:507](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L507) |
| ID3D12CommandQueue | UpdateTileMappings | Stub / missing | Explicit unsupported/logging-only body | [runtime/shims/d3d12_com.cpp:494](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L494) |
| ID3D12CommandQueue | Wait | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:515](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L515) |
| ID3D12DescriptorHeap | GetCPUDescriptorHandleForHeapStart | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:494](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L494) |
| ID3D12DescriptorHeap | GetDesc | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:493](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L493) |
| ID3D12DescriptorHeap | GetDevice | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:109](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L109) |
| ID3D12DescriptorHeap | GetGPUDescriptorHandleForHeapStart | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:498](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L498) |
| ID3D12DescriptorHeap | GetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:51](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L51) |
| ID3D12DescriptorHeap | SetName | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_com_object.h:77](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L77) |
| ID3D12DescriptorHeap | SetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:67](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L67) |
| ID3D12DescriptorHeap | SetPrivateDataInterface | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:483](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L483) |
| ID3D12Device11 | AddToStateObject | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CheckDriverMatchingIdentifier | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CheckFeatureSupport | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1793](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1793) |
| ID3D12Device11 | CopyDescriptors | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1326](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1326) |
| ID3D12Device11 | CopyDescriptorsSimple | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1347](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1347) |
| ID3D12Device11 | CreateCommandAllocator | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1188](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1188) |
| ID3D12Device11 | CreateCommandList | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1192](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1192) |
| ID3D12Device11 | CreateCommandList1 | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1199](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1199) |
| ID3D12Device11 | CreateCommandQueue | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1179](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1179) |
| ID3D12Device11 | CreateCommandQueue1 | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1682](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1682) |
| ID3D12Device11 | CreateCommandSignature | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateCommittedResource | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1527](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1527) |
| ID3D12Device11 | CreateCommittedResource1 | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1636](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1636) |
| ID3D12Device11 | CreateCommittedResource2 | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1646](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1646) |
| ID3D12Device11 | CreateCommittedResource3 | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1659](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1659) |
| ID3D12Device11 | CreateComputePipelineState | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateConstantBufferView | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateDepthStencilView | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1296](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1296) |
| ID3D12Device11 | CreateDescriptorHeap | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1220](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1220) |
| ID3D12Device11 | CreateFence | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1216](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1216) |
| ID3D12Device11 | CreateGraphicsPipelineState | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateHeap | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateHeap1 | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateLifetimeTracker | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateMetaCommand | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreatePipelineLibrary | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreatePipelineState | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreatePlacedResource | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreatePlacedResource1 | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreatePlacedResource2 | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateProtectedResourceSession | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateProtectedResourceSession1 | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateQueryHeap | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateRenderTargetView | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1234](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1234) |
| ID3D12Device11 | CreateReservedResource | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1580](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1580) |
| ID3D12Device11 | CreateReservedResource1 | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1586](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1586) |
| ID3D12Device11 | CreateReservedResource2 | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1599](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1599) |
| ID3D12Device11 | CreateRootSignature | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateSampler | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1460](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1460) |
| ID3D12Device11 | CreateSampler2 | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1473](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1473) |
| ID3D12Device11 | CreateSamplerFeedbackUnorderedAccessView | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateShaderCacheSession | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateShaderResourceView | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1358](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1358) |
| ID3D12Device11 | CreateSharedHandle | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateStateObject | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | CreateUnorderedAccessView | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_vulkan_device.cpp:1416](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1416) |
| ID3D12Device11 | EnqueueMakeResident | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1153](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1153) |
| ID3D12Device11 | EnumerateMetaCommandParameters | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | EnumerateMetaCommands | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | Evict | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1138](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1138) |
| ID3D12Device11 | GetAdapterLuid | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | GetCopyableFootprints | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1700](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1700) |
| ID3D12Device11 | GetCopyableFootprints1 | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1689](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1689) |
| ID3D12Device11 | GetCustomHeapProperties | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | GetDescriptorHandleIncrementSize | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1230](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1230) |
| ID3D12Device11 | GetDeviceRemovedReason | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_vulkan_device.cpp:1127](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1127) |
| ID3D12Device11 | GetNodeCount | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_vulkan_device.cpp:1126](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1126) |
| ID3D12Device11 | GetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:51](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L51) |
| ID3D12Device11 | GetRaytracingAccelerationStructurePrebuildInfo | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | GetResourceAllocationInfo | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1771](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1771) |
| ID3D12Device11 | GetResourceAllocationInfo1 | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1775](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1775) |
| ID3D12Device11 | GetResourceAllocationInfo2 | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1779](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1779) |
| ID3D12Device11 | GetResourceTiling | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1609](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1609) |
| ID3D12Device11 | MakeResident | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1134](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1134) |
| ID3D12Device11 | OpenExistingHeapFromAddress | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | OpenExistingHeapFromFileMapping | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | OpenSharedHandle | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | OpenSharedHandleByName | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | RemoveDevice | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | SetBackgroundProcessingMode | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1168](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1168) |
| ID3D12Device11 | SetEventOnMultipleFenceCompletion | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | SetName | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_com_object.h:77](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L77) |
| ID3D12Device11 | SetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:67](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L67) |
| ID3D12Device11 | SetPrivateDataInterface | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Device11 | SetResidencyPriority | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:1145](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1145) |
| ID3D12Device11 | SetStablePowerState | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_vulkan_device.cpp:1163](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1163) |
| ID3D12Device11 | ShaderCacheControl | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:1038](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L1038) |
| ID3D12Fence1 | GetCompletedValue | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:401](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L401) |
| ID3D12Fence1 | GetCreationFlags | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:402](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L402) |
| ID3D12Fence1 | GetDevice | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:109](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L109) |
| ID3D12Fence1 | GetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:51](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L51) |
| ID3D12Fence1 | SetEventOnCompletion | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:410](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L410) |
| ID3D12Fence1 | SetName | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_com_object.h:77](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L77) |
| ID3D12Fence1 | SetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:67](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L67) |
| ID3D12Fence1 | SetPrivateDataInterface | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:369](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L369) |
| ID3D12Fence1 | Signal | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:404](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L404) |
| ID3D12GraphicsCommandList8 | AtomicCopyBufferUINT | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | AtomicCopyBufferUINT64 | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | Barrier | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:144](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L144) |
| ID3D12GraphicsCommandList8 | BeginEvent | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | BeginQuery | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | BeginRenderPass | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | BuildRaytracingAccelerationStructure | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | ClearDepthStencilView | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:231](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L231) |
| ID3D12GraphicsCommandList8 | ClearRenderTargetView | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:223](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L223) |
| ID3D12GraphicsCommandList8 | ClearState | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | ClearUnorderedAccessViewFloat | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:250](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L250) |
| ID3D12GraphicsCommandList8 | ClearUnorderedAccessViewUint | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:243](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L243) |
| ID3D12GraphicsCommandList8 | Close | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:88](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L88) |
| ID3D12GraphicsCommandList8 | CopyBufferRegion | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:179](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L179) |
| ID3D12GraphicsCommandList8 | CopyRaytracingAccelerationStructure | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | CopyResource | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:194](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L194) |
| ID3D12GraphicsCommandList8 | CopyTextureRegion | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:185](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L185) |
| ID3D12GraphicsCommandList8 | CopyTiles | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | DiscardResource | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | Dispatch | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | DispatchMesh | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | DispatchRays | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | DrawIndexedInstanced | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | DrawInstanced | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | EmitRaytracingAccelerationStructurePostbuildInfo | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | EndEvent | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | EndQuery | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | EndRenderPass | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | ExecuteBundle | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:104](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L104) |
| ID3D12GraphicsCommandList8 | ExecuteIndirect | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | ExecuteMetaCommand | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | GetDevice | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:109](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L109) |
| ID3D12GraphicsCommandList8 | GetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:51](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L51) |
| ID3D12GraphicsCommandList8 | GetType | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:84](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L84) |
| ID3D12GraphicsCommandList8 | IASetIndexBuffer | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | IASetPrimitiveTopology | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | IASetVertexBuffers | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | InitializeMetaCommand | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | OMSetBlendFactor | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | OMSetDepthBounds | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | OMSetFrontAndBackStencilRef | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_com.cpp:264](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L264) |
| ID3D12GraphicsCommandList8 | OMSetRenderTargets | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | OMSetStencilRef | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | RSSetScissorRects | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | RSSetShadingRate | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | RSSetShadingRateImage | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | RSSetViewports | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | Reset | Partial / unsupported | Unsupported marker in body or a recognized local helper | [runtime/shims/d3d12_com.cpp:93](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L93) |
| ID3D12GraphicsCommandList8 | ResolveQueryData | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | ResolveSubresource | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:200](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L200) |
| ID3D12GraphicsCommandList8 | ResolveSubresourceRegion | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:206](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L206) |
| ID3D12GraphicsCommandList8 | ResourceBarrier | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:120](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L120) |
| ID3D12GraphicsCommandList8 | SOSetTargets | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetComputeRoot32BitConstant | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetComputeRoot32BitConstants | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetComputeRootConstantBufferView | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetComputeRootDescriptorTable | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetComputeRootShaderResourceView | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetComputeRootSignature | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetComputeRootUnorderedAccessView | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetDescriptorHeaps | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetGraphicsRoot32BitConstant | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetGraphicsRoot32BitConstants | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetGraphicsRootConstantBufferView | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetGraphicsRootDescriptorTable | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetGraphicsRootShaderResourceView | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetGraphicsRootSignature | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetGraphicsRootUnorderedAccessView | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetMarker | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetName | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_com_object.h:77](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L77) |
| ID3D12GraphicsCommandList8 | SetPipelineState | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetPipelineState1 | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetPredication | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com.cpp:218](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L218) |
| ID3D12GraphicsCommandList8 | SetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:67](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L67) |
| ID3D12GraphicsCommandList8 | SetPrivateDataInterface | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetProtectedResourceSession | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetSamplePositions | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | SetViewInstanceMask | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12GraphicsCommandList8 | WriteBufferImmediate | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_com.cpp:69](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com.cpp#L69) |
| ID3D12Resource | GetDesc | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:624](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L624) |
| ID3D12Resource | GetDevice | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:109](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L109) |
| ID3D12Resource | GetGPUVirtualAddress | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:508](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L508) |
| ID3D12Resource | GetHeapProperties | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:636](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L636) |
| ID3D12Resource | GetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:51](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L51) |
| ID3D12Resource | Map | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:646](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L646) |
| ID3D12Resource | ReadFromSubresource | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:666](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L666) |
| ID3D12Resource | SetName | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_com_object.h:77](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L77) |
| ID3D12Resource | SetPrivateData | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_com_object.h:67](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_com_object.h#L67) |
| ID3D12Resource | SetPrivateDataInterface | Stub / missing | Inherited generated fallback | [runtime/shims/d3d12_vulkan_device.cpp:508](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L508) |
| ID3D12Resource | Unmap | No-op / constant | Empty or constant-return body (may be intentional) | [runtime/shims/d3d12_vulkan_device.cpp:658](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L658) |
| ID3D12Resource | WriteToSubresource | Body present | Nontrivial definition; no recognized unsupported marker | [runtime/shims/d3d12_vulkan_device.cpp:662](https://github.com/ItsNotRexed/Leonida/blob/67204bf8c0471335d9046890288b33e8d5e2875b/runtime/shims/d3d12_vulkan_device.cpp#L662) |

## Listed task IDs

This is an inventory of the current tables, not a lifetime completion ledger.
Active includes claimed work and PRs; blocked is recognized only from explicit status text.
New task prefixes are discovered automatically. Repeated task IDs count once.

| Task | State | Evidence |
|---|---|---|
| ASSET-10 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-12 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-19 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-20 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-38 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-44 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-48 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-49 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-50 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-51 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-52 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-53 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-55 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-56 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-57 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-58 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| ASSET-59 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-36 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-39 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-64 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-67 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-77 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-78 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-94 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-100 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-101 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-104 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-124 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-125 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-126 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-127 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-128 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-129 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-130 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-131 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-132 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-133 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-134 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-135 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| BUILD-136 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| D3D-2 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-3 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-4 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-8 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-15 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-16 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-17 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-21 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-24 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-26 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-27 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-29 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-30 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-32 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-34 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-38 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-39 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-45 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-47 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-48 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-49 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-50 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-51 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-52 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-53 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-54 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-55 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-56 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-57 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-58 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-59 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-61 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-62 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-63 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-68 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-69 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-71 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-72 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-73 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-74 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-76 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-77 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-78 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-79 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-80 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-81 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-82 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-85 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-86 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-87 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-88 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-90 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-91 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-92 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-93 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-94 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-95 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-96 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-97 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-98 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-99 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-100 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| D3D-101 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/313) |
| FUZZ-10 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| FUZZ-11 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| FUZZ-12 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| FUZZ-13 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| PROC-15 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| PROC-23 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| PROC-24 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| PROC-25 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| PROC-26 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-4 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-5 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-10 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-13 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-19 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-20 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-21 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-22 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-23 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-24 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| RT-25 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-10 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-21 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-23 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-31 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-33 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-35 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-36 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-41 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-44 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-45 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-48 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-52 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-63 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-65 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-67 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-74 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-83 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-85 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-88 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-89 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-91 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-92 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-93 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-94 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-95 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-96 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-98 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-99 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-104 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-105 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-106 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-107 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-108 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-109 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-110 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-111 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-112 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-113 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-114 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-115 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-116 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-117 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| SHADER-118 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-29 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-39 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-50 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-53 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-54 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-55 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-56 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-57 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-58 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-59 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-61 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-71 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-81 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-88 | Blocked | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-92 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-96 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-97 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-98 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-99 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-100 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-101 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-102 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-103 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-104 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-105 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-106 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-107 | Active / claimed | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
| TEST-108 | Available | [Coordination table](https://github.com/ItsNotRexed/Leonida/issues/634) |
