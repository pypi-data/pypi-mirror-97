TEMPLATE_PROJECT_DIRS = [
    "src/",
    "assets/",
    "tests/",
]

TEMPLATE_PROJECT_FILES = [
    "template/src/endpoints.py",
    "template/assets/model.joblib",
    "template/assets/loans_test.pqt",
    "template/tests/test_accuracy.py",
    "template/tests/test_plausibility.py",
    "template/tests/test_schema.py",
    "template/tests/test_taktile_endpoint_tests.py",
    "template/.gitignore",
    "template/.gitattributes",
    "template/.buildfile",
    "template/.dockerignore",
    "template/README.md",
    "template/requirements.txt",
]


CONFIG_FILE_TEMPLATE = """
# If this option is set only commits with a commit message starting
# by the deployment_prefix will be deployed
# deployment_prefix: "#deploy"

service:

  # For the `instance_type` format, use the following: <instance_kind>.<instance_size>
  # Only 'gp' (general purpose) instance_kind is supported for now
  # instance_size can be: small, medium, large, xlarge, or xxlarge.
  # This is the instance type that will be used for both arrow and rest

  # Rest deployment scaling parameters
  rest:
    instance_type: gp.small
    # Maximum and minimum number of replicas to which the REST service is allowed to reach
    # by the auto-scaler
    max_replicas: 1
    # Minimum, or starting number of replicas
    replicas: 1

  # Arrow deployment scaling parameters
  arrow:
    instance_type: gp.small
    # Arrow # replicas are fixed and don't autoscale
    replicas: 1

version: {version}
"""
