# Editable opening and audience art

The eight reviewed masters generate 64 performed poses plus exact names, motifs, title and stable props. The audience background uses the same 320x144 scene and existing return/talk rectangles. Original palette 999 and font 0 are included in references. Individual historical source qualifications remain in GENERATION-PROVENANCE.json.

From this directory, with Python 3, Pillow and NumPy:

    python tools/export_opening.py export --config tools/export-config-all-eight-r1.json --output /new/isolated-art-output
    python -m unittest discover -s tools -p 'test_*.py'

The exporter refuses to overwrite output resources. Inspect generated pixel proofs before changing runtime inputs. Public packaging changes only path references in provenance and the optional reference extraction helper; runtime VIEW bytes are exact.
