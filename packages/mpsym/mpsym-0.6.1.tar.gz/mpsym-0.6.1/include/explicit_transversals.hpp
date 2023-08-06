#ifndef GUARD_EXPLICIT_TRANSVERSALS_H
#define GUARD_EXPLICIT_TRANSVERSALS_H

#include <map>
#include <ostream>
#include <vector>

#include "perm.hpp"
#include "perm_set.hpp"
#include "schreier_structure.hpp"

namespace mpsym
{

namespace internal
{

struct ExplicitTransversals : public SchreierStructure
{
  ExplicitTransversals(unsigned degree, unsigned root, PermSet const &labels)
  : _degree(degree),
    _root(root),
    _labels(labels)
  { _orbit[root] = Perm(_degree); }

  virtual ~ExplicitTransversals() = default;

  void add_label(Perm const &label) override
  { _labels.insert(label); }

  void create_edge(unsigned origin,
                   unsigned destination,
                   unsigned label) override;

  unsigned root() const override;
  std::vector<unsigned> nodes() const override;
  PermSet labels() const override;

  bool contains(unsigned node) const override;
  bool incoming(unsigned node, Perm const &edge) const override;
  Perm transversal(unsigned origin) const override;

private:
  void dump(std::ostream &os) const override;

  unsigned _degree;
  unsigned _root;
  PermSet _labels;
  std::map<unsigned, Perm> _orbit;
};

} // namespace internal

} // namespace mpsym

#endif // GUARD_EXPLICIT_TRANSVERSALS_H
