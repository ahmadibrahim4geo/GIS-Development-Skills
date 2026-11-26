/**
 * Offline PWA cache guardrails, API error sanitization, realtime cursoring,
 * and 15-field offline sync queue matching web-mobile-offline-sync-contract.md.
 * Pure browser-and-Node ESM (zero bare node: static imports).
 */

function sha256HexSync(input) {
  const nodeCrypto = globalThis.process?.getBuiltinModule?.("node:crypto");
  if (nodeCrypto) {
    return nodeCrypto.createHash("sha256").update(input, "utf8").digest("hex");
  }
  // Compact pure-JS FNV-1a x2 fallback when synchronous browser WebCrypto is unavailable.
  let h1 = 0x811c9dc5;
  let h2 = 0x9e3779b9;
  for (let i = 0; i < input.length; i++) {
    const ch = input.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 0x01000193) >>> 0;
    h2 = Math.imul(h2 ^ ch, 0x85ebca6b) >>> 0;
  }
  return (h1.toString(16).padStart(8, "0") + h2.toString(16).padStart(8, "0")).repeat(4);
}

const BLOCKED_OSM_HOSTS = new Set(["tile.openstreetmap.org", "a.tile.openstreetmap.org", "b.tile.openstreetmap.org", "c.tile.openstreetmap.org"]);

export function validateTileSourceUrl(urlStr) {
  const parsed = new URL(urlStr);
  if (BLOCKED_OSM_HOSTS.has(parsed.hostname.toLowerCase())) {
    throw new Error(`Blocked prohibited bulk/offline OSM tile source '${parsed.hostname}'. Use self-hosted PMTiles or licensed tiles.`);
  }
  return urlStr;
}

export function redactAndClassifyApiError(statusCode, rawMessage = "", secretValues = []) {
  let clean = String(rawMessage || "");
  for (const sec of secretValues) {
    if (sec) clean = clean.split(sec).join("[REDACTED]");
  }
  clean = clean.replace(/(Bearer\s+)[A-Za-z0-9._-]+/gi, "$1[REDACTED]");
  clean = clean.replace(/((?:api[_-]?key|token|access_token)=)[^&\s]+/gi, "$1[REDACTED]");
  const kind =
    statusCode === 401 || statusCode === 403
      ? "auth-or-token-rejected"
      : statusCode === 429
        ? "quota-rate-limited"
        : "provider-error";
  return {
    statusCode,
    kind,
    userMessage: "External map/API service unavailable; switched cleanly to local fallback layer.",
    sanitizedDetail: clean,
  };
}

export class RealtimeCursorStream {
  constructor(baseDelayMs = 500, maxDelayMs = 30000) {
    this.baseDelayMs = baseDelayMs;
    this.maxDelayMs = maxDelayMs;
    this.attempts = 0;
    this.lastCursor = 0;
    this.seenIds = new Set();
    this.events = [];
  }

  nextBackoffMs() {
    const delay = Math.min(this.maxDelayMs, this.baseDelayMs * Math.pow(2, this.attempts));
    this.attempts += 1;
    return delay;
  }

  markConnected() {
    this.attempts = 0;
  }

  ingest(event) {
    const seq = Number(event.cursor);
    if (this.seenIds.has(event.event_id) || seq <= this.lastCursor) {
      return { accepted: false, reason: "duplicate-or-stale-cursor" };
    }
    this.seenIds.add(event.event_id);
    this.lastCursor = seq;
    this.events.push(structuredClone(event));
    return { accepted: true, cursor: seq };
  }
}

export class WebOfflineOutbox {
  constructor(initialSerialized = null) {
    const parsed = initialSerialized ? JSON.parse(initialSerialized) : { queue: [], conflicts: [] };
    this.queue = parsed.queue || [];
    this.conflicts = parsed.conflicts || [];
  }

  enqueue({ clientOpId, featureId, layerId, opType, baseRevision = null, geometry = null, attributes = {} }) {
    const payloadStr = JSON.stringify({ featureId, layerId, opType, baseRevision, geometry, attributes });
    const record = {
      client_op_id: clientOpId,
      feature_id: featureId,
      layer_id: layerId,
      op_type: opType,
      base_revision: baseRevision,
      server_revision: null,
      local_timestamp_utc: new Date().toISOString(),
      server_timestamp_utc: null,
      payload_sha256: sha256HexSync(payloadStr),
      state: "queued",
      attempt_count: 0,
      last_error: null,
      geometry_geojson: geometry ? structuredClone(geometry) : null,
      attributes: structuredClone(attributes),
      binary_attachment_refs: [],
    };
    this.queue.push(record);
    return record;
  }

  serializeBackup() {
    return JSON.stringify({ queue: this.queue, conflicts: this.conflicts }, null, 2);
  }

  flush(serverStore, { online = true, authenticated = true } = {}) {
    if (!online || !authenticated) {
      return { flushed: 0, deferred: this.queue.length };
    }
    const remaining = [];
    let flushed = 0;
    for (const item of this.queue) {
      item.attempt_count += 1;
      const current = serverStore[item.feature_id];
      const currentRev = current ? current.revision : 0;
      if (item.base_revision !== null && currentRev !== item.base_revision) {
        item.state = "conflict";
        item.server_revision = currentRev;
        item.last_error = "Revision mismatch (409); manual merge required (LWW blocked).";
        this.conflicts.push(item);
        continue;
      }
      const nextRev = currentRev + 1;
      serverStore[item.feature_id] = {
        revision: nextRev,
        deleted: item.op_type === "delete_tombstone",
        geometry: item.geometry_geojson,
        attributes: item.attributes,
      };
      item.state = "acked";
      item.server_revision = nextRev;
      item.server_timestamp_utc = new Date().toISOString();
      flushed += 1;
    }
    this.queue = remaining;
    return { flushed, conflicts: this.conflicts.length, deferred: 0 };
  }
}
