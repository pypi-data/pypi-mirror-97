from distutils.core import setup, Extension


x13_hash_module = Extension('deeponion-x13_hash',
                               sources = ['x13module.c',
                                          'x13.c',
					  'sha3/blake.c',
					  'sha3/bmw.c',
					  'sha3/groestl.c',
					  'sha3/jh.c',
					  'sha3/keccak.c',
					  'sha3/skein.c',
					  'sha3/cubehash.c',
					  'sha3/echo.c',
					  'sha3/luffa.c',
					  'sha3/simd.c',
                                          'sha3/hamsi.c',
                                          'sha3/hamsi_helper.c',
                                          'sha3/fugue.c',
					  'sha3/shavite.c'],

                               include_dirs=['.', './sha3'],
				headers=['/home/hempel/hash/deeponion-x13-hash-1.0/x13.h'])

setup (name = 'deeponion-x13-hash',
       version = '1.0.1',
       description = 'Bindings for proof of work used by x13',
       maintainer = 'thohemp',
       ext_modules = [x13_hash_module],
       url="https://github.com/thohemp/x13-hash")

