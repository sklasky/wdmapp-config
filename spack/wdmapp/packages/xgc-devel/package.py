# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XgcDevel(CMakePackage):
    """XGC-Devel used for coupling with GENE-CUTH via the coupler"""

    homepage = "https://hbps.pppl.gov/computing/xgc-1"
    # FIXME, there is no tarball, but it still needs a URL, so it's fake
    url = "https://github.com/wdmapp/xgc1.tar.gz"
    git = "git@github.com:wdmapp/XGC-Devel.git"

    maintainers = ['germasch', 'bd4', 'cwsmith', 'Damilare06']

    version('wdmapp', branch='wdmapp', preferred=True)
    version('rpi', branch='rpi')

    variant('adios2', default=True,
            description="use ADIOS2 for I/O")
    variant('coupling_core_edge_gene', default=False,
            description='Enable XGC/GENE coupling')
    variant('cabana', default=True,
            description='Enable Kokkos/Cabana kernels')
    variant('effis', default=False,
            description='Enable EFFIS')

    _xgc_options = {'coupling_core_edge': False,
                    'init_gene_pert': False,
                    'use_old_read_input': False,
                    'convert_grid2': False,
                    'new_flx_aif': False,
                    'deltaf_mode2': False,
                    'pure_rk4': False,
                    'v_perp': True,
                    'use_bicub_mod': True,
                    'use_one_d_i_cub_mod': True}

    for opt, default in _xgc_options.items():
        variant(opt, default=default, description="Enable " + opt.upper())

    depends_on('petsc@3.7.0:3.7.999 ~complex +double')
    depends_on('pkgconfig')
    depends_on('adios +fortran')
    depends_on('adios2 +fortran', when='+adios2')
    depends_on('adios2 +fortran', when='+coupling_core_edge_gene')
    depends_on('fftw@3.3.8:')
    depends_on('cabana@develop', when='+cabana')
    depends_on('pspline')
    depends_on('camtimers')
    depends_on('effis', when='+effis')

    def cmake_args(self):
        spec = self.spec
        args = []
        args += ['-DBUILD_TESTING=OFF']
        args += ['-DXGC_USE_ADIOS1=ON']
        args += ['-DXGC_USE_ADIOS2={}'.format(
            'ON' if '+adios2' in spec else 'OFF')]
        args += ['-DXGC_USE_CABANA={}'.format(
            'ON' if '+cabana' in spec else 'OFF')]
        if '+cabana' in spec:
            args += ['-DCMAKE_CXX_COMPILER=%s' % spec['kokkos'].kokkos_cxx]
        args += ['-DXGC_GENE_COUPLING={}'.format(
            'ON' if '+coupling_core_edge_gene' in spec else 'OFF')]
        args += ['-DUSE_SYSTEM_PSPLINE=ON']
        args += ['-DUSE_SYSTEM_CAMTIMERS=ON']
        args += ['-DEFFIS={}'.format('ON' if '+effis' in spec else 'OFF')]

        for opt in self._xgc_options:
            args += ['-DXGC_{}={}'.format(opt.upper(),
                                          'ON' if '+'+opt in spec else 'OFF')]
        return args
