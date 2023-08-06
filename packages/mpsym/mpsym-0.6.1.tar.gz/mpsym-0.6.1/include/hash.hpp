#ifndef GUARD_HASH_H
#define GUARD_HASH_H

#include <iterator>

namespace mpsym
{

namespace util
{

template<typename IT>
std::size_t container_hash(IT first, IT last) {
  // see: https://stackoverflow.com/questions/20511347/a-good-hash-function-for-a-vector
  // boost container hash API is not stable across a sufficient range of versions
  std::size_t seed = std::distance(first, last);;
  for (auto it = first; it != last; ++it)
    seed ^= *it + 0x9e3779b9 + (seed << 6) + (seed >> 2);
  return seed;
}

template<typename T>
struct ContainerHash
{
  std::size_t operator()(T const &c) const
  { return util::container_hash(c.begin(), c.end()); }
};

} // namespace util

} // namespace mpsym

#endif // GUARD_HASH_H
