import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
from PhysicsTools.NanoAOD.common_cff import Var, ExtVar 

def LazyVar(expr, valtype, doc=None, precision=-1):
    return Var(expr, valtype, doc, precision, lazyEval=True)

process = cms.Process("L1Dump", eras.Phase2C17I13M9)

process.load('Configuration.StandardSequences.Services_cff')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(f'/store/cmst3/group/l1tr/FastPUPPI/15_1_X/fpinputs_151X/v1/TT_PU200/inputs151X_{i}.root' for i in range(1,11)),
)

process.load('Configuration.Geometry.GeometryExtendedRun4D110Reco_cff')
process.load('Configuration.Geometry.GeometryExtendedRun4D110_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff') # needed to read HCal TPs
process.load('SimCalorimetry.HGCalSimProducers.hgcalDigitizer_cfi') # needed for HGCAL_noise_fC
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '141X_mcRun4_realistic_v3', '')

process.l1tTrackSelectionProducer.processSimulatedTracks = False # these would need stubs, and are not used anyway

process.deps = cms.Task(
    process.l1tTkMuonsGmt,
    process.l1tSAMuonsGmt,
    process.l1tGTTInputProducer,
    process.l1tTrackSelectionProducer,
    process.l1tVertexFinderEmulator,
    process.l1tPhase2L1CaloEGammaEmulator,
    process.l1tPhase2CaloPFClusterEmulator,
    process.l1tPhase2GCTBarrelToCorrelatorLayer1Emulator,    
    process.L1TLayer1TaskInputsTask,
    process.L1TLayer1Task,
    process.l1tLayer2EG,
    process.L1TPFJetsEmulationTask,
    process.L1TPFJetsExtendedTask,
    process.L1TBJetsTask
)

