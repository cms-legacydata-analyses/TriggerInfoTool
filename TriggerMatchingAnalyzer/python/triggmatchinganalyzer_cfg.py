import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
#if more events are activated, choose to print every 100:
#process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#        'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/SingleElectron/AOD/12Oct2013-v1/10000/1045436C-1240-E311-851B-003048D2BF1C.root'
	'root://eospublic.cern.ch//eos/opendata/cms/Run2011A/Jet/AOD/12Oct2013-v1/20001/948D96B8-1F3F-E311-AEE6-02163E008D66.root'
    )
)
#needed to get the actual prescale values used from the global tag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db')
process.GlobalTag.globaltag = 'FT_53_LV5_AN1::All'

#This is inspired by https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideHLTAnalysis
process.demo = cms.EDAnalyzer('TriggMatchingAnalyzer',
                 filterName = cms.string("hltSingleJet190Regional"),
                 TrackCollection = cms.InputTag("generalTracks")
                             )




process.p = cms.Path(process.demo)
