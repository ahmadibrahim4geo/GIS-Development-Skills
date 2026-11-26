/**
 * Deterministic browser-compatible geospatial core for Web GIS vertical slices (W01-W12).
 * Pure ESM (zero external runtime deps): runs cleanly in modern browsers AND Node.js v20+.
 */

const WGS84_A = 6378137.0;
const WGS84_INV_F = 298.257223563;
const WGS84_F = 1.0 / WGS84_INV_F;
const WGS84_E2 = 2 * WGS84_F - WGS84_F * WGS84_F;
const WGS84_EP2 = WGS84_E2 / (1.0 - WGS84_E2);
const UTM_K0 = 0.9996;
const SUPPORTED_CRS = new Set(["EPSG:4326", "OGC:CRS84", "URN:OGC:DEF:CRS:OGC:1.3:CRS84"]);

export function validateCrsCode(crsName = "EPSG:4326") {
  const norm = String(crsName || "EPSG:4326").trim().toUpperCase();
  if (!SUPPORTED_CRS.has(norm)) {
    throw new Error(`Unsupported GeoJSON CRS '${crsName}'. Convert explicitly via PROJ/Proj4js before loading.`);
  }
  return norm;
}

export function loadGeoJsonFeatureCollection(rawInput) {
  const doc = typeof rawInput === "string" ? JSON.parse(rawInput) : structuredClone(rawInput);
  if (!doc || doc.type !== "FeatureCollection" || !Array.isArray(doc.features)) {
    throw new Error("Invalid GeoJSON: expected a FeatureCollection with a features array.");
  }
  const declaredCrs = doc.crs?.properties?.name;
  if (declaredCrs) {
    validateCrsCode(declaredCrs);
  }
  return {
    type: "FeatureCollection",
    name: doc.name || "untitled",
    attribution: doc.attribution || "Attribution required per dataset terms",
    features: doc.features.map((feat, idx) => ({
      type: "Feature",
      id: feat.id ?? `feature-${idx + 1}`,
      properties: feat.properties ? { ...feat.properties } : {},
      geometry: feat.geometry ? structuredClone(feat.geometry) : null,
    })),
  };
}

export function haversineMeters(lon1, lat1, lon2, lat2) {
  const rad = Math.PI / 180.0;
  const r = 6371008.8;
  const dLat = (lat2 - lat1) * rad;
  const dLon = (lon2 - lon1) * rad;
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dLon / 2) ** 2;
  return 2 * r * Math.asin(Math.min(1.0, Math.sqrt(a)));
}

export function wgs84ToUtm(lon, lat, zone = 36) {
  const rad = Math.PI / 180.0;
  const phi = lat * rad;
  const lam = lon * rad;
  const lam0 = ((zone - 1) * 6 - 180 + 3) * rad;
  const sinPhi = Math.sin(phi);
  const cosPhi = Math.cos(phi);
  const tanPhi = Math.tan(phi);

  const n = WGS84_A / Math.sqrt(1 - WGS84_E2 * sinPhi * sinPhi);
  const t = tanPhi * tanPhi;
  const c = WGS84_EP2 * cosPhi * cosPhi;
  const aTerm = cosPhi * (lam - lam0);

  const e4 = WGS84_E2 * WGS84_E2;
  const e6 = e4 * WGS84_E2;
  const m =
    WGS84_A *
    ((1 - WGS84_E2 / 4 - (3 * e4) / 64 - (5 * e6) / 256) * phi -
      ((3 * WGS84_E2) / 8 + (3 * e4) / 32 + (45 * e6) / 1024) * Math.sin(2 * phi) +
      ((15 * e4) / 256 + (45 * e6) / 1024) * Math.sin(4 * phi) -
      ((35 * e6) / 3072) * Math.sin(6 * phi));

  const easting =
    UTM_K0 *
      n *
      (aTerm +
        ((1 - t + c) * aTerm ** 3) / 6 +
        ((5 - 18 * t + t * t + 72 * c - 58 * WGS84_EP2) * aTerm ** 5) / 120) +
    500000.0;

  let northing =
    UTM_K0 *
    (m +
      n *
        tanPhi *
        (aTerm ** 2 / 2 +
          ((5 - t + 9 * c + 4 * c * c) * aTerm ** 4) / 24 +
          ((61 - 58 * t + t * t + 600 * c - 330 * WGS84_EP2) * aTerm ** 6) / 720));
  if (lat < 0) northing += 10000000.0;
  return { easting, northing, zone, epsg: lat >= 0 ? 32600 + zone : 32700 + zone };
}

