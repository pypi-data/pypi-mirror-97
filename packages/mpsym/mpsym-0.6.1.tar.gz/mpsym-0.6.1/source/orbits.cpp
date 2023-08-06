#include <algorithm>
#include <cassert>
#include <memory>
#include <unordered_set>
#include <vector>

#include "orbit.hpp"
#include "perm.hpp"
#include "perm_set.hpp"
#include "schreier_structure.hpp"

namespace mpsym
{

namespace internal
{

Orbit Orbit::generate(unsigned x,
                      PermSet const &generators,
                      std::shared_ptr<SchreierStructure> ss)
{
  Orbit orbit{x};

  if (generators.trivial())
    return orbit;

  assert(x < generators.degree());

  generators.assert_inverses();

  orbit.extend(generators, {x}, {x}, ss);

  return orbit;
}

bool Orbit::operator==(Orbit const &other) const
{
  if (size() != other.size())
    return false;

  std::set<unsigned> this_set(begin(), end());
  std::set<unsigned> other_set(begin(), end());

  return this_set == other_set;
}

bool Orbit::generated_by(unsigned x, PermSet const &generators) const
{
  if (generators.trivial())
    return size() == 1u && _elements[0] == x;

  assert(x < generators.degree());

  // this orbit
  std::unordered_set<unsigned> this_orbit;
  this_orbit.insert(begin(), end());

  if (this_orbit.find(x) == this_orbit.end())
    return false;

  // orbit of x
  std::unordered_set<unsigned> x_orbit{x};

  // enumerate orbit of x
  auto generators_with_inverses(generators.with_inverses());

  std::vector<unsigned> stack{x};

  while (!stack.empty()) {
    unsigned y = stack.back();
    stack.pop_back();

    for (Perm const &gen : generators_with_inverses) {
      unsigned y_prime = gen[y];

      // check if the orbit of x contains an element not in this orbit
      if (this_orbit.find(y_prime) == this_orbit.end())
        return false;

      if (x_orbit.find(y_prime) == x_orbit.end()) {
        x_orbit.insert(y_prime);

        // check if this orbit is a subset of the orbit of x
        if (x_orbit.size() > this_orbit.size())
          return false;

        stack.push_back(y_prime);
      }
    }
  }

  // check if the orbit of x is a subset of this orbit
  if (x_orbit.size() < this_orbit.size())
    return false;

  // the orbits match
  return true;
}

void Orbit::update(PermSet const &generators_old,
                   PermSet const &generators_new,
                   std::shared_ptr<SchreierStructure> ss)
{
  if (generators_new.trivial())
    return;

#ifndef NDEBUG
  if (!generators_old.trivial())
    assert(generators_new.degree() == generators_old.degree());
#endif

  generators_old.assert_inverses();
  generators_new.assert_inverses();

  auto generators(generators_old);
  generators.insert(generators_new.begin(), generators_new.end());

  if (ss) {
    for (Perm const &gen_new : generators_new)
      ss->add_label(gen_new);
  }

  std::vector<unsigned> stack;
  std::unordered_set<unsigned> done(begin(), end());

  for (unsigned i = 0u; i < generators_new.size(); ++i) {
    for (unsigned x : *this) {
      unsigned y = generators_new[i][x];

      if (done.find(y) == done.end()) {
        done.insert(y);
        stack.push_back(y);

        if (ss)
          ss->create_edge(y, x, generators_old.size() + i);
      }
    }
  }

  _elements.insert(end(), stack.begin(), stack.end());

  extend(generators, stack, done, ss);
}

void Orbit::extend(PermSet const &generators,
                   std::vector<unsigned> stack,
                   std::unordered_set<unsigned> done,
                   std::shared_ptr<SchreierStructure> ss)
{
  while (!stack.empty()) {
    unsigned x = stack.back();
    stack.pop_back();

    assert(x < generators.degree());

    for (auto i = 0u; i < generators.size(); ++i) {
      unsigned y = generators[i][x];

      if (done.find(y) == done.end()) {
        done.insert(y);
        stack.push_back(y);

        _elements.push_back(y);

        if (ss)
          ss->create_edge(y, x, i);
      }
    }
  }
}

OrbitPartition::OrbitPartition(unsigned degree)
: _partition_indices(degree, -1)
{}

OrbitPartition::OrbitPartition(unsigned degree,
                               std::vector<Orbit> const &partitions)
: _partitions(partitions),
  _partition_indices(degree, -1)
{
#ifndef NDEBUG
  for (auto const &part : partitions) {
    for (unsigned x : part)
      assert(x < degree);
  }
#endif

  update_partition_indices();
}

OrbitPartition::OrbitPartition(unsigned degree,
                               std::vector<int> const &partition_indices)
: _partition_indices(partition_indices)
{
#ifndef NDEBUG
  assert(partition_indices.size() == degree);
#else
  (void)degree;
#endif

  update_partitions();
}

OrbitPartition::OrbitPartition(unsigned degree, PermSet const &generators)
: _partition_indices(degree, -1)
{
  if (generators.trivial())
    return;

  assert(generators.degree() == degree);

  std::vector<int> processed(generators.degree(), 0);
  unsigned num_processed = 0u;

  unsigned x = 0u;

  for (;;) {
    auto orbit(Orbit::generate(x, generators.with_inverses()));

    _partitions.push_back(orbit);

    if ((num_processed += orbit.size()) == generators.degree())
      break;

    for (unsigned y : orbit)
      processed[y] = 1;

    while (processed[x])
      ++x;
  }

  update_partition_indices();
}

std::vector<OrbitPartition> OrbitPartition::split(
  OrbitPartition const &split) const
{
  assert(split._partition_indices.size() == _partition_indices.size());

  std::vector<int> new_partition_indices(_partition_indices.size(), -1);
  std::vector<int> current_partitions_indices(split.num_partitions(), 0);

  std::vector<std::vector<int>> split_partition_indices(split.num_partitions());
  for (auto &partition_indices : split_partition_indices)
    partition_indices.resize(_partition_indices.size());

  for (unsigned x = 0u; x < _partition_indices.size(); ++x) {
    int i = split.partition_index(x);
    int j = partition_index(x);

    if (new_partition_indices[j] == -1)
      new_partition_indices[j] = current_partitions_indices[i]++;

    split_partition_indices[i][x] = new_partition_indices[j];
  }

  std::vector<OrbitPartition> res;
  for (auto const &partition_indices : split_partition_indices)
    res.emplace_back(partition_indices.size(), partition_indices);

  return res;
}

void OrbitPartition::remove_from_partition(unsigned x)
{
  assert(x < _partition_indices.size());

  int i = _partition_indices[x];

  if (i == -1)
    return;

  _partitions[i].erase(
    std::find(_partitions[i].begin(), _partitions[i].end(), x));

  _partition_indices[x] = -1;
}

void OrbitPartition::change_partition(unsigned x, int i)
{
  assert(x < _partition_indices.size());

  if (i < 0) {
    remove_from_partition(x);
    return;
  }

  _partition_indices[x] = i;

  for (auto p_it = _partitions.begin(); p_it != _partitions.end(); ++p_it) {
    auto e_it = std::find(p_it->begin(), p_it->end(), x);

    if (e_it != p_it->end()) {
      p_it->erase(e_it);

      if (p_it->empty())
        _partitions.erase(p_it);

      break;
    }
  }

  add_to_partition(x, i);
}

void OrbitPartition::add_to_partition(unsigned x, int i)
{
  if (i >= static_cast<int>(_partitions.size()) - 1)
    _partitions.resize(i + 1);

  _partitions[i].insert(x);
}

void OrbitPartition::update_partitions()
{
  for (unsigned x = 0u; x < _partition_indices.size(); ++x) {
    int i = partition_index(x);

    if (i == -1)
      continue;

    add_to_partition(x, i);
  }
}

void OrbitPartition::update_partition_indices()
{
  for (int i = 0; i < static_cast<int>(_partitions.size()); ++i) {
    for (unsigned x : _partitions[i])
      _partition_indices[x] = i;
  }
}

} // namespace internal

} // namespace mpsym
