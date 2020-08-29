# LD-flag-cleanup


LD-flag-cleanup is a CLI tool to allow you to delete feature flags by filtering with "tags: in your LaunchDarkly platform


## Installation

### Initial setup

- Clone the repo locally `git clone https://github.com/launchdarkly-labs/ld-flag-cleanup.git`
- Create a `.env` file and fill in the correct values below, without quotes:

        LD_API_KEY=$YOUR_API_KEY
        LD_PROJ_KEY=$YOUR_PROJECT_KEY
        LD_ENV_KEY=$YOUR_ENVIRONMENT_KEY

### How to run it:

- Ensure that you have [`python3`](https://www.python.org/downloads/)
- Run `virtualenv venv` to create a virtualenv, then activate it.
- Run `pip install -r requirements.txt` to install dependencies.
- Run `python main.py create_delete_list` to generate a list of flags (stored in replay/toDelete) matching the delete criteria
- Run `python main.py delete_flags` to delete feature flags from the list generated in the previous step

### Delete criteria:

- Any feature flag not tagged with "real"

### Sample API Token Policy:
```
[
  {
    "notResources": [
      "proj/support-service:env/*:flag/*;real"
    ],
    "actions": [
      "*"
    ],
    "effect": "allow"
  }
]
```
