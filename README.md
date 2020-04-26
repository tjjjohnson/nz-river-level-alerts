# nz-river-level-alerts

`dev_environment_setup.sh` will install various dependencies required to run on amazon linux 2.

`aws configure` which will require access key ID and secret as well as a region. This is required for the email service and also deployment to lambda.

then run `src/lambda_function.py`

# Lambda setup

`make update-lambda`

or if you just want to build the lambda zip file without deploying the function

`make build-lambda`

## Environment variables

```
RIVER_LEVEL_ALERTS_EMAIL_ADDRESS=email_address
RIVER_LEVEL_ALERTS_RULES_YAML=s3://bucket/river_level_alerts_rules.yaml
```

## Rules

By default the rules will be taken from `example_alert_rules.yaml` but you should set the `RIVER_LEVEL_ALERTS_RULES_YAML` environment variable to override this.

```
- test_rule:
  Location: Whareroa Whareroa at FishTrap
  Direction: above
  Level: 0.5
```