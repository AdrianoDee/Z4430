
import copy
from PhysicsTools.PatAlgos.tools.helpers import *

#
# Clustering
#

from RecoEcal.EgammaClusterProducers.correctedHybridSuperClusters_cfi import *
uncleanedOnlyCorrectedHybridSuperClusters = correctedHybridSuperClusters.clone()
uncleanedOnlyCorrectedHybridSuperClusters.rawSuperClusterProducer = cms.InputTag("hybridSuperClusters","uncleanOnlyHybridSuperClusters")

uncleanedOnlyClustering = cms.Sequence(uncleanedOnlyCorrectedHybridSuperClusters)

#
# Tracking
#

from RecoEgamma.EgammaElectronProducers.ecalDrivenElectronSeeds_cfi import *
uncleanedOnlyElectronSeeds = ecalDrivenElectronSeeds.clone()
uncleanedOnlyElectronSeeds.barrelSuperClusters = cms.InputTag("uncleanedOnlyCorrectedHybridSuperClusters")
uncleanedOnlyElectronSeeds.endcapSuperClusters = cms.InputTag("")

from TrackingTools.GsfTracking.CkfElectronCandidateMaker_cff import *
uncleanedOnlyElectronCkfTrackCandidates = electronCkfTrackCandidates.clone()
uncleanedOnlyElectronCkfTrackCandidates.src = cms.InputTag("uncleanedOnlyElectronSeeds")

from TrackingTools.GsfTracking.GsfElectronGsfFit_cff import *
uncleanedOnlyElectronGsfTracks = electronGsfTracks.clone()
uncleanedOnlyElectronGsfTracks.src = 'uncleanedOnlyElectronCkfTrackCandidates'

uncleanedOnlyTracking = cms.Sequence(uncleanedOnlyElectronSeeds*uncleanedOnlyElectronCkfTrackCandidates*uncleanedOnlyElectronGsfTracks)

#
# Conversions
#

from RecoEgamma.EgammaPhotonProducers.conversionTrackCandidates_cfi import *
uncleanedOnlyConversionTrackCandidates = conversionTrackCandidates.clone()
uncleanedOnlyConversionTrackCandidates.scHybridBarrelProducer = cms.InputTag("uncleanedOnlyCorrectedHybridSuperClusters")
uncleanedOnlyConversionTrackCandidates.bcBarrelCollection  = cms.InputTag("hybridSuperClusters","uncleanOnlyHybridSuperClusters")
#uncleanedOnlyConversionTrackCandidates.scIslandEndcapProducer  = cms.InputTag("correctedMulti5x5SuperClustersWithPreshower")
#uncleanedOnlyConversionTrackCandidates.bcEndcapCollection  = cms.InputTag("multi5x5BasicClusters","multi5x5EndcapBasicClusters")

from RecoEgamma.EgammaPhotonProducers.ckfOutInTracksFromConversions_cfi import *
uncleanedOnlyCkfOutInTracksFromConversions = ckfOutInTracksFromConversions.clone()
uncleanedOnlyCkfOutInTracksFromConversions.src = cms.InputTag("uncleanedOnlyConversionTrackCandidates","outInTracksFromConversions")
uncleanedOnlyCkfOutInTracksFromConversions.producer = cms.string('uncleanedOnlyConversionTrackCandidates')
uncleanedOnlyCkfOutInTracksFromConversions.ComponentName = cms.string('uncleanedOnlyCkfOutInTracksFromConversions')

from RecoEgamma.EgammaPhotonProducers.ckfInOutTracksFromConversions_cfi import *
uncleanedOnlyCkfInOutTracksFromConversions = ckfInOutTracksFromConversions.clone()
uncleanedOnlyCkfInOutTracksFromConversions.src = cms.InputTag("conversionTrackCandidates","inOutTracksFromConversions")
uncleanedOnlyCkfInOutTracksFromConversions.producer = cms.string('conversionTrackCandidates')
uncleanedOnlyCkfInOutTracksFromConversions.ComponentName = cms.string('ckfInOutTracksFromConversions')

