#ifndef GUARD_SCHREIER_GENERATOR_QUEUE_H
#define GUARD_SCHREIER_GENERATOR_QUEUE_H

#include <cassert>
#include <memory>
#include <vector>

#include "perm.hpp"
#include "schreier_structure.hpp"
#include "util.hpp"

namespace mpsym
{

namespace internal
{

class SchreierGeneratorQueue
{
  using sg_type = PermSet;
  using sg_it_type = sg_type::const_iterator;

  using fo_type = Orbit;
  using fo_it_type = fo_type::const_iterator;

public:
  using value_type = Perm;
  using const_reference = Perm const &;

  class const_iterator : public util::Iterator<const_iterator, Perm const>
  {
  public:
    const_iterator()
    : _queue(nullptr),
      _end(true)
    {}

    const_iterator(SchreierGeneratorQueue *queue)
    : _queue(queue),
      _end(false)
    {
      _queue->advance();
      _queue->mark_used();
    }

    bool operator==(const_iterator const &rhs) const override
    { return end() && rhs.end(); }

  private:
    reference current() override
    { return _queue->_schreier_generator; }

    void next() override
    { _queue->advance(); }

    bool end() const
    { return _end || _queue->_exhausted; }

    SchreierGeneratorQueue *_queue;
    bool _end;
  };

  SchreierGeneratorQueue()
  : _valid(false)
  {}

  void update(sg_type const &strong_generators,
              fo_type const &fundamental_orbit,
              std::shared_ptr<SchreierStructure> schreier_structure)
  {
    if (_valid)
      return;

    _sg_it = strong_generators.begin();
    _sg_begin = _sg_it;
    _sg_end = strong_generators.end();

    _beta_it = fundamental_orbit.begin();
    _beta_end = fundamental_orbit.end();

    _schreier_structure = schreier_structure;

    _u_beta = u_beta();

    _valid = true;
    _used = false;
    _exhausted = _sg_it == _sg_end;
  }

  void invalidate() { _valid = false; }

  const_iterator begin() { return const_iterator(this); }
  const_iterator end() { return const_iterator(); }

private:
  Perm u_beta()
  { return _schreier_structure->transversal(*_beta_it); }

  Perm u_beta_x()
  { return _schreier_structure->transversal((*_sg_it)[*_beta_it]); }

  void next_sg()
  {
    if (++_sg_it == _sg_end)
      next_beta();
  }

  void next_beta()
  {
    if (++_beta_it == _beta_end) {
      _exhausted = true;
    } else {
      _sg_it = _sg_begin;
      _u_beta = u_beta();
    }
  }

  void advance()
  {
    if (_used)
      next_sg();

    while (!_exhausted && _schreier_structure->incoming(*_beta_it, *_sg_it))
      next_sg();

    if (_exhausted)
      return;

    _schreier_generator = _u_beta * (*_sg_it) * ~u_beta_x();
  }

  void mark_used() { _used = true; }

  sg_it_type _sg_it;
  sg_it_type _sg_begin;
  sg_it_type _sg_end;

  fo_it_type _beta_it;
  fo_it_type _beta_end;

  std::shared_ptr<SchreierStructure> _schreier_structure;

  bool _valid;
  bool _used;
  bool _exhausted;

  Perm _u_beta;
  Perm _schreier_generator;
};

} // namespace internal

} // namespace mpsym

#endif // GUARD_SCHREIER_GENERATOR_QUEUE_H
