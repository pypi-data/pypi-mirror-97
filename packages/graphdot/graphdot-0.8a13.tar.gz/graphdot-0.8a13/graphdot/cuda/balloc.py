#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import ctypes
from pycuda.driver import managed_empty
from pycuda.driver import mem_attach_flags as ma_flags


def unified_memory(size, dtype):
    return managed_empty(size, dtype, 'C', ma_flags.GLOBAL)


def pad(n, align):
    return ((n + align - 1) // align) * align


class ArrayView(np.ndarray):
    @property
    def ptr(self):
        return ctypes.addressof(ctypes.c_char.from_buffer(self.base))


class BeltAllocator:

    def __init__(self, dtype, slab_size=16777216, allocator=unified_memory):
        self.dtype = dtype
        self.slab_size = slab_size
        self.allocator = allocator
        self.current = None
        self.held = []

        self._allocate_slab()

    def __call__(self, size, alignment=8):
        if size > self.slab_size // 8:
            # no need of belt allocator for large allocations
            # return self.allocator(size, self.dtype)
            raise ValueError('Size %d too large for belt allocator' % size)
        else:
            self.head = pad(self.head, alignment)
            if self.head + size > self.slab_size:
                self.held.append(self.current)
                self._allocate_slab()
                self.head = 0

            alloc = np.frombuffer(self.current[self.head:self.head + size],
                                  dtype=self.dtype).view(ArrayView)
            self.head += size
            return alloc

    def allocate(self, size, alignment=8):
        if size > self.slab_size // 8:
            # no need of belt allocator for large allocations
            # return self.allocator(size, self.dtype)
            raise ValueError('Size %d too large for belt allocator' % size)
        else:
            self.head = pad(self.head, alignment)
            if self.head + size > self.slab_size:
                self._allocate_slab()

            alloc = self.current[self.head:self.head + size]
            self.head += size
            return alloc

    def dummy(self, size, alignment=8):
        return None

    def _allocate_slab(self):
        print('Allocating slab')
        if self.current:
            self.held.append(self.current)
        buffer = self.allocator(self.slab_size, self.dtype)
        buffer[:] = 0
        self.current = memoryview(buffer)
        self.head = 0


# if __name__ == '__main__':

#     import pycuda.autoinit

#     alloc = BeltAllocator(np.float32)

#     A = alloc(9)
#     B = alloc(1)
#     A[0] = 42
#     B[0] = 88
#     print(type(A))
#     print(A.base)
#     print(A.ptr)
#     print(B.ptr)
#     print(alloc.current[0])
#     print(np.frombuffer(alloc.current[0:32], np.float32))
