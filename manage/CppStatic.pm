package CppStatic;

use lib '.';
use Execute;
use Platform;

use POSIX;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    runAllCheckCpp
    runFormatCpp
);

sub runAllCheckCpp {
    _runCppCheck($releaseBuildDirectory, $verbose);
    _runClangFormatDry($releaseBuildDirectory, $verbose);
    _runClangTidy($releaseBuildDirectory, $verbose);
}

sub _runCppCheck {
    # arguments:
    #    - cmake build folder
    #    - verbose (defaut = 0)
    my ($_cmake_folder) = @_;
    my $_verbose = $_[1] || 0;
    executeTestCommand("$pyenv; cmake --build $_cmake_folder --target cppcheck -- ",
    "C++ code static analysis cppcheck", $_verbose);
}

sub _runClangFormatDry {
    # arguments:
    #    - CMake build folder
    #    - verbose (default = 0)
    my ($_cmake_folder) = @_;
    my $_verbose = $_[1] || 0;
    executeTestCommand("$pyenv; cmake --build $_cmake_folder --target clang_format_dry_run",
        "Check if C++ code is formatted clang_tidy", $_verbose);
}

sub runFormatCpp {
    # arguments:
    #    - CMake build folder
    #    - verbose (default = 0)
    my ($_cmake_folder) = @_;
    my $_verbose = $_[1] || 0;
    executeTestCommand("$pyenv; cmake --build $_cmake_folder --target clang_format_inplace_edit",
        "Format C++ code clang_format", $_verbose);
}

sub _runClangTidy {
    # arguments:
    #    - CMake build folder
    #    - verbose (default = 0)
    my ($_cmake_folder) = @_;
    my $_verbose = $_[1] || 0;
   executeTestCommand("cmake --build $_cmake_folder --target clang_tidy",
        "Check C++ code with clang-tidy", $_verbose);
}

1;
