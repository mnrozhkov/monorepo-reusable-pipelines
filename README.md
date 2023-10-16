
# Install 

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Run  pipelines 

### Run `pipeline_a_segment` projects

```
dvc exp run -R pipeline_a_segment/x
dvc exp run -R pipeline_a_segment/y
dvc exp run -R pipeline_a_segment/z

```

### Run `pipeline_b_detect` projects

```
dvc exp run -R pipeline_b_detect/i
dvc exp run -R pipeline_b_detect/j
```

## Run a pipeline (target/data/customer) 

`run.sh` script copies `dvc.yaml` template for a target division, and then runs a DVC pipeline.
 
```bash
./run.sh PROJECT TARGET 
```
Arguments:
- PROJECT - Path to a project/pipeline/model directory with a common `template_dvc.yaml`
- TARGET - Name of the target/data/customer to apply DVC pipeline to

Examples 
```bash
 # Run a segmentation pipeline for customer `x`
./run.sh pipeline_a_segment x
```

# Run multiple pipelines (list of targets)

Parse list of targets and run DVC pipeline for each of them
 
```bash
./run_targets.sh PROJECT TARGETS 
```
Arguments:
- PROJECT - Path to a project/pipeline/model directory with a common `template_dvc.yaml`
- TARGETS - Comma separated list of targets (no spaces in between)

Examples 
```bash
 # Run a detection pipeline for each target
./run_targets.sh pipeline_a_segment x,y,z
./run_targets.sh pipeline_b_detect i,j
```


# Cloud Versioning Workflows

## 1 - Setup Remote Storages

Add `local` remote
```
mkdir /tmp/monorepo-reusable-pipelines
dvc remote add --local -d local /tmp/monorepo-reusable-pipelines
```

Add `remote-i` remote
```
dvc remote add remote-i s3://cse-cloud-version/monorepo-reusable-pipelines/remote-i/ 
dvc remote modify remote-i version_aware true
```

Add `remote-j` remote
```
dvc remote add remote-j s3://cse-cloud-version/monorepo-reusable-pipelines/pipeline_b_detect/j/ 
dvc remote modify remote-j version_aware true
```



# Changes

**Oct 16, 2023 - Add metrics tracking**
- metrics saved with DVCLive (in `ml/src/train.py` script)
- for project `pipeline_a_segment` - metrics saved in `PROJECT/dvclive/`, metrics/plot files automatically added to the root `dvc.yaml`, version with Git 
- for project `pipeline_b_detect` - metrics saved in `PROJECT/results/`, metrics/plot files specified in `dvc.yaml` (as outs in the `train` stage), version with DVC (not Git)
- in both cases DVC updates metrics/plots in Studio/VSCode in real time