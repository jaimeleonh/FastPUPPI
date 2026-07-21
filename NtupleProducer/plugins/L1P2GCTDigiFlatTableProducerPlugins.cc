#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"

#include "DataFormats/L1TCalorimeterPhase2/interface/DigitizedClusterCorrelator.h"
typedef SimpleFlatTableProducer<l1tp2::DigitizedClusterCorrelator> L1P2GCTEmDigiClusterFlatTableProducer;

#include "DataFormats/L1TCalorimeterPhase2/interface/CaloPFCluster.h"
typedef SimpleFlatTableProducer<l1tp2::CaloPFCluster> L1P2GCTPFClusterFlatTableProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(L1P2GCTEmDigiClusterFlatTableProducer);
DEFINE_FWK_MODULE(L1P2GCTPFClusterFlatTableProducer);