uncleanedOnlyCkfTracksFromConversions = cms.Sequence(uncleanedOnlyConversionTrackCandidates*uncleanedOnlyCkfOutInTracksFromConversions*uncleanedOnlyCkfInOutTracksFromConversions)

from RecoEgamma.EgammaPhotonProducers.conversionTrackSequence_cff import *
uncleanedOnlyGeneralConversionTrackProducer = generalConversionTrackProducer.clone()

from RecoEgamma.EgammaPhotonProducers.conversionTrackSequence_cff import *
uncleanedOnlyInOutConversionTrackProducer = inOutConversionTrackProducer.clone()
uncleanedOnlyInOutConversionTrackProducer.TrackProducer = cms.string('uncleanedOnlyCkfInOutTracksFromConversions')

from RecoEgamma.EgammaPhotonProducers.conversionTrackSequence_cff import *
uncleanedOnlyOutInConversionTrackProducer = outInConversionTrackProducer.clone()
uncleanedOnlyOutInConversionTrackProducer.TrackProducer = cms.string('uncleanedOnlyCkfOutInTracksFromConversions')

from RecoEgamma.EgammaPhotonProducers.conversionTrackSequence_cff import *
uncleanedOnlyGsfConversionTrackProducer = gsfConversionTrackProducer.clone()
uncleanedOnlyGsfConversionTrackProducer.TrackProducer = cms.string('uncleanedOnlyElectronGsfTracks')

uncleanedOnlyConversionTrackProducers  = cms.Sequence(uncleanedOnlyGeneralConversionTrackProducer*uncleanedOnlyInOutConversionTrackProducer*uncleanedOnlyOutInConversionTrackProducer*uncleanedOnlyGsfConversionTrackProducer)

from RecoEgamma.EgammaPhotonProducers.conversionTrackSequence_cff import *
uncleanedOnlyInOutOutInConversionTrackMerger = inOutOutInConversionTrackMerger.clone()
uncleanedOnlyInOutOutInConversionTrackMerger.TrackProducer2 = cms.string('uncleanedOnlyOutInConversionTrackProducer')
uncleanedOnlyInOutOutInConversionTrackMerger.TrackProducer1 = cms.string('uncleanedOnlyInOutConversionTrackProducer')

from RecoEgamma.EgammaPhotonProducers.conversionTrackSequence_cff import *
uncleanedOnlyGeneralInOutOutInConversionTrackMerger = generalInOutOutInConversionTrackMerger.clone()
uncleanedOnlyGeneralInOutOutInConversionTrackMerger.TrackProducer2 = cms.string('uncleanedOnlyGeneralConversionTrackProducer')
uncleanedOnlyGeneralInOutOutInConversionTrackMerger.TrackProducer1 = cms.string('uncleanedOnlyInOutOutInConversionTrackMerger')

from RecoEgamma.EgammaPhotonProducers.conversionTrackSequence_cff import *
uncleanedOnlyGsfGeneralInOutOutInConversionTrackMerger = gsfGeneralInOutOutInConversionTrackMerger.clone()
uncleanedOnlyGsfGeneralInOutOutInConversionTrackMerger.TrackProducer2 = cms.string('uncleanedOnlyGsfConversionTrackProducer')
uncleanedOnlyGsfGeneralInOutOutInConversionTrackMerger.TrackProducer1 = cms.string('uncleanedOnlyGeneralInOutOutInConversionTrackMerger')

uncleanedOnlyConversionTrackMergers = cms.Sequence(uncleanedOnlyInOutOutInConversionTrackMerger*uncleanedOnlyGeneralInOutOutInConversionTrackMerger*uncleanedOnlyGsfGeneralInOutOutInConversionTrackMerger)