export function utmToWgs84(easting, northing, zone = 36, northern = true) {
  const rad = Math.PI / 180.0;
  const x = easting - 500000.0;
  const y = northern ? northing : northing - 10000000.0;
  const e1 = (1 - Math.sqrt(1 - WGS84_E2)) / (1 + Math.sqrt(1 - WGS84_E2));
  const m = y / UTM_K0;
  const mu =
    m /
    (WGS84_A *
      (1 - WGS84_E2 / 4 - (3 * WGS84_E2 ** 2) / 64 - (5 * WGS84_E2 ** 3) / 256));

  const phi1 =
    mu +
    ((3 * e1) / 2 - (27 * e1 ** 3) / 32) * Math.sin(2 * mu) +
    ((21 * e1 ** 2) / 16 - (55 * e1 ** 4) / 32) * Math.sin(4 * mu) +
    ((151 * e1 ** 3) / 96) * Math.sin(6 * mu);

  const sin1 = Math.sin(phi1);
  const cos1 = Math.cos(phi1);
  const tan1 = Math.tan(phi1);
  const n1 = WGS84_A / Math.sqrt(1 - WGS84_E2 * sin1 * sin1);
  const t1 = tan1 * tan1;
  const c1 = WGS84_EP2 * cos1 * cos1;
  const r1 = (WGS84_A * (1 - WGS84_E2)) / Math.pow(1 - WGS84_E2 * sin1 * sin1, 1.5);
  const d = x / (n1 * UTM_K0);

  const lat =
    phi1 -
    ((n1 * tan1) / r1) *
      ((d * d) / 2 -
        ((5 + 3 * t1 + 10 * c1 - 4 * c1 * c1 - 9 * WGS84_EP2) * d ** 4) / 24 +
        ((61 + 90 * t1 + 298 * c1 + 45 * t1 * t1 - 252 * WGS84_EP2 - 3 * c1 * c1) * d ** 6) / 720);

  const lam0 = ((zone - 1) * 6 - 180 + 3) * rad;
  const lon =
    lam0 +
    (d -
      ((1 + 2 * t1 + c1) * d ** 3) / 6 +
      ((5 - 2 * c1 + 28 * t1 - 3 * c1 * c1 + 8 * WGS84_EP2 + 24 * t1 * t1) * d ** 5) / 120) /
      cos1;

  return { lon: lon / rad, lat: lat / rad };
}

function segmentsProperlyIntersect(a1, a2, b1, b2) {
  const cross = (p, q, r) => (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]);
  const d1 = cross(a1, a2, b1);
  const d2 = cross(a1, a2, b2);
  const d3 = cross(b1, b2, a1);
  const d4 = cross(b1, b2, a2);
  return ((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0));
}

export function hasSelfIntersection(ring) {
  if (!Array.isArray(ring) || ring.length < 4) return true;
  const edges = [];
  for (let i = 0; i < ring.length - 1; i++) {
    edges.push([ring[i], ring[i + 1]]);
  }
  for (let i = 0; i < edges.length; i++) {
    for (let j = i + 2; j < edges.length; j++) {
      if (i === 0 && j === edges.length - 1) continue;
      if (segmentsProperlyIntersect(edges[i][0], edges[i][1], edges[j][0], edges[j][1])) {
        return true;
      }
    }
  }
  return false;
}

