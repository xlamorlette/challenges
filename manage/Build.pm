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
    my $_verbose = $_[1] || 0;
    my $buildDirectory = $mode eq "Release" ? $releaseBuildDirectory : $debugBuildDirectory;
    my $buildCommand = platformIsLinux()
        ? $ninja
        : "cmake --build . --config $mode";
    executeTestCommand("$pyenv; cd $buildDirectory; $buildCommand", "build in $mode mode", $_verbose);
}

sub cleanBuild {
    # arguments:
    #    - verbose (optional)
    my $_verbose = $_[0] || 0;
    executeCommandIgnoreReturnCode("$rm ./$buildBaseDirectory", "clean build directory", $_verbose);
}

sub cleanMiscArtefacts {
    # argument:
    #    - verbose (optional)
    my $_verbose = $_[0] || 0;
    if (platformIsLinux()) {
        executeCommandIgnoreReturnCode("$rm .mypy_cache", "clean Mypy cache", $_verbose);
        executeCommandIgnoreReturnCode("$rm test-reports 2>/dev/null", "clean test reports", $_verbose);
        executeCommandIgnoreReturnCode("find . -name __pycache__ | xargs rm -rf", "clean Python caches", $_verbose);
        executeCommandIgnoreReturnCode("find . -name *.egg-info | xargs rm -rf", "clean Python eggs", $_verbose);
        executeCommandIgnoreReturnCode("find . -name .pytest_cache | xargs rm -rf", "clean Pytest cache", $_verbose);
    }
    executeCommandIgnoreReturnCode("$rm CMakeUserPresets.json", "clean CMakeUserPresets", $_verbose);
}

sub prepareBuild {
    # arguments:
    #    - baseDirectory
    #    - verbose (optional)
    my ($baseDirectory) = @_;
    my $_verbose = $_[1] || 0;
    executeTestCommand("$pyenv; conan profile detect --force", "detect Conan profile", $_verbose);
    executeCommandIgnoreReturnCode("$mkdir $releaseBuildDirectory", "create Release build directory", $_verbose);
    executeCommandIgnoreReturnCode("$mkdir $debugBuildDirectory", "create Debug build directory", $_verbose);
    executeTestCommand("$pyenv; conan install . -s build_type=Release --output-folder=$releaseBuildDirectory --build=missing",
        "install Conan packages in Release mode", $_verbose);
    executeTestCommand("$pyenv; conan install . -s build_type=Debug --output-folder=$debugBuildDirectory --build=missing",
        "install Conan packages in Debug mode", $_verbose);
    my $cmakeOptions = platformIsLinux()
        ? "-G Ninja"
        : "-DCMAKE_TOOLCHAIN_FILE='conan_toolchain.cmake'";
    executeTestCommand("$pyenv; cd $releaseBuildDirectory; "
        . "cmake $cmakeOptions -DCMAKE_BUILD_TYPE=Release $baseDirectory", "call CMake in Release mode", $_verbose);
    executeTestCommand("$pyenv; cd $debugBuildDirectory; "
        . "cmake $cmakeOptions -DCMAKE_BUILD_TYPE=Debug $baseDirectory", "call CMake in Debug mode", $_verbose);
}

1;
