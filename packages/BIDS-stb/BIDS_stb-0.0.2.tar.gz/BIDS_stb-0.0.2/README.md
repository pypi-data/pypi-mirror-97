# BIDS_stb


Converts BIDS formatted jsons into jsons with single trial beta outputs.
Takes original json path, target conditions, the number of total trials, and an optional output directory.
Generates json for each trial of each condition with single trial beta output.

## Options:
  -c, --condition_names TEXT  Condition names as they appear in the BIDS file.
                              Takes multiple inputs separated by -c.

  -n, --num_trials INTEGER    Number of trials. Defaults to 1.
  
  -d, --json_new_dir TEXT     Output directory for new JSONs. Defaults to
                              current working directory.

  --help                      Show help.