process.muStubTable = cms.EDProducer("SimpleTriggerL1MuonStubFlatTableProducer",
    src = cms.InputTag("l1tStubsGmt", "tps"),
    cut = cms.string(""),
    name = cms.string("MuStub"),
    doc = cms.string("MuStub from GMT"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table
    variables = cms.PSet(
        etaRegion = Var("etaRegion",  int),
        phiRegion = Var("phiRegion",  int),
        depthRegion = Var("depthRegion",  int),
        tfLayer = Var("tfLayer",  int),
        phi = Var("coord1 * 3.1415926536/512",  float, doc="phi coordinate of the stub (at least for stubs in the barrel)"),
        eta = Var("eta1 * 3.1415926536/128",  float, doc="eta coordinate of the stub (at least for stubs in the barrel)"),
        coord1 = Var("coord1",  int),
        coord2 = Var("coord2",  int),
        eta1 = Var("eta1",  int),
        eta2 = Var("eta2",  int),
        isBarrel  = Var("isBarrel",  int),
        bx  = Var("bxNum",  int),
        time  = Var("time",  int),
        etaQuality  = Var("etaQuality",  int),
        quality  = Var("quality",  int),
    )
)
process.dtPhiStubTable = cms.EDProducer("L1P2DTPhStubFlatTableProducer",
    src = cms.InputTag("dtTriggerPhase2PrimitiveDigis"),
    cut = cms.string(""),
    name = cms.string("DTPhiStub"),
    doc = cms.string("DT Phi Stub"),
    extension = cms.bool(False), # this is the main table
    variables = cms.PSet(
         bx = Var("bxNum() - 20", int),
         wheel = Var("whNum()", int),
         sector = Var("scNum()", int),
         station = Var("stNum()", int),
         superlayer = Var("slNum()", int),
         hwPhiAngle = Var("phi()", int),
         hwPhiBending = Var("phiBend()", int),
         quality = Var("quality()", int),
         index = Var("index()", int),
         hwT0 = Var("t0()", int),
         t0 = Var("(t0() - 32*20)/32. * 25", float, "time in ns, centered on BX0"),
         chi2 = Var("chi2()", int),
         rpcFlag= Var("rpcFlag()", int),
    )
)
process.dtThetaStubTable = cms.EDProducer("L1P2DTThStubFlatTableProducer",
    src = cms.InputTag("dtTriggerPhase2PrimitiveDigis"),
    cut = cms.string(""),
    name = cms.string("DTThetaStub"),
    doc = cms.string("DT Theta Stub"),
    extension = cms.bool(False), # this is the main table
    variables = cms.PSet(
         bx = Var("bxNum() - 20", int),
         wheel = Var("whNum()", int),
         sector = Var("scNum()", int),
         station = Var("stNum()", int),
         hwZGlobal = Var("z()", int),
         hwKSlope = Var("k()", int),
         quality = Var("quality()", int),
         index = Var("index()", int),
         hwT0 = Var("t0()", int),
         t0 = Var("(t0() - 32*20)/32. * 25", float, "time in ns, centered on BX0"),
         chi2 = Var("chi2()", int),
         rpcFlag= Var("rpcFlag()", int),
    )
)


process.staMuTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tSAMuonsGmt","prompt"),
    cut = cms.string(""),
    name = cms.string("StaMu"),
    doc = cms.string("StaMuons from GMT (Prompt)"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table
    variables = cms.PSet(
        pt   = LazyVar("phPt",  float),
        eta  = LazyVar("phEta", float),
        phi  = LazyVar("phPhi", float),
        z0   = LazyVar("phZ0",  float, doc="Z coordinate of the reconstructed production vertex"),
        dxy   = LazyVar("phD0",  float, doc="transverse impact parameter (always zero currently)"),
        charge = LazyVar("phCharge", int, doc="charge"),
        quality = LazyVar("hwQual", int, doc="quality (TBD)"),
    )
)
process.staMuDisplTable = process.staMuTable.clone(
    src = cms.InputTag("l1tSAMuonsGmt","displaced"),
    name = cms.string("StaMuDisplaced"),
    doc = cms.string("StaMuons from GMT (displaced)"),
)

process.tkMuTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tTkMuonsGmt"),
    cut = cms.string(""),
    name = cms.string("TkMu"),
    doc = cms.string("TkMuons from GMT"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table
    variables = cms.PSet(
        pt   = LazyVar("phPt",  float),
        eta  = LazyVar("phEta", float),
        phi  = LazyVar("phPhi", float),
        mass = Var("0.10566", float),
        z0   = LazyVar("phZ0",  float, doc="Z coordinate of the reconstructed production vertex"),
        dxy   = LazyVar("phD0",  float, doc="transverse impact parameter (always zero currently)"),
        charge = LazyVar("phCharge", int, doc="charge"),
        quality = LazyVar("hwQual", int, doc="quality (TBD)"),
        hwPt   = LazyVar("hwPt", int),
        hwEta  = LazyVar("hwEta", int),
        hwPhi  = LazyVar("hwPhi", int),
        hwZ0  = LazyVar("hwZ0", int),
        hwD0  = LazyVar("hwD0", int),
        hwCharge  = LazyVar("hwCharge", int),
        hwIsoSum  = LazyVar("hwIsoSum", int),
        hwIsoSumAp  = LazyVar("hwIsoSumAp", int),
        hwQual  = LazyVar("hwQual", int),
    )
)

process.genMu = cms.EDFilter("GenParticleSelector",
    src = cms.InputTag("genParticles"),
    cut = cms.string("(abs(pdgId) = 13 || abs(pdgId) == 16975 || abs(pdgId) == 17) && status == 1 && pt > 0.5 && abs(eta) < 2.7"),
)


process.genMuTable = cms.EDProducer("SimpleGenParticleFlatTableProducer",
    src = cms.InputTag("genMu"),
    cut = cms.string(""),
    name = cms.string("Gen"),
    doc = cms.string("gen muons"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table
    variables = cms.PSet(
        pt  = Var("pt",  float),
        phi = Var("phi", float),
        eta  = Var("eta", float),
        mass  = Var("mass", float),
        beta  = Var("p/energy", float),
        z0   = Var("vz",  float, doc="Production point along the beam axis"),
        dxy   = Var("vertex.Rho",  float, doc="transverse distance of production point from the beam axis"),
        pdgId  = Var("pdgId", int, doc="PDG id"),
        charge  = Var("charge", int, doc="charge"),
        isPrompt  = Var("statusFlags().isPrompt()", int, doc="Prompt muon"),
        isFromTau  = Var("statusFlags().isDirectPromptTauDecayProduct()", int, doc="Muon from prompt tau decay"),
    )
)

process.p_mu = cms.Path(process.tkMuTable + process.muStubTable + process.staMuTable + process.staMuDisplTable + process.dtPhiStubTable + process.dtThetaStubTable)
process.p_muMC = cms.Path(process.genMu + process.genMuTable)
process.p_mu.associate(cms.Task(process.l1tStubsGmt, process.l1tTkMuonsGmt, process.l1tSAMuonsGmt))

process.puppiTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src = cms.InputTag("l1tLayer2Deregionizer:Puppi"),
        cut = cms.string(""),
        name = cms.string("Puppi"),
        doc = cms.string("L1Puppi candidates"),
        singleton = cms.bool(False), # the number of entries is variable
        extension = cms.bool(False), # this is the main table
        variables = cms.PSet(
            pt   = Var("pt",  float),
            phi  = Var("phi", float),
            eta  = Var("eta", float),
            mass = Var("mass", float),
            z0   = LazyVar("vz",  float),
            dxy  = LazyVar("dxy",  float),
            charge = Var("charge", int, doc="charge"),
            pdgId  = Var("pdgId", int, doc="PDG id"),
            puppiWeight = LazyVar("puppiWeight()", float, doc="PUPPI weight")
        )
    )

process.p_puppi = cms.Path(process.puppiTable)
process.p_puppi.associate(process.deps)

process.tracksTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tPFTracksFromL1Tracks"),
    cut = cms.string(""),
    name = cms.string("Tk"),
    doc = cms.string("L1 tracks"),
    singleton = cms.bool(False),
    extension = cms.bool(False),
    variables = cms.PSet(
        pt = Var("pt", float, precision=8),
        phi = Var("phi", float, precision=8),
        eta = Var("eta", float, precision=8),
        d0 = LazyVar("trackWord.getD0", float, precision=8),
        z0 = LazyVar("trackWord.getZ0", float, precision=8),
        maxAbsDxy = LazyVar("max(abs(track.POCA.x), abs(track.POCA.y))", float, precision=8),
        chi2rphi = LazyVar("trackWord.getChi2RPhi", float, precision=8),
        chi2rz = LazyVar("trackWord.getChi2RZ", float, precision=8),
        bendchi2 = LazyVar("trackWord.getBendChi2", float, precision=8),
        nStubs = LazyVar("trackWord.getNStubs", int, precision=8),
        mva = LazyVar("trackWord.getMVAQuality", float, precision=8),
    )
)

