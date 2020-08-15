# What is this repository about?

This repository hosts a set of simple examples that use CMSSW EDAnalyzers to extract trigger information for CMS Open/Legacy Data. Currently, this repository has two main branches, 2010 and 2011 (works for 2012 as well) corresponding to the CMS data that has been so far released.
The examples are organized in packages, each of which has its own instructions.  

Below is a general description of the common ingedients used for building the snippets in these examples.

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
