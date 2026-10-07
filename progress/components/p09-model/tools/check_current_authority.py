"""Check the recovered P09 bindings against the supplied current authority.

This cannot compare against unavailable historical catalog/speech JSON.
It changes no model, canonical content, or tests.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cakood.p09_model import LABEL_IDS, SCRIPT_BINDINGS, RECORD_UNITS, FLAG_IDS


def require(value, detail):
    if not value:
        raise ValueError(detail)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    authority = ROOT / "authority"
    catalog = json.loads((authority / "full-line-catalog.json").read_text())
    speech = json.loads((authority / "speech-units.json").read_text())
    revision = json.loads((authority / "CURRENT-SCRIPT-REVISION.json").read_text())
    fixture = json.loads((ROOT / "tests/fixtures/p09/canonical-bindings.json").read_text())
    require(revision["editorial_revision"] == fixture["editorial_revision"] == 3, "Revision changed")
    for key, filename in (("catalog_sha256", "full-line-catalog.json"),
                          ("speech_sha256", "speech-units.json")):
        require(digest(authority / filename) == revision[key] == fixture[key], filename + " pin mismatch")
    require(digest(authority / "complete-body.md") == fixture["gdd_sha256"] ==
            "18e2eb1a300cc1ac1192916441b640ca6134af619ee17eb424637b4dde28647c", "GDD changed")
    rows = [r for r in catalog["records"] if r["id"].startswith("P09.")]
    units = [u for u in speech["units"] if u["record_id"].startswith("P09.")]
    ids = set(LABEL_IDS.values()) | {r for group in SCRIPT_BINDINGS.values() for r in group}
    require(len(rows) == len(ids) == 20 and len(units) == 20, "P09 record/unit count mismatch")
    require(ids == {r["id"] for r in rows} == set(fixture["records"]), "P09 coverage mismatch")
    require(list(fixture["records"]) == [r["id"] for r in rows], "Record order mismatch")
    speakers = {
        "P09.OPEN.001": ["stringer", "jack"],
        "P09.LOOK.001": ["jack"],
        "P09.DIALOGUE.001": ["stringer", "jack", "stringer"],
        "P09.FAILURE.001": ["stringer", "rita"],
        "P09.DIALOGUE.002": ["stringer", "jack", "stringer", "jack", "stringer"],
        "P09.DIALOGUE.003": ["rita", "stringer", "rita", "stringer"],
        "P09.SUCCESS.001": ["jack"],
        "P09.LOOK.002": ["jack"],
        "P09.FAILURE.002": ["jack"],
    }
    require(set(speakers) == set(RECORD_UNITS), "Spoken record set mismatch")
    for row in rows:
        record = row["id"]
        record_units = [u for u in units if u["record_id"] == record]
        expected = {"text_sha256": row["text_sha256"], "speaker_id": row["speaker_id"],
                    "trigger": row["trigger"], "source_obligations": row["source_obligations"],
                    "speech_units": [u["line_id"] for u in record_units],
                    "speech_speakers": {u["line_id"]: u["speaker_id"] for u in record_units}}
        require(fixture["records"][record] == expected, record + " fixture metadata mismatch")
        text = row["text"]
        serialized = json.dumps(text, ensure_ascii=False)
        require(hashlib.sha256(serialized.encode()).hexdigest() == row["text_sha256"],
                record + " text hash mismatch")
        if record in RECORD_UNITS:
            require([u["line_id"] for u in record_units] == list(RECORD_UNITS[record]),
                    record + " model unit order mismatch")
            require([u["speaker_id"] for u in record_units] == speakers[record],
                    record + " actor presence semantics mismatch")
            chunks = text if isinstance(text, list) else [{"text": text, "speaker": row["speaker"]}]
            require(len(chunks) == len(record_units), record + " text/unit length mismatch")
            for chunk, unit in zip(chunks, record_units):
                require(chunk["text"] == unit["text"] == unit["caption_text"] and
                        chunk["speaker"] == unit["speaker"], unit["line_id"] + " speech/caption mismatch")
        else:
            require(not record_units, record + " unexpected speech units")
    require(fixture["speech_metadata"] == [{k: u[k] for k in
            ("line_id", "record_id", "speaker_id", "laugh_opportunity")} for u in units],
            "Speech/laugh metadata or order mismatch")
    require(FLAG_IDS == {"RUMOR_CLEARED", "TERMS_CARD_AVAILABLE"}, "P09 grants outside branch scope")
    # These are explicit current-source obligations, reviewed alongside the retained contract.
    obligations = {
        "P09.LOOK.001": "Observation itself may clear chair misunderstanding; tag belongs to furniture.",
        "P09.CHOICE.001": "Direct question succeeds without object ritual.",
        "P09.FAILURE.001": "Immediate factual correction; no relationship penalty or persuasion lock.",
        "P09.DIALOGUE.002": "Care, agreed guest/noise arrangement, renewal, funded/scheduled repair all explicit; card unsigned now, signed only P14.",
        "P09.READ.002": "Plain-language fictional promise; no real tenancy guarantee or signed claim.",
        "P09.SUCCESS.001": "RUMOR_CLEARED and TERMS_CARD_AVAILABLE only; later commitment still needed.",
        "P09.CHOICE.004": "May explicitly connect their shared wish; no new dependency.",
    }
    for record, text in obligations.items():
        require(text in fixture["records"][record]["source_obligations"], record + " obligation mismatch")
    gdd = (authority / "complete-body.md").read_text()
    require("VC01_WON AND VC02_WON AND VC03_WON AND VC04_WON" in gdd,
            "Four separate finale contest wins missing")
    result = {"status": "PASS_CURRENT_AUTHORITY", "records": 20, "speech_units": 20,
              "record_order": "matched", "unit_order": "matched", "record_text_hashes": "matched",
              "speech_captions_and_speakers": "matched", "fixture_obligations": "matched",
              "actor_sequences": speakers, "reviewed_mechanics_obligations": obligations,
              "gdd_matches_checkpoint02": True, "model_modified": False,
              "historical_comparison_limit": "Historical catalog/speech JSON unavailable. This is a current-authority validation, not proof of unchanged old P09 text."}
    (ROOT / "evidence/gate3-current-authority.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
