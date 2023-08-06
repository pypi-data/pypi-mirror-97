import pytest
import json
from pathlib import Path
from ..stb import _stb

def test_stb_model(json_orig_path, condition_names, num_trials, json_new_dir, expected_output):
    _stb(json_orig_path, condition_names, num_trials, json_new_dir)

    output_files = [
        "stb_trial-000_trial_type.Foot.json",
        "stb_trial-001_trial_type.Foot.json",
        "stb_trial-002_trial_type.Foot.json",
        "stb_trial-000_trial_type.Lips.json",
        "stb_trial-001_trial_type.Lips.json",
        "stb_trial-002_trial_type.Lips.json",
    ]
    output_files = [Path(json_new_dir) / out_file for out_file in output_files]

    assert len(output_files) == len(expected_output)

    for out_file, xo in zip(output_files, expected_output):
        produced_json = json.loads(out_file.read_text())

        assert produced_json == xo