process.p_tracks = cms.Path(process.tracksTable)
process.p_tracks.associate(cms.Task(process.l1tPFTracksFromL1Tracks))

process.outnano = cms.OutputModule("NanoAODOutputModule",
    fileName = cms.untracked.string("l1Mu.root"),
    outputCommands = cms.untracked.vstring("drop *", "keep nanoaodFlatTable_*Table_*_*"),
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string("ZLIB"),
)
process.end = cms.EndPath(process.outnano)

schedule = [p for (k,p) in process.paths_().items() if k.startswith("p_") ]
schedule += [process.end]
process.schedule = cms.Schedule(schedule)

def noNano():
    process.schedule = cms.Schedule(process.p_dumps)

process.source.fileNames  = [ 
    f'/store/cmst3/group/l1tr/FastPUPPI/15_1_X/fpinputs_151X/v1/DYToLL_M50_PU200/inputs151X_{i}.root' for i in range(2,3)
]
process.source.fileNames  = [ 
    '/store/cmst3/group/l1tr/FastPUPPI/15_1_X/fpinputs_151X/v1/HSCPtauPrime_4000_PU0/inputs151x-HSCPtauPrime_4000_PU0-2-0.fp151x.root'
]
process.source.duplicateCheckMode = cms.untracked.string("noDuplicateCheck")