#include <algorithm>
#include <cassert>
#include <chrono>
#include <iterator>
#include <memory>
#include <numeric>
#include <ostream>
#include <sstream>
#include <stdexcept>
#include <utility>
#include <vector>

#include "bsgs.hpp"
#include "dbg.hpp"
#include "dump.hpp"
#include "orbit.hpp"
#include "perm.hpp"
#include "perm_set.hpp"
#include "pr_randomizer.hpp"
#include "explicit_transversals.hpp"
#include "schreier_structure.hpp"
#include "schreier_tree.hpp"

namespace mpsym
{

namespace internal
{

void BSGSTransversalsBase::reserve_schreier_structure(
  unsigned i, unsigned root, unsigned degree)
{
  if (i < _schreier_structures.size())
    return;

  assert(i == _schreier_structures.size());

  _schreier_structures.push_back(make_schreier_structure(root, degree, {}));
}

void BSGSTransversalsBase::update_schreier_structure(
  unsigned i, unsigned root, unsigned degree, PermSet const &generators)
{
  auto ss(make_schreier_structure(root, degree, generators));

  Orbit::generate(root, generators, ss);

  if (i < _schreier_structures.size())
    _schreier_structures[i].swap(ss);

  assert(i == _schreier_structures.size());

  _schreier_structures.push_back(ss);
}

void BSGSTransversalsBase::insert_schreier_structure(
  unsigned i, unsigned root, unsigned degree, PermSet const &generators)
{
  _schreier_structures.insert(_schreier_structures.begin() + i, nullptr);

  update_schreier_structure(i, root, degree, generators);
}

BSGS::BSGS(unsigned degree)
: _degree(degree)
{ assert(degree > 0); }

BSGS::BSGS(unsigned degree,
           PermSet const &generators,
           BSGSOptions const *options_,
           timeout::flag aborted)
: _degree(degree)
{
  assert(degree > 0);

  if (generators.trivial())
    return;

  generators.assert_degree(degree);

  auto options(BSGSOptions::fill_defaults(options_));

  transversals_init(&options);

  DBG(DEBUG) << "Constructing BSGS";
  DBG(DEBUG) << "Generators: " << generators;

  bool construct_sym = false;

  if (options.check_sym && degree > 8u) {
    PermSet generators_minimized(generators);
    generators_minimized.minimize_degree();

    if (generators_minimized.degree() > 8u) {
      PrRandomizer pr(generators_minimized);

      if (pr.test_symmetric())
        construct_sym = true;
    }
  }

  if (construct_sym)
    construct_symmetric(generators.support());
  else
    construct_unknown(generators, &options, aborted);

  DBG(DEBUG) << "=> B = " << _base;
  DBG(DEBUG) << "=> SGS = " << _strong_generators;

  assert(base_size() > 0u);
}

BSGS::BSGS(unsigned degree,
           Base const &base,
           PermSet const &strong_generators,
           BSGSOptions const *options_)
: _degree(degree),
  _base(base),
  _strong_generators(strong_generators)
{
  assert(degree > 0);

  strong_generators.assert_degree(degree);

  auto options(BSGSOptions::fill_defaults(options_));

  transversals_init(&options);

  auto sgs(strong_generators);
  for (unsigned i = 0; i < base_size(); ++i) {
    update_schreier_structure(i, sgs);

    for (auto it = sgs.begin(); it != sgs.end();) {
      if (!it->stabilizes(base_point(i))) {
        it = sgs.erase(it);
      } else {
        ++it;
      }
    }
  }

  assert(sgs.empty());
}

BSGS::order_type BSGS::order() const
{
  order_type res = 1;

  for (unsigned i = 0u; i < base_size(); ++i)
    res *= orbit(i).size();

  return res;
}

PermSet BSGS::strong_generators(unsigned i) const
{
  PermSet ret;
  for (Perm const &sg : strong_generators()) {
    if (sg.stabilizes(_base.begin(), _base.begin() + i))
      ret.insert(sg);
  }

  return ret;
}

Orbit BSGS::orbit(unsigned i) const
{
  auto nodes(schreier_structure(i)->nodes());

  return Orbit(nodes.begin(), nodes.end());
}

Perm BSGS::transversal(unsigned i, unsigned o) const
{ return schreier_structure(i)->transversal(o); }

PermSet BSGS::transversals(unsigned i) const
{
  PermSet transversals;
  for (unsigned o : orbit(i))
    transversals.insert(schreier_structure(i)->transversal(o));

  return transversals;
}

PermSet BSGS::stabilizers(unsigned i) const
{ return schreier_structure(i)->labels(); }

std::pair<Perm, unsigned> BSGS::strip(Perm const &perm, unsigned offs) const
{
  Perm result(perm);

  for (unsigned i = offs; i < base_size(); ++i) {
    unsigned beta = result[base_point(i)];
    if (!schreier_structure(i)->contains(beta))
      return std::make_pair(result, i + 1u);

    result *= ~schreier_structure(i)->transversal(beta);
  }

  return std::make_pair(result, base_size() + 1u);
}

bool BSGS::strips_completely(Perm const &perm) const
{
  auto strip_result(strip(perm));

  return strip_result.first.id() && strip_result.second == base_size() + 1u;
}

void BSGS::extend_base(unsigned bp)
{ _base.push_back(bp); }

void BSGS::extend_base(unsigned bp, unsigned i)
{ _base.insert(_base.begin() + i, bp); }

void BSGS::transversals_init(BSGSOptions const *options)
{
  switch (options->transversals) {
    case BSGSOptions::Transversals::EXPLICIT:
      _transversals = std::make_shared<BSGSTransversals<ExplicitTransversals>>();
      break;
    case BSGSOptions::Transversals::SCHREIER_TREES:
      _transversals = std::make_shared<BSGSTransversals<SchreierTree>>();
      break;
    case BSGSOptions::Transversals::SHALLOW_SCHREIER_TREES:
      throw std::logic_error("TODO");
  }
}

void BSGS::construct_symmetric(std::vector<unsigned> const &support)
{
  DBG(DEBUG) << "Group is symmetric";

  if (_degree == 1u)
    return;

  _base = std::vector<unsigned>(support.begin(), std::prev(support.end()));

  for (auto it(_base.rbegin()); it != _base.rend(); ++it)
    _strong_generators.insert(Perm(_degree, {{*it, support.back()}}));

  _strong_generators.make_unique();

  for (unsigned i = 0u; i < _base.size(); ++i) {
    PermSet tmp(_strong_generators.subset(0, support.size() - i - 1u));
    tmp.insert_inverses();

    update_schreier_structure(i, tmp);
  }

  _is_symmetric = true;
}

void BSGS::construct_unknown(PermSet const &generators,
                             BSGSOptions const *options,
                             timeout::flag aborted)
{
  switch (options->construction) {
    case BSGSOptions::Construction::AUTO:
      if (options->schreier_sims_random_use_known_order &&
          options->schreier_sims_random_known_order > 0) {
        schreier_sims_random(generators, options, aborted);
      } else {
        schreier_sims(generators, options, aborted);
      }
      break;
    case BSGSOptions::Construction::SCHREIER_SIMS:
      schreier_sims(generators, options, aborted);
      break;
    case BSGSOptions::Construction::SCHREIER_SIMS_RANDOM:
      schreier_sims_random(generators, options, aborted);
      break;
    case BSGSOptions::Construction::SOLVE:
      solve(generators);
      break;
  }

  if (options->reduce_gens)
    reduce_gens();
}

std::ostream &operator<<(std::ostream &os, BSGS const &bsgs)
{
  os << "BASE: " << DUMP(bsgs._base) << "\n"
     << "SGS: " << DUMP(bsgs._strong_generators);

  return os;
}

} // namespace internal

} // namespace mpsym
