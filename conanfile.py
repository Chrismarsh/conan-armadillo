# from conans.errors import ConanException
import os
import shutil

from conans import CMake, ConanFile, tools


class ArmadilloConan(ConanFile):
    name = "armadillo"
    version = "9.800.2"
    license = "Apache License 2.0"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-armadillo"
    description = "C++ library for linear algebra & scientific computing"
    settings = "os", "build_type"
    options = {
        # If true the recipe will use blas and lapack from system
        "use_system_blas": [True, False],
        # "link_with_mkl": [True, False],
        "with_lapack":[True,False],
        "with_blas":[True,False],
        "use_wrapper":[True,False],
        "build_shared":[True,False]}
    default_options = ("use_system_blas=True",
                       # "link_with_mkl=False",
                       # "use_extern_cxx11_rng=False",
                       "with_lapack=True",
                       "with_blas=True",
                       "use_wrapper=True",
                       "build_shared=False")
    generators = "cmake"

    source_folder_name = "armadillo-{0}".format(version)
    source_tar_file = "{0}.tar.xz".format(source_folder_name)

    def requirements(self):
        if not self.options.use_system_blas:
            self.requires("openblas/[>=0.3.5]@conan/stable")
            self.requires("lapack/3.7.1@conan/stable")

    def configure_cmake(self):
        cmake = CMake(self)

        # if self.options.link_with_mkl and not self.options.use_system_blas:
        #      raise Exception("Link with MKL options can only be True when use_system_blas is also True")
        
        cmake.definitions["ARMA_USE_WRAPPER"] = self.options.use_wrapper
        cmake.definitions["ARMA_NO_DEBUG"] = True
        cmake.definitions["DETECT_HDF5"] = False
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.build_shared

        cmake.configure(source_folder="armadillo-%s"%self.version)
        return cmake


    def source(self):
        tools.download(
            "http://sourceforge.net/projects/arma/files/{0}".format(self.source_tar_file), self.source_tar_file)
       
        self.run("tar -xvf {0}".format(self.source_tar_file))

        if not self.options.with_lapack:
            tools.replace_in_file(file_path="armadillo-%s/include/armadillo_bits/config.hpp"%self.version,
                               search="#define ARMA_USE_LAPACK",
                               replace="//#define ARMA_USE_LAPACK")
        
        if not self.options.with_blas:
            tools.replace_in_file(file_path="armadillo-%s/include/armadillo_bits/config.hpp"%self.version,
                               search="#define ARMA_USE_BLAS",
                               replace="//#define ARMA_USE_BLAS")


    def build(self):

        cmake = self.configure_cmake()
        cmake.build()


    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["armadillo"]
        return
      
