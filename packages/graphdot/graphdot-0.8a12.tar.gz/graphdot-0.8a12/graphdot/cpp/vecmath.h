#ifndef GRAPHDOT_VECMATH_H_
#define GRAPHDOT_VECMATH_H_

#include <cuda_runtime.h>

namespace graphdot {

std::ostream & operator << (std::ostream &out, float2 v) {
    out << v.x << ' ' << v.y;
    return out;
}

#define VEC2_OPERATORS(T, S) \
inline __host__ __device__ T operator + (T const &u, T const &v) {\
    return make_##T(u.x + v.x, u.y + v.y);\
}\
inline __host__ __device__ T operator - (T const &u, T const &v) {\
    return make_##T(u.x - v.x, u.y - v.y);\
}\
inline __host__ __device__ T operator + (T const &u, S v) {\
    return make_##T(u.x + v, u.y + v);\
}\
inline __host__ __device__ T operator + (S v, T const &u) {\
    return make_##T(u.x + v, u.y + v);\
}\
inline __host__ __device__ T operator * (T const &u, S v) {\
    return make_##T(u.x * v, u.y * v);\
}\
inline __host__ __device__ T operator * (S v, T const &u) {\
    return make_##T(u.x * v, u.y * v);\
}\
inline __host__ __device__ T operator / (T const &u, S v) {\
    return make_##T(u.x / v, u.y / v, u.z / v);\
}\
inline __host__ __device__ T operator / (S v, T const &u) {\
    return make_##T(u.x / v, u.y / v, u.z / v);\
}\
inline __host__ __device__ auto dot(T const &u, T const &v) {\
    return u.x * v.x + u.y * v.y + u.z * v.z;\
}


VEC2_OPERATORS(int3, int)
VEC2_OPERATORS(float3, float)

inline bool operator <(int2 const &u, int2 const &v) {
    return u.x < v.x || (u.x == v.x && u.y < v.y);
}

}

#endif
