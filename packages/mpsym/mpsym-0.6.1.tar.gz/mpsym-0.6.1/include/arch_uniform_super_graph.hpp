#ifndef GUARD_ARCH_UNIFORM_SUPER_GRAPH_H
#define GUARD_ARCH_UNIFORM_SUPER_GRAPH_H

#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

#include "arch_graph_automorphisms.hpp"
#include "arch_graph_system.hpp"
#include "bsgs.hpp"
#include "perm_group.hpp"
#include "perm_set.hpp"

namespace mpsym
{

class TaskMapping;
class TMORs;

class ArchUniformSuperGraph : public ArchGraphSystem
{
public:
  virtual ~ArchUniformSuperGraph() = default;

  ArchUniformSuperGraph(std::shared_ptr<ArchGraphSystem> super_graph,
                        std::shared_ptr<ArchGraphSystem> proto);

  std::string to_gap() const override;
  std::string to_json() const override;

  std::shared_ptr<ArchGraphSystem> super_graph() const
  { return _subsystem_super_graph; }

  std::shared_ptr<ArchGraphSystem> proto() const
  { return _subsystem_proto; }

  unsigned num_processors() const override;
  unsigned num_channels() const override;

  internal::PermSet automorphisms_generators(
    AutomorphismOptions const *options = nullptr,
    internal::timeout::flag aborted = internal::timeout::unset()) override
  {
    return internal::PermGroup::wreath_product_generators(
      _subsystem_proto->automorphisms_generators(options, aborted),
      _subsystem_super_graph->automorphisms_generators(options, aborted));
  }

private:
  internal::BSGS::order_type num_automorphisms_(
    AutomorphismOptions const *options,
    internal::timeout::flag aborted) override
  {
    return internal::PermGroup::wreath_product_order(
      _subsystem_proto->automorphisms(options, aborted),
      _subsystem_super_graph->automorphisms(options, aborted));
  }

  internal::PermGroup automorphisms_(
    AutomorphismOptions const *options,
    internal::timeout::flag aborted) override;

  void init_repr_(AutomorphismOptions const *options,
                  internal::timeout::flag aborted) override;

  bool repr_ready_() const override;

  void reset_repr_() override;

  TaskMapping repr_(TaskMapping const &mapping_,
                    ReprOptions const *options,
                    TMORs *orbits,
                    internal::timeout::flag aborted) override;

  std::shared_ptr<internal::ArchGraphAutomorphisms>
  wreath_product_action_super_graph(AutomorphismOptions const *options,
                                    internal::timeout::flag aborted) const;

  std::vector<std::shared_ptr<internal::ArchGraphAutomorphisms>>
  wreath_product_action_proto(AutomorphismOptions const *options,
                              internal::timeout::flag aborted) const;

  std::shared_ptr<ArchGraphSystem> _subsystem_super_graph;
  std::shared_ptr<ArchGraphSystem> _subsystem_proto;

  bool _super_graph_trivial = false;
  bool _proto_trivial = false;

  std::shared_ptr<internal::ArchGraphAutomorphisms> _sigma_total;
  std::shared_ptr<internal::ArchGraphAutomorphisms> _sigma_super_graph;
  std::vector<std::shared_ptr<internal::ArchGraphAutomorphisms>> _sigmas_proto;
  bool _sigmas_valid = false;
};

} // namespace mpsym

#endif // GUARD_ARCH_GRAPH_H
