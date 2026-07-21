#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"

#include "DataFormats/L1TMuonPhase2/interface/MuonStub.h"
typedef SimpleFlatTableProducer<l1t::MuonStub> SimpleTriggerL1MuonStubFlatTableProducer;

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(SimpleTriggerL1MuonStubFlatTableProducer);