from RecoEgamma.EgammaPhotonProducers.allConversions_cfi import *
uncleanedOnlyAllConversions = allConversions.clone()
uncleanedOnlyAllConversions.scBarrelProducer = cms.InputTag("uncleanedOnlyCorrectedHybridSuperClusters")
uncleanedOnlyAllConversions.bcBarrelCollection  = cms.InputTag("hybridSuperClusters","uncleanOnlyHybridSuperClusters")
#uncleanedOnlyAllConversions.scEndcapProducer = cms.InputTag("correctedMulti5x5SuperClustersWithPreshower")
#uncleanedOnlyAllConversions.bcEndcapCollection = cms.InputTag("multi5x5BasicClusters","multi5x5EndcapBasicClusters")
uncleanedOnlyAllConversions.src = cms.InputTag("uncleanedOnlyGsfGeneralInOutOutInConversionTrackMerger")

uncleanedOnlyConversions = cms.Sequence(uncleanedOnlyCkfTracksFromConversions*uncleanedOnlyConversionTrackProducers*uncleanedOnlyConversionTrackMergers*uncleanedOnlyAllConversions)

#
# Particle Flow Tracking
#

from RecoParticleFlow.PFTracking.pfTrack_cfi import *
uncleanedOnlyPfTrack = pfTrack.clone()
uncleanedOnlyPfTrack.GsfTrackModuleLabel = cms.InputTag("uncleanedOnlyElectronGsfTracks")

from RecoParticleFlow.PFTracking.pfConversions_cfi import *
uncleanedOnlyPfConversions = pfConversions.clone()
uncleanedOnlyPfConversions.conversionCollection = cms.InputTag("allConversions")

from RecoParticleFlow.PFTracking.pfTrackElec_cfi import *
uncleanedOnlyPfTrackElec = pfTrackElec.clone()
uncleanedOnlyPfTrackElec.PFConversions = cms.InputTag("uncleanedOnlyPfConversions")
uncleanedOnlyPfTrackElec.GsfTrackModuleLabel = cms.InputTag("uncleanedOnlyElectronGsfTracks")
uncleanedOnlyPfTrackElec.PFRecTrackLabel = cms.InputTag("uncleanedOnlyPfTrack")

uncleanedOnlyPfTracking = cms.Sequence(uncleanedOnlyPfTrack*uncleanedOnlyPfConversions*uncleanedOnlyPfTrackElec)

#
# Electrons
#

from RecoEgamma.EgammaElectronProducers.gsfElectronCores_cfi import *
uncleanedOnlyGsfElectronCores = ecalDrivenGsfElectronCores.clone()
uncleanedOnlyGsfElectronCores.gsfTracks = cms.InputTag("uncleanedOnlyElectronGsfTracks")
uncleanedOnlyGsfElectronCores.gsfPfRecTracks = cms.InputTag("uncleanedOnlyPfTrackElec")

from RecoEgamma.EgammaElectronProducers.gsfElectrons_cfi import *
uncleanedOnlyGsfElectrons = ecalDrivenGsfElectrons.clone()
uncleanedOnlyGsfElectrons.gsfPfRecTracksTag = cms.InputTag("uncleanedOnlyPfTrackElec")
uncleanedOnlyGsfElectrons.gsfElectronCoresTag = cms.InputTag("uncleanedOnlyGsfElectronCores")
uncleanedOnlyGsfElectrons.seedsTag = cms.InputTag("uncleanedOnlyElectronSeeds")

uncleanedOnlyElectrons = cms.Sequence(uncleanedOnlyGsfElectronCores*uncleanedOnlyGsfElectrons)

#
# Whole Sequence
#

uncleanedOnlyElectronSequence = cms.Sequence(uncleanedOnlyClustering*uncleanedOnlyTracking*uncleanedOnlyConversions*uncleanedOnlyPfTracking*uncleanedOnlyElectrons)
