package Build;

use lib '.';
use Execute;
use Platform;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    build
    cleanBuild
    cleanMiscArtefacts
    prepareBuild
);

sub build {
    # arguments:
    #    - mode: Release / Debug
    #    - verbose (optional)
    my ($mode) = @_;
    local $verbose = $_[1] || 0;
    my $buildDirectory = $mode eq "Release" ? $releaseBuildDirectory : $debugBuildDirectory;
    my $buildCommand = platformIsLinux()
        ? $ninja
        : "cmake --build . --config $mode";
    executeTestCommand("$pyenv; cd $buildDirectory; $buildCommand", "build in $mode mode", $verbose);
}

sub cleanBuild {
    # arguments:
    #    - verbose (optional)
    local $verbose = $_[0] || 0;
    executeCommandIgnoreReturnCode("$rm ./$buildBaseDirectory", "clean build directory", $verbose);
}

sub cleanMiscArtefacts {
    # argument:
    #    - verbose (optional)
    local $verbose = $_[0] || 0;
    if (platformIsLinux()) {
        executeCommandIgnoreReturnCode("$rm .mypy_cache", "clean Mypy cache", $verbose);
        executeCommandIgnoreReturnCode("$rm test-reports 2>/dev/null", "clean test reports", $verbose);
        executeCommandIgnoreReturnCode("find . -name __pycache__ | xargs rm -rf", "clean Python caches", $verbose);
        executeCommandIgnoreReturnCode("find . -name *.egg-info | xargs rm -rf", "clean Python eggs", $verbose);
        executeCommandIgnoreReturnCode("find . -name .pytest_cache | xargs rm -rf", "clean Pytest cache", $verbose);
    }
    executeCommandIgnoreReturnCode("$rm CMakeUserPresets.json", "clean CMakeUserPresets", $verbose);
}

sub prepareBuild {
    # arguments:
    #    - baseDirectory
    #    - verbose (optional)
    my ($baseDirectory) = @_;
    local $verbose = $_[1] || 0;
    executeTestCommand("$pyenv; conan profile detect --force", "detect Conan profile", $verbose);
    executeCommandIgnoreReturnCode("$mkdir $releaseBuildDirectory", "create Release build directory", $verbose);
    executeCommandIgnoreReturnCode("$mkdir $debugBuildDirectory", "create Debug build directory", $verbose);
    executeTestCommand("$pyenv; conan install . -s build_type=Release --output-folder=$releaseBuildDirectory --build=missing",
        "install Conan packages in Release mode", $verbose);
    executeTestCommand("$pyenv; conan install . -s build_type=Debug --output-folder=$debugBuildDirectory --build=missing",
        "install Conan packages in Debug mode", $verbose);
    if (platformIsLinux()) {
        executeTestCommand("$pyenv; cd $releaseBuildDirectory; cmake -G Ninja -DCMAKE_BUILD_TYPE=Release "
            . " $baseDirectory", "call CMake in Release mode", $verbose);
        executeTestCommand("$pyenv; cd $debugBuildDirectory; cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug "
            . " $baseDirectory", "call CMake in Debug mode", $verbose);
    } else {
        executeTestCommand("$pyenv; cd $releaseBuildDirectory; cmake -DCMAKE_TOOLCHAIN_FILE='conan_toolchain.cmake' "
            . "-DCMAKE_BUILD_TYPE=Release $baseDirectory", "call CMake in Release mode", $verbose);
        executeTestCommand("$pyenv; cd $debugBuildDirectory; cmake -DCMAKE_TOOLCHAIN_FILE='conan_toolchain.cmake' "
            . "-DCMAKE_BUILD_TYPE=Debug $baseDirectory", "call CMake in Debug mode", $verbose);
    }
}

1;
