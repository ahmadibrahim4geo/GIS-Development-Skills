import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  SpatialEditorStore,
  formatCoordinatesBidi,
  hasSelfIntersection,
  haversineMeters,
  loadGeoJsonFeatureCollection,
  normalizeAntimeridianBbox,
  resolveSubpathAsset,
  sanitizePopupHtml,
  utmToWgs84,
  validateCrsCode,
  validateImageryDateMetadata,
  wgs84ToUtm,
} from "../../examples/web-gis/shared/spatial-core.mjs";
import {
  RealtimeCursorStream,
  WebOfflineOutbox,
  redactAndClassifyApiError,
  validateTileSourceUrl,
} from "../../examples/web-gis/shared/pwa-sync.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", "..");
const FIXTURE_RAW = fs.readFileSync(
  path.join(ROOT, "tests", "shared-gis-fixtures", "geojson_epsg4326_bilingual.geojson"),
  "utf8"
);
const EXPECTED = JSON.parse(
  fs.readFileSync(
    path.join(ROOT, "tests", "shared-gis-fixtures", "expected-shared-contracts.json"),
    "utf8"
  )
);

test("GIS-001, GIS-003, GIS-007 & GIS-010: loads bilingual EPSG:4326 GeoJSON cleanly", () => {
  const fc = loadGeoJsonFeatureCollection(FIXTURE_RAW);
  assert.equal(fc.features.length, EXPECTED.gis_001_expected.feature_count);
  assert.deepEqual(
    fc.features.map((f) => f.id),
    EXPECTED.gis_001_expected.feature_ids
  );
  assert.deepEqual(
    fc.features.map((f) => f.geometry.type),
    EXPECTED.gis_001_expected.geometry_types
  );
  assert.equal(fc.features[0].properties.name_ar, "نقطة معاينة القاهرة");
  assert.equal(fc.features[0].properties.notes, null);
  assert.match(fc.attribution, /GIS Development Skills/i);
});

test("GIS-002 & GIS-006: WGS84<->UTM36N transformation parity, geodesic distance & unsupported CRS gate", () => {
  const ref = EXPECTED.gis_002_cairo_utm36n_reference;
  const utm = wgs84ToUtm(ref.lon, ref.lat, 36);
  assert.equal(utm.epsg, ref.epsg_target);
  assert.ok(Math.abs(utm.easting - ref.approx_easting_m) < 15.0);
  assert.ok(Math.abs(utm.northing - ref.approx_northing_m) < 15.0);

  const back = utmToWgs84(utm.easting, utm.northing, 36, true);
  assert.ok(haversineMeters(ref.lon, ref.lat, back.lon, back.lat) < ref.roundtrip_tolerance_m);

  const fc = loadGeoJsonFeatureCollection(FIXTURE_RAW);
  const line = fc.features[1].geometry.coordinates;
  const dist = haversineMeters(line[0][0], line[0][1], line[1][0], line[1][1]);
  assert.ok(Math.abs(dist - ref.line_corridor_haversine_m_approx) < ref.line_distance_tolerance_m);

  assert.throws(
    () => validateCrsCode("EPSG:999999"),
    /Unsupported GeoJSON CRS/
  );
});

test("GIS-004, GIS-005 & GIS-008: editing, undo/redo, and bowtie self-intersection rejection", () => {
  const store = new SpatialEditorStore(FIXTURE_RAW);
  assert.equal(hasSelfIntersection(store.snapshot().features[2].geometry.coordinates[0]), false);
  assert.equal(hasSelfIntersection(EXPECTED.gis_008_invalid_bowtie_polygon), true);

  assert.throws(
    () =>
      store.createFeature({
        type: "Feature",
        id: "bad-bowtie",
        properties: { name_en: "Invalid" },
        geometry: { type: "Polygon", coordinates: [EXPECTED.gis_008_invalid_bowtie_polygon] },
      }),
    /Self-intersecting polygon rejected/
  );

  store.updateProperties("pt-cairo-01", { status: "surveyed-ar-الأصل" });
  assert.equal(store.snapshot().features[0].properties.status, "surveyed-ar-الأصل");

  store.deleteFeature("mp-sensors-04");
  assert.equal(store.snapshot().features.length, 3);
  store.undo();
  assert.equal(store.snapshot().features.length, 4);
  store.redo();
  assert.equal(store.snapshot().features.length, 3);
  store.undo();
  assert.equal(store.snapshot().features.length, 4);
});

