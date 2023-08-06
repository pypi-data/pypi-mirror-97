import json
import pytest

@pytest.fixture(scope="session")
def orig_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("orig")

@pytest.fixture(scope="session")
def sample_model_dict():
    return {
      "Name": "ds114_model1",
      "Description": "sample model for ds114",
      "Input": {
        "task": "fingerfootlips"
      },
      "Steps": [
        {
          "Level": "run",
          "Transformations": [
            {
              "Name": "Factor",
              "Input": ["trial_type"]
            },
            {
              "Name": "Convolve",
              "Input": [
                "trial_type.Finger",
                "trial_type.Foot",
                "trial_type.Lips"
              ]
            }
          ],
          "Model": {
            "X": [
              "trial_type.Finger",
              "trial_type.Foot",
              "trial_type.Lips",
              "framewise_displacement",
              "trans_x", "trans_y", "trans_z", "rot_x", "rot_y", "rot_z",
              "a_comp_cor_00", "a_comp_cor_01", "a_comp_cor_02",
              "a_comp_cor_03", "a_comp_cor_04", "a_comp_cor_05"
            ]
          },
          "Contrasts": [
            {
              "Name": "finger_vs_others",
              "ConditionList": [
                "trial_type.Finger",
                "trial_type.Foot",
                "trial_type.Lips"
              ],
              "Weights": [
                1,
                -0.5,
                -0.5
              ],
              "Type": "t"
            }
          ]
        },
        {
          "Level": "session",
          "Transformations": [
            {
              "Name": "split",
              "Input": ["finger_vs_others"],
              "By": "session"
            }
          ]
        },
        {
          "Level": "subject",
          "Model": {
            "X": [
              "finger_vs_others.test",
              "finger_vs_others.retest"
            ]
          },
          "Contrasts": [
            {
              "Name": "session_diff",
              "ConditionList": [
                "finger_vs_others.test",
                "finger_vs_others.retest"
              ],
              "Weights": [1, -1],
              "Type": "t"
            }
          ]
        },
        {
          "Level": "dataset",
          "DummyContrasts": {
            "Conditions": ["session_diff"],
            "Type": "t"
          }
        }
      ]
    }

@pytest.fixture(scope="session")
def json_orig_path(orig_dir, sample_model_dict):
    orig_json = orig_dir.dirpath() / "input_model.json"
    orig_json.ensure()
    with open(str(orig_json), "w") as model_f:
        json.dump(sample_model_dict, model_f)

    return str(orig_json)

@pytest.fixture(scope="session")
def condition_names():
    return ["trial_type.Lips", "trial_type.Foot"]

@pytest.fixture(scope="session")
def num_trials():
    return 3

@pytest.fixture(scope="session")
def json_new_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("new")

