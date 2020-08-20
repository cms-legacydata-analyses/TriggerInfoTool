# What is this repository about?

This repository hosts a set of simple examples that use CMSSW EDAnalyzers to extract trigger information for CMS Open/Legacy Data. Currently, this repository has two main branches, 2010 and 2011 (which also works for 2012), corresponding to the CMS data that has been so far released.  Please choose the one you need as instructions may vary a little.

The examples are organized in packages.  Here is a summary of what they contain:

* GeneralInfoAnalyzer: several C++ snippets on how to access trigger information such as metadata, prescales, module information, etc.
* ModuleInTriggerAnalyzer: shows how to dump all the modules for a specific trigger and/or obtain the last active module (filter) of a trigger.
* TriggerMatchingAnalyzer: how to match reconstructed tracks to objects that fired a trigger (or possible set of triggers) that contain a specific module
* TriggerSimplePrescalesAnalyzer: use wildcards to acces different versions of the same trigger, check their L1 and HLT prescales, and whether the trigger accepted the event or not

[Below](#trigger-info-analysis-tool) is a general description of the common ingredients used for building the snippets in these examples.

# Continuous Integration

This repository contains also [a github workflow](.github/workflows/main.yml), which runs the test jobs on the CMS open data container using github free resources. It sets up a minikube environment and runs a workflow defined with argo workflow engine. The ouput is returned as a github artifcat. The workflow is triggered by a pull request. The test workflows are defined in [argo-workflow.yaml](argo-workflow.yaml).

# Usage instructions

Usage instructions are very similar for the different example packages in this repository.  Please replace the placeholders in this instructions, which are defined right below, with the appropiate names as they fit your interest.

+ {packagename}: the name of a package in this repository; e.g., `TriggerSimplePrescalesAnalyzer`.
+ {configname}: the name of the config file within in the python directory in the corresponding package; e.g., `simpleprescalesinfoanalyzer_cfg.py`

First, you have to create a [VM](http://opendata.cern.ch/docs/cms-virtual-machine-2011 "CMS 2011 Virtual Machines: How to install") from the CMS Open Data website or set up a [Docker container](http://opendata.cern.ch/docs/cms-guide-docker). 

Then follow these steps:

- Create a CMSSW environment (if using the Docker container, this step can be skipped as they are release-specific): 

    ```
    cmsrel CMSSW_5_3_32
    ```

- Change to the CMSSW_5_3_32/src/ directory:

    ```
    cd CMSSW_5_3_32/src/
    ```

- Initialize the CMSSW environment:

  ```
  cmsenv
  ```

- Obtain the code from git and move it to the `src` area:

  ```
  git clone git://github.com/cms-legacydata-analyses/TriggerInfoTool.git
  cd TriggerInfoTool
  ```
  
- Go to the TriggerInfoTool/{packagename} area.  Note that the code lives under `src`

  ```
  cd {packagename}
  ```

- Compile everything:

  ```
  scram b
  ```

- Make a soft link to the python configuration file

```
ln -s python/{configname} .
```

- Make symbolic links to the conditions database

```
ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA FT_53_LV5_AN1
ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db FT_53_LV5_AN1_RUNA.db
```

- Make sure the `cms-opendata-conddb.cern.ch` directory has actually expanded in your VM or Docker container.  One way of doing this is executing:

```
ls -l
ls -l /cvmfs/
```

You should now see the `cms-opendata-conddb.cern.ch` link in the `/cvmfs` area.


- Run the CMSSW executable in the background and dump the output in a log file with any name (full.log in this case)

```
cmsRun {configname} > full.log 2>&1 &
```

- Check the development of the job if needed:

```
tail -f full.log
```

*NOTE*: The first time you execute the job, it will take a long time (depending on your connection speed) to the point that it looks like it is not doing anything.  That is fine.  This is because the database payload files will be downloaded/cached locally in the VM or container (if using cvmfs).  Later attempts should be faster, however.


# Trigger Info Analysis Tool

## Description

The skeleton of the EDAnalyzers used in this repository, and/or the code snippets that can be extracted from them, could be used for physics analysis.

The code has plenty of in-line comments to make it more understandable (hopefuly) and to point potential users to the original sources. It has been put together compiling the most important pieces of already-available CMSSW software, which will be described in the section below.

## The CMS Trigger System

Physically, an event is the result of a single readout of the detector electronics and the signals that will (in general) have been generated by particles, tracks, energy deposits, present in a number of bunch crossings. The task of the online Trigger and Data Acquisition System (TriDAS) is to select, out of the millions of events recorded in the detector, the most interesting 100 or so per second, and then store them for further analysis. An event has to pass two independent sets of tests, or Trigger Levels, in order to qualify. The tests range from simple and of short duration (Level-1) to sophisticated ones requiring significantly more time to run (High Levels 2 and 3, called HLT). In the end, the HLT system creates RAW data events containing:
- the detector data,
- the level 1 trigger result
- the result of the HLT selections (HLT trigger bits)
- and some of the higher-level objects created during HLT processing.

Original Source: [TriggerSystem](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCMSSWFramework?rev=10#TriggerSystemi "TriggerSystem")


### The HLT

The HLT contains many trigger paths, each corresponding to a dedicated trigger (such as a prescaled single-electron trigger or a 3-jets-with-MET trigger). A path consists of several steps (software modules), each module performing a well-defined task such as unpacking (raw to digi), reconstruction of physics objects (electrons, muons, jets, MET, etc.), making intermediate decisions triggering more refined reconstructions in subsequent modules, or calculating the final decision for a trigger path. The CMSSW Framework/EDM ensures that if an intermediate filter decision on a trigger path is negative, the rest of the path is not executed (skipped) and the specific trigger is regarded as rejecting the event. In order to save CPU time, each reconstruction step is followed by a filter in order to avoid running time-consuming reco code if it is already clear it will not be needed.
In general it is expected that all HLT trigger paths are run, even if the event is already accepted by a path. In case this turns out to be too time-consuming, a truncated mode of HLT operations should be foreseen where the HLT short-circuits after the first accept (and after the triggers needed to classify the event for a primary data set and output stream are computed) and does not run the rest of the triggers. Presumably, the triggers not run online could be run in the offline reconstruction step to compute all trigger bits (for events written out) in order to get a complete trigger picture allowing trigger efficiency studies.
Each HLT trigger path must be seeded by one or more L1 trigger bit seeds: the first filter module in each HLT path is looking for a suitable L1 seed (consisting of L1 bit[s] and L1 object[s]) as a starting point for that specific HLT trigger.

Original Source: [SWGuideHighLevelTrigger](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideHighLevelTrigger?rev=120#How_it_works "SWGuideHighLevelTrigger")

### Persistent Trigger Results Objects and Available Software

Two persistent HLT products are available:

- TriggerResults: (subclassed from HLTGlobalStatus object), containing 
all the usual decision bits.  

    The TriggerResults product (available for events written to output) 
allows access to the configuration and trigger decisions, i.e., 
all the usual "trigger bits", including:
    1. Final decision of individual path and of full trigger table
    2. Which triggers were run (some triggers may not run due to lack of a corresponding L1 seed or HLT running in truncated mode)
    3. For each trigger rejecting the event, (the index of) which intermediate or final module instances on the path rejected the event
    4. For each trigger encountering an error condition, (the index of) 
which module instances on the path encountered un-recoverable 
errors.

    The corresponding code can be found in [DataFormats/Common/interface/TriggerResults.h](https://github.com/cms-sw/cmssw/blob/CMSSW_5_3_X/DataFormats/Common/interface/TriggerResults.h "TriggerResults.h") and [DataFormats/Common/interface/HLTGlobalStatus.h](https://github.com/cms-sw/cmssw/blob/CMSSW_5_3_X/DataFormats/Common/interface/HLTGlobalStatus.h "HLTGlobalStatus.h")

- TriggerEvent: summarising the "L3" trigger collections and "L3" filter decisions.  

    The corresponding code can be found in [DataFormats/HLTReco/interface/TriggerEvent.h](https://github.com/cms-sw/cmssw/blob/CMSSW_5_3_X/DataFormats/HLTReco/interface/TriggerEvent.h "TriggerEvent.h")

Additionally, the package [HLTrigger/HLTcore](htts://github.com/cms-sw/cmssw/tree/CMSSW_5_3_X/HLTrigger/HLTcore "HLTrigger/HLTcore") contains several 
analyzers pulling out the trigger information. 
You can use the corresponding analyzers directly - see their cfi files in 
the python subdirectory - or copy relevant code pieces into your modules.

- TriggerSummaryAnalyzerAOD: analyser printing the content of the TriggerEvent product
- HLTEventAnalyzerAOD: analyser combining the information from TriggerResults and TriggerEvent products

The HLTEventAnalyzer plugin make use of the helper class [HLTConfigProvider](https://github.com/cms-sw/cmssw/blob/CMSSW_5_3_X/HLTrigger/HLTcore/interface/HLTConfigProvider.h "HLTConfigProvider") (also in [HLTrigger/HLTcore](https://github.com/cms-sw/cmssw/tree/CMSSW_5_3_X/HLTrigger/HLTcore "HLTrigger/HLTcore")), which extracts the HLT configuration (paths, modules) from the provenance. 

Note: this helper class must be initialised calling it's init(...) 
from the beginRun() method of your plugin using this helper class. The reason 
that it has to be (re-)initialised in beginRun() is that the HLT 
configuration can (only) change at the boundary between runs. 

Original Source: [Persistent Trigger Results Objects](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideHighLevelTrigger?rev=120#Persistent_Trigger_Results_Object "Persistent Trigger Results Objects") 