test("GIS-013 & GIS-014: rejects fake acquisition dates and normalizes antimeridian bbox", () => {
  for (const row of EXPECTED.gis_013_fake_imagery_cases) {
    const res = validateImageryDateMetadata(row);
    assert.equal(res.valid, !row.must_reject);
  }
  const anti = normalizeAntimeridianBbox(EXPECTED.gis_014_antimeridian_segment.bbox_unwrapped);
  assert.equal(anti.spansAntimeridian, true);
  assert.equal(anti.shortestDeltaLon, EXPECTED.gis_014_antimeridian_segment.shortest_delta_lon_deg);
});

test("WEB-QA-04, WEB-QA-05, WEB-QA-10 & WEB-QA-11: XSS escaping, BiDi coords & subpath safety", () => {
  const xssHtml = sanitizePopupHtml({
    id: "evil-1",
    properties: {
      name_ar: "<script>alert(1)</script>موقع",
      onclick: '<img src=x onerror="steal()">',
    },
  });
  assert.doesNotMatch(xssHtml, /<script>/i);
  assert.doesNotMatch(xssHtml, /<img/i);
  assert.match(xssHtml, /&lt;script&gt;/);

  const bidi = formatCoordinatesBidi(31.2357, 30.0444, "ar");
  assert.equal(bidi.dir, "rtl");
  assert.equal(bidi.numericDir, "ltr");
  assert.ok(bidi.text.includes("30.04440°"));

  assert.equal(
    resolveSubpathAsset("/GIS-Development-Skills/explorer.html".replace("explorer.html", ""), "tests/shared.json"),
    "/GIS-Development-Skills/tests/shared.json"
  );
  assert.throws(() => resolveSubpathAsset("/GIS-Development-Skills/", "../secret.json"), /traversal/);
});

test("WEB-QA-06, WEB-QA-07, WEB-QA-08 & WEB-QA-14: offline queue, OSM scrape ban, key redaction & cursor stream", () => {
  assert.throws(() => validateTileSourceUrl("https://tile.openstreetmap.org/12/2400/1680.png"), /Blocked prohibited/);
  assert.equal(
    validateTileSourceUrl("https://cdn.example.invalid/basemaps/cairo.pmtiles"),
    "https://cdn.example.invalid/basemaps/cairo.pmtiles"
  );

  const errRes = redactAndClassifyApiError(429, "GET failed Bearer secret-tok-123 api_key=XYZ999", ["secret-tok-123"]);
  assert.equal(errRes.kind, "quota-rate-limited");
  assert.doesNotMatch(errRes.sanitizedDetail, /secret-tok-123|XYZ999/);

  const stream = new RealtimeCursorStream(100, 1000);
  assert.equal(stream.nextBackoffMs(), 100);
  assert.equal(stream.nextBackoffMs(), 200);
  assert.equal(stream.ingest({ event_id: "e1", cursor: 5 }).accepted, true);
  assert.equal(stream.ingest({ event_id: "e1", cursor: 5 }).accepted, false);
  assert.equal(stream.ingest({ event_id: "e2", cursor: 4 }).accepted, false);

  const outbox1 = new WebOfflineOutbox();
  outbox1.enqueue({
    clientOpId: "web-op-1",
    featureId: "pt-new-1",
    layerId: "stations",
    opType: "create",
    baseRevision: null,
    geometry: { type: "Point", coordinates: [31.2, 30.0] },
    attributes: { name_ar: "نقطة أوفلاين" },
  });
  const backup = outbox1.serializeBackup();
  const coldReopened = new WebOfflineOutbox(backup);
  const serverStore = {};
  assert.deepEqual(coldReopened.flush(serverStore, { online: false, authenticated: true }), { flushed: 0, deferred: 1 });
  assert.deepEqual(coldReopened.flush(serverStore, { online: true, authenticated: true }), { flushed: 1, conflicts: 0, deferred: 0 });
  assert.equal(serverStore["pt-new-1"].revision, 1);

  // Conflict prevents silent blind LWW overwrite.
  coldReopened.enqueue({
    clientOpId: "web-op-conflict",
    featureId: "pt-new-1",
    layerId: "stations",
    opType: "update",
    baseRevision: 0,
    geometry: { type: "Point", coordinates: [31.9, 30.9] },
    attributes: { name_ar: "تعديل متعارض" },
  });
  const conflictRes = coldReopened.flush(serverStore, { online: true, authenticated: true });
  assert.equal(conflictRes.conflicts, 1);
  assert.equal(serverStore["pt-new-1"].attributes.name_ar, "نقطة أوفلاين");
});
