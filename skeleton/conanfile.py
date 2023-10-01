from conan import ConanFile
from conan.tools.cmake import CMakeToolchain


class SkeletonConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    def requirements(self):
        self.requires("catch2/3.4.0")
        self.requires("zlib/1.2.11")

    def generate(self):
        tc = CMakeToolchain(self)
        if self.settings.os == "Linux":
            tc.user_presets_path = False
        tc.generate()