@pytest.fixture(scope="session")
def expected_output():
    return [
      {
        "Name": "ds114_model1",
        "Description": "sample model for ds114",
        "Input": {
          "task": "fingerfootlips"
        },
        "Steps": [
          {
            "Level": "run",
            "Transformations": [
              {
                'Name': 'Factor',
                'Input': [
                  'trial_number'
                ]
              },
              {
                "Name": "Factor",
                "Input": [
                  "trial_type"
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'trial_number.0',
                  'trial_type.Foot'
                ],
                'Output': [
                  'trial-000_trial_type.Foot'
                ]
              },
              {
                'Name': 'Not',
                'Input': [
                  'trial_number.0'
                ], 
                'Output': [
                  'other_trials'
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'other_trials',
                  'trial_type.Foot'
                ],
                'Output': [
                  'other_trials_trial_type.Foot'
                ]
              },
              {
                "Name": "Convolve",
                "Input": [
                  "trial-000_trial_type.Foot",
                  "other_trials_trial_type.Foot",
                  "trial_type.Finger",
                  "trial_type.Lips"
                ]
              }
            ],
            "Model": {
              "X": [
                "trial-000_trial_type.Foot",
                "other_trials_trial_type.Foot",
                "trial_type.Finger",
                "trial_type.Lips",
                "framewise_displacement",
                "trans_x",
                "trans_y",
                "trans_z",
                "rot_x",
                "rot_y",
                "rot_z",
                "a_comp_cor_00",
                "a_comp_cor_01",
                "a_comp_cor_02",
                "a_comp_cor_03",
                "a_comp_cor_04",
                "a_comp_cor_05"
              ]
            },
            "DummyContrasts": {
              "Conditions": [
                "trial-000_trial_type.Foot"
              ],
              "Type": "t"
            }
          }
        ]
      },
      {
        "Name": "ds114_model1",
        "Description": "sample model for ds114",
        "Input": {
          "task": "fingerfootlips"
        },
        "Steps": [
          {
            "Level": "run",
            "Transformations": [
              {
                'Name': 'Factor',
                'Input': [
                  'trial_number'
                ]
              },
              {
                "Name": "Factor",
                "Input": [
                  "trial_type"
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'trial_number.1',
                  'trial_type.Foot'
                ],
                'Output': [
                  'trial-001_trial_type.Foot'
                ]
              },
              {
                'Name': 'Not',
                'Input': [
                  'trial_number.1'
                ], 
                'Output': [
                  'other_trials'
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'other_trials',
                  'trial_type.Foot'
                ],
                'Output': [
                  'other_trials_trial_type.Foot'
                ]
              },
              {
                "Name": "Convolve",
                "Input": [
                  "trial-001_trial_type.Foot",
                  "other_trials_trial_type.Foot",
                  "trial_type.Finger",
                  "trial_type.Lips"
                ]
              }
            ],
            "Model": {
              "X": [
                "trial-001_trial_type.Foot",
                "other_trials_trial_type.Foot",
                "trial_type.Finger",
                "trial_type.Lips",
                "framewise_displacement",
                "trans_x",
                "trans_y",
                "trans_z",
                "rot_x",
                "rot_y",
                "rot_z",
                "a_comp_cor_00",
                "a_comp_cor_01",
                "a_comp_cor_02",
                "a_comp_cor_03",
                "a_comp_cor_04",
                "a_comp_cor_05"
              ]
            },
            "DummyContrasts": {
              "Conditions": [
                "trial-001_trial_type.Foot"
              ],
              "Type": "t"
            }
          }
        ]
      },
      {
        "Name": "ds114_model1",
        "Description": "sample model for ds114",
        "Input": {
          "task": "fingerfootlips"
        },
        "Steps": [
          {
            "Level": "run",
            "Transformations": [
              {
                'Name': 'Factor',
                'Input': [
                  'trial_number'
                ]
              },
              {
                "Name": "Factor",
                "Input": [
                  "trial_type"
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'trial_number.2',
                  'trial_type.Foot'
                ],
                'Output': [
                  'trial-002_trial_type.Foot'
                ]
              },
              {
                'Name': 'Not',
                'Input': [
                  'trial_number.2'
                ], 
                'Output': [
                  'other_trials'
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'other_trials',
                  'trial_type.Foot'
                ],
                'Output': [
                  'other_trials_trial_type.Foot'
                ]
              },
              {
                "Name": "Convolve",
                "Input": [
                  "trial-002_trial_type.Foot",
                  "other_trials_trial_type.Foot",
                  "trial_type.Finger",
                  "trial_type.Lips"
                ]
              }
            ],
            "Model": {
              "X": [
                "trial-002_trial_type.Foot",
                "other_trials_trial_type.Foot",
                "trial_type.Finger",
                "trial_type.Lips",
                "framewise_displacement",
                "trans_x",
                "trans_y",
                "trans_z",
                "rot_x",
                "rot_y",
                "rot_z",
                "a_comp_cor_00",
                "a_comp_cor_01",
                "a_comp_cor_02",
                "a_comp_cor_03",
                "a_comp_cor_04",
                "a_comp_cor_05"
              ]
            },
            "DummyContrasts": {
              "Conditions": [
                "trial-002_trial_type.Foot"
              ],
              "Type": "t"
            }
          }
        ]
      },
      {
        "Name": "ds114_model1",
        "Description": "sample model for ds114",
        "Input": {
          "task": "fingerfootlips"
        },
        "Steps": [
          {
            "Level": "run",
            "Transformations": [
              {
                'Name': 'Factor',
                'Input': [
                  'trial_number'
                ]
              },
              {
                "Name": "Factor",
                "Input": [
                  "trial_type"
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'trial_number.0',
                  'trial_type.Lips'
                ],
                'Output': [
                  'trial-000_trial_type.Lips'
                ]
              },
              {
                'Name': 'Not',
                'Input': [
                  'trial_number.0'
                ], 
                'Output': [
                  'other_trials'
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'other_trials',
                  'trial_type.Lips'
                ],
                'Output': [
                  'other_trials_trial_type.Lips'
                ]
              },
              {
                "Name": "Convolve",
                "Input": [
                  "trial-000_trial_type.Lips",
                  "other_trials_trial_type.Lips",
                  "trial_type.Finger",
                  "trial_type.Foot"
                ]
              }
            ],
            "Model": {
              "X": [
                "trial-000_trial_type.Lips",
                "other_trials_trial_type.Lips",
                "trial_type.Finger",
                "trial_type.Foot",
                "framewise_displacement",
                "trans_x",
                "trans_y",
                "trans_z",
                "rot_x",
                "rot_y",
                "rot_z",
                "a_comp_cor_00",
                "a_comp_cor_01",
                "a_comp_cor_02",
                "a_comp_cor_03",
                "a_comp_cor_04",
                "a_comp_cor_05"
              ]
            },
            "DummyContrasts": {
              "Conditions": [
                "trial-000_trial_type.Lips"
              ],
              "Type": "t"
            }
          }
        ]
      },
      {
        "Name": "ds114_model1",
        "Description": "sample model for ds114",
        "Input": {
          "task": "fingerfootlips"
        },
        "Steps": [
          {
            "Level": "run",
            "Transformations": [
              {
                'Name': 'Factor',
                'Input': [
                  'trial_number'
                ]
              },
              {
                "Name": "Factor",
                "Input": [
                  "trial_type"
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'trial_number.1',
                  'trial_type.Lips'
                ],
                'Output': [
                  'trial-001_trial_type.Lips'
                ]
              },
              {
                'Name': 'Not',
                'Input': [
                  'trial_number.1'
                ], 
                'Output': [
                  'other_trials'
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'other_trials',
                  'trial_type.Lips'
                ],
                'Output': [
                  'other_trials_trial_type.Lips'
                ]
              },
              {
                "Name": "Convolve",
                "Input": [
                  "trial-001_trial_type.Lips",
                  "other_trials_trial_type.Lips",
                  "trial_type.Finger",
                  "trial_type.Foot"
                ]
              }
            ],
            "Model": {
              "X": [
                "trial-001_trial_type.Lips",
                "other_trials_trial_type.Lips",
                "trial_type.Finger",
                "trial_type.Foot",
                "framewise_displacement",
                "trans_x",
                "trans_y",
                "trans_z",
                "rot_x",
                "rot_y",
                "rot_z",
                "a_comp_cor_00",
                "a_comp_cor_01",
                "a_comp_cor_02",
                "a_comp_cor_03",
                "a_comp_cor_04",
                "a_comp_cor_05"
              ]
            },
            "DummyContrasts": {
              "Conditions": [
                "trial-001_trial_type.Lips"
              ],
              "Type": "t"
            }
          }
        ]
      },
      {
        "Name": "ds114_model1",
        "Description": "sample model for ds114",
        "Input": {
          "task": "fingerfootlips"
        },
        "Steps": [
          {
            "Level": "run",
            "Transformations": [
              {
                'Name': 'Factor',
                'Input': [
                  'trial_number'
                ]
              },
              {
                "Name": "Factor",
                "Input": [
                  "trial_type"
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'trial_number.2',
                  'trial_type.Lips'
                ],
                'Output': [
                  'trial-002_trial_type.Lips'
                ]
              },
              {
                'Name': 'Not',
                'Input': [
                  'trial_number.2'
                ], 
                'Output': [
                  'other_trials'
                ]
              },
              {
                'Name': 'And',
                'Input': [
                  'other_trials',
                  'trial_type.Lips'
                ],
                'Output': [
                  'other_trials_trial_type.Lips'
                ]
              },
              {
                "Name": "Convolve",
                "Input": [
                  "trial-002_trial_type.Lips",
                  "other_trials_trial_type.Lips",
                  "trial_type.Finger",
                  "trial_type.Foot"
                ]
              }
            ],
            "Model": {
              "X": [
                "trial-002_trial_type.Lips",
                "other_trials_trial_type.Lips",
                "trial_type.Finger",
                "trial_type.Foot",
                "framewise_displacement",
                "trans_x",
                "trans_y",
                "trans_z",
                "rot_x",
                "rot_y",
                "rot_z",
                "a_comp_cor_00",
                "a_comp_cor_01",
                "a_comp_cor_02",
                "a_comp_cor_03",
                "a_comp_cor_04",
                "a_comp_cor_05"
              ]
            },
            "DummyContrasts": {
              "Conditions": [
                "trial-002_trial_type.Lips"
              ],
              "Type": "t"
            }
          }
        ]
      }
    ] 