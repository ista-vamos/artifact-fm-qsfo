# Default recipe (runs when `just` is invoked with no args)
default:
    @just --list

# -------------------------------------------------
# Variables
# -------------------------------------------------
# Allow overriding from the CLI: `just PROFILE=release build`

QSFO := "qsfo"
PROFILE := ""
FEATURES := ""

# Convert FEATURES into a flag only if set

profile_flag := if PROFILE == "" { "" } else { "--profile {{PROFILE}}" }
features_flag := if FEATURES == "" { "" } else { "--features {{FEATURES}}" }

smoketest:
  @echo "TODO"

run:
  @just run-avoidance
  @just run-f16

# Build the project with all its features
# build-all:
#     {{ CARGO }} build --all-targets --all-features {{ profile_flag }}
#     @just build-python