export class SpatialEditorStore {
  constructor(initialCollection) {
    this._state = loadGeoJsonFeatureCollection(initialCollection);
    this._undo = [];
    this._redo = [];
  }

  snapshot() {
    return structuredClone(this._state);
  }

  _commit(mutator) {
    this._undo.push(structuredClone(this._state));
    this._redo = [];
    mutator(this._state);
    return this.snapshot();
  }

  createFeature(feature) {
    if (feature.geometry?.type === "Polygon" && hasSelfIntersection(feature.geometry.coordinates?.[0])) {
      throw new Error("Self-intersecting polygon rejected; requires explicit repair approval.");
    }
    return this._commit((state) => {
      state.features.push(structuredClone(feature));
    });
  }

  updateProperties(featureId, patch) {
    return this._commit((state) => {
      const target = state.features.find((f) => f.id === featureId);
      if (!target) throw new Error(`Feature '${featureId}' not found`);
      target.properties = { ...target.properties, ...structuredClone(patch) };
    });
  }

  deleteFeature(featureId) {
    return this._commit((state) => {
      const before = state.features.length;
      state.features = state.features.filter((f) => f.id !== featureId);
      if (state.features.length === before) throw new Error(`Feature '${featureId}' not found`);
    });
  }

  undo() {
    if (!this._undo.length) return this.snapshot();
    this._redo.push(structuredClone(this._state));
    this._state = this._undo.pop();
    return this.snapshot();
  }

  redo() {
    if (!this._redo.length) return this.snapshot();
    this._undo.push(structuredClone(this._state));
    this._state = this._redo.pop();
    return this.snapshot();
  }

  exportGeoJson() {
    return JSON.stringify(this._state, null, 2);
  }
}

export function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function sanitizePopupHtml(feature) {
  const title = escapeHtml(feature?.properties?.name_ar || feature?.properties?.name_en || feature?.id || "Feature");
  const rows = Object.entries(feature?.properties || {})
    .map(([k, v]) => `<tr><th>${escapeHtml(k)}</th><td>${v === null ? "<em>null</em>" : escapeHtml(v)}</td></tr>`)
    .join("");
  return `<div class="gis-popup"><h4>${title}</h4><table>${rows}</table></div>`;
}

export function formatCoordinatesBidi(lon, lat, lang = "en") {
  const coords = `${Number(lat).toFixed(5)}°, ${Number(lon).toFixed(5)}°`;
  return {
    dir: lang === "ar" ? "rtl" : "ltr",
    numericDir: "ltr",
    text: lang === "ar" ? `الإحداثيات (WGS84): \u200E${coords}` : `Coords (WGS84): ${coords}`,
  };
}

export function resolveSubpathAsset(baseUrl, relativeAsset) {
  const base = String(baseUrl || "/").endsWith("/") ? String(baseUrl || "/") : `${baseUrl}/`;
  const cleanRel = String(relativeAsset || "").replace(/^\/+/, "");
  if (cleanRel.includes("..")) {
    throw new Error(`Disallowed path traversal in asset reference: ${relativeAsset}`);
  }
  return `${base}${cleanRel}`;
}

export function validateImageryDateMetadata(record) {
  if (record?.claimed_as_acquisition && !record?.acquisition_date) {
    return {
      valid: false,
      reason: "Mosaic release date or OSM edit timestamp cannot be presented as satellite acquisition date.",
    };
  }
  return { valid: true, acquisition_date: record?.acquisition_date || null };
}

export function normalizeAntimeridianBbox(bbox) {
  const [west, south, east, north] = bbox.map(Number);
  const spansAntimeridian = west > east;
  const shortestDeltaLon = spansAntimeridian ? 360 - west + east : east - west;
  return { west, south, east, north, spansAntimeridian, shortestDeltaLon: Number(shortestDeltaLon.toFixed(6)) };
}
