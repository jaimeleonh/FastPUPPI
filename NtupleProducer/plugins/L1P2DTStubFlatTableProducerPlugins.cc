#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"

#include "DataFormats/L1TMuonPhase2/interface/MuonStub.h"
#include "L1Trigger/L1TMuon/interface/GeometryTranslator.h"
#include "DataFormats/L1DTTrackFinder/interface/L1Phase2MuDTPhContainer.h"
#include "DataFormats/L1DTTrackFinder/interface/L1Phase2MuDTThContainer.h"
#include <ap_int.h>
#include <ap_fixed.h>

template <typename T>
class L1P2DTStubFlatTableProducer : public SimpleFlatTableProducerBase<typename T::Segment_Container::value_type, T> {
public:
  typedef typename T::Segment_Container ContainerType;
  typedef typename T::Segment_Container::value_type StubType;

  L1P2DTStubFlatTableProducer(edm::ParameterSet const &params)
      : SimpleFlatTableProducerBase<StubType, T>(params),
        maxLen_(params.existsAs<unsigned int>("maxLen") ? params.getParameter<unsigned int>("maxLen")
                                                        : std::numeric_limits<unsigned int>::max()),
        cut_(params.getParameter<std::string>("cut"), params.getUntrackedParameter<bool>("lazyEval")) /*,
        translator_(std::make_unique<L1TMuon::GeometryTranslator>(this->consumesCollector()))*/
  {}

  ~L1P2DTStubFlatTableProducer() override {}

  static edm::ParameterSetDescription baseDescriptions() {
    edm::ParameterSetDescription desc = SimpleFlatTableProducerBase<StubType, T>::baseDescriptions();

    desc.add<std::string>("cut", "")->setComment("selection on the main input collection");
    desc.addUntracked<bool>("lazyEval", false)
        ->setComment("if true, can use methods of inheriting classes. Can cause problems when multi-threading.");
    desc.addOptional<unsigned int>("maxLen")->setComment(
        "define the maximum length of the input collection to put in the branch");
    return desc;
  }

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
    edm::ParameterSetDescription desc = SimpleFlatTableProducer<StubType>::baseDescriptions();
    descriptions.addWithDefaultLabel(desc);
  }

  std::unique_ptr<nanoaod::FlatTable> fillTable(const edm::Event &iEvent, const edm::Handle<T> &prod) const override {
    const ContainerType &selContainer = *prod->getContainer();
    std::vector<const StubType *> selobjs;
    if (prod.isValid() || !(this->skipNonExistingSrc_)) {
      for (unsigned int i = 0, n = selContainer.size(); i < n; ++i) {
        const auto &obj = selContainer[i];
        if (cut_(obj)) {
          selobjs.push_back(&obj);
        }
        if (selobjs.size() >= maxLen_)
          break;
      }
    }
    auto out = std::make_unique<nanoaod::FlatTable>(selobjs.size(), this->name_, /*singleton=*/false, this->extension_);
    for (const auto &var : this->vars_)
      var->fill(selobjs, *out);

    std::vector<float> eta, phi, rho, z;
    if constexpr (std::is_same_v<StubType, L1Phase2MuDTPhDigi>) {
      //const L1Phase2MuDTPh
      //out->setDoc("L1 Phase 2 DT phi trigger primitives");
      for (const auto *ptr : selobjs) {
        const L1Phase2MuDTPhDigi &phiS = *ptr;
        // use kBMTF logic to get the phi
        ap_uint<18> normalization0 = phiS.scNum() * ap_uint<15>(21845);
        ap_int<18> normalization1 = ap_int<18>(ap_int<17>(phiS.phi()) * ap_ufixed<8, 0>(0.3183));
        ap_int<18> kmtf_phi = ap_int<18>(normalization0 + normalization1);
        phi.push_back(kmtf_phi.to_int() * M_PI / (1 << 17));
      }
      out->template addColumn<float>("phi", phi, "phi in global coordinates");
    }
    /*} else if constexpr (std::is_same_v<T, L1Phase2MuDTThContainer>) {
      //out->setDoc("L1 Phase 2 DT theta trigger primitives");
    */
    return out;
  }

protected:
  const unsigned int maxLen_;
  const StringCutObjectSelector<StubType> cut_;
  //std::unique_ptr<L1TMuon::GeometryTranslator> translator_;
};

typedef L1P2DTStubFlatTableProducer<L1Phase2MuDTPhContainer> L1P2DTPhStubFlatTableProducer;
typedef L1P2DTStubFlatTableProducer<L1Phase2MuDTThContainer> L1P2DTThStubFlatTableProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(L1P2DTPhStubFlatTableProducer);
DEFINE_FWK_MODULE(L1P2DTThStubFlatTableProducer);
