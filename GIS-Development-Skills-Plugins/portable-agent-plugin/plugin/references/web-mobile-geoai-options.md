# Web & Mobile GeoAI Options, Inference Boundaries & Agent Safeguards

> Covers all 13 GeoAI runtimes, on-device vs server/cloud execution boundaries, CRS pixel-to-world fidelity, and agent safety rules (`REQ-WM-027`, `REQ-WM-045`, `Web_Mobile_r3 §12`).

---

## 1. Thirteen GeoAI Runtimes & Spatial AI Frameworks (`§12`)

| Execution Tier | Tool / Runtime | Typical GIS Workload | Key Constraints & Fallbacks |
|---|---|---|---|
| **Browser On-Device** | `ONNX Runtime Web` (`WebGPU`/`WASM`), `TensorFlow.js`, `Transformers.js`, `MediaPipe`, `OpenCV.js`, `WebGPU`, `WebAssembly` | Client tile segmentation hints, road sign detection, client OCR/clustering | Detect `navigator.gpu` cleanly and fall back to WASM or server endpoint; disclose model weights size (`MB`) and license separately |
| **Mobile On-Device** | `ONNX Runtime Mobile`, `Google LiteRT` *(formerly TFLite)*, `CoreML` (iOS), `OpenCV Mobile` | Offline field photo classification, defect bounding boxes, vegetation health proxy | Thermal throttling on sustained camera inference; validate quantization precision delta vs full FP32 baseline |
| **Server / Workstation GPU** | `TorchGeo`, `Segment Anything (SAM / SAM2)`, `Grounding DINO`, `Raster Vision` / Python `OpenCV` | Large-area satellite/drone parcel segmentation, promptable building footprint extraction | Preserve raster `GeoTransform` + `EPSG` CRS + `NoData` masks when converting masks to polygons (`affine`) |
| **Local Private Agent LLM** | Local quantized model server (`llama.cpp`/`Ollama` local) when offline | Structured JSON intent parsing without external cloud PII egress | Schema-validate all outputs (`Zod`/JSON Schema); zero unconsented cloud polygon upload |

---

## 2. Non-Negotiable GeoAI Engineering & Agent Guardrails (`REQ-WM-045`)

1. **Affine GeoTransform & CRS Preservation:** Converting raster segmentation masks (`pixel x, y`) to GIS polygons **must** apply the source GeoTIFF/COG affine matrix and exact source `EPSG` CRS — never output normalized `[0..1]` pixel coords as `EPSG:4326`.
2. **Metric CRS & User Confirmation Before Spatial Writes:** When a GeoAI agent proposes spatial analysis or destructive/batch edits (e.g., *"buffer every school by 500 m and export parcels"*), it must:
   - Transform inputs from geographic degrees (`EPSG:4326`) into an appropriate **metric projected CRS** (e.g., matching UTM zone) or verified geodesic buffer before measuring `500 m`;
   - Display a dry-run preview (count, layer, CRS, units, output path) and obtain explicit user approval before modifying datasets (`prompt-intent-orchestrator`).
3. **Zero Silent Cloud Upload of Private Site Data (`OWASP #9`):** Never transmit sensitive survey coordinates, military/utility layers, or field photographs to a hosted Vision/GeoAI API unless explicitly configured, disclosed, and authorized by the user.
4. **No Hallucinated URLs, Weights, or Accuracy Claims:** Model code license (e.g., `Apache-2.0` runtime) != model weight license (`CC-BY-NC` / research-only check!). Report F1/IoU or detection confidence strictly from measured validation fixtures (`NOT RUN` when absent).
5. **Five Standard GeoAI Agent Workflows:** `(a)` On-device WebGPU/WASM single-tile detection + CPU fallback, `(b)` Field photo capture -> LiteRT tag -> human review before saving feature, `(c)` Cloud-native STAC/COG AOI inference job via Python worker -> Vector polygon readback, `(d)` Natural-language spatial filter validated by JSON schema & readonly SQL allowlist before PostGIS/DuckDB query, `(e)` Interactive SAM polygon assist inside editor `Undo` command stack.
