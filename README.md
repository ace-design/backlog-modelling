# Backlog Modelling reference implementation

  - Authors: 
    - Sébastien Mosser
    - Corinne Pulgar
    - Vladimir Reinharz
  - Contributors:
    - Benjamin Benni (Instant systems)
    - Guilhem Molines (IBM)

## How to setup the environmenent?

On your local computer, we rely on Python 3.9 and `pipenv` to install dependencies

```
 pipenv install
```

The code uses _numpy_, a scientific computing library that could be complicated to setup locally. Thus, we provide a Docker version of the code that contains all the dependencies:

```
TODO
```

## How to run the scenarios locally?

We assume here an up and running environment. The `Makefile` provide an easy way to start the scenarios using the right environment. For example, to run the first scenario:

```
make scenario_1
```

By convention, each scenario produces a PDF file as output, stored in the `output` directory

## How to run the scenarios (with docker)?

As the scenarios can consume a lot of memory (the twoi last ones), be sure that you have allocated up to 4Gb of RAM to containers in your local Docker settings.

To run a scenario, use the `docker_run.sh` script, indicating which scenario you want to execute and which directory to be used as output.

## How to access to the datasets?

We release as part of this artefact the following datasets:

  - `dataset/raw`: the original files published by Dalpiaz in 2018;
  - `dataset/gilson`: the result of the analysis of these stories by the the team of the University of Canterburry (NZ);
  - `dataset/cases`: a JSON format of each stories processed by Visual Narrator and the approach form gilson et al.

If you want to run Visual Narrator on top of these file, we provide a docker image and a shell script to make it easier (in `dataset/raw/visual_narrator.sh`).

## How to acces to the result without recomputing?

The resulting figures for each dataset are available in the `results` directory.

## How to access to the code of each scenairo?

The Python code used to support each scenario is available in the `scenarios` directory. When a scenario requires sopme additional data (_e.g._, ground truth, or exat information), these data are stored in the `scenarios/data` directory.

## How to access to the metamodel?

The metamodel and graph-based implementation of the approach is stored in the `backlog` directory.