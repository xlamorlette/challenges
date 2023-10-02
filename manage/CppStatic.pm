package CppStatic;

use lib '.';
use Execute;
use Platform;

use POSIX;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    checkCpp
    formatCpp
);

sub checkCpp {
    # arguments:
    #    - verbose (defaut = 0)
    my $_verbose = $_[0] || 0;
    _runCppCheck($_verbose);
    #_runClangFormatDry($_verbose);
    #_runClangTidy($_verbose);
}

sub _runCppCheck {
    # arguments:
    #    - verbose (defaut = 0)
    my $_verbose = $_[0] || 0;
    return if platformIsWindows();
    my $conanRun = ". $releaseBuildDirectory/conanrun.sh";
    my $cppcheckOptions = "--quiet --enable=all --inline-suppr --disable=missingInclude --error-exitcode=2";
    my $cppcheckCommand = "cppcheck --project=$releaseBuildDirectory/compile_commands.json $cppcheckOptions";
    executeTestCommand("$conanRun; $cppcheckCommand", "run CppCheck", $_verbose);
}

sub _runClangFormatDry {
    # arguments:
    #    - verbose (default = 0)
    my ($_cmake_folder) = @_;
    my $_verbose = $_[1] || 0;
    executeTestCommand("$pyenv; cmake --build $releaseBuildDirectory --target clang_format_dry_run",
        "Check if C++ code is formatted clang_tidy", $_verbose);
}

sub formatCpp {
    # arguments:
    #    - verbose (default = 0)
    my $_verbose = $_[0] || 0;
    executeTestCommand("$pyenv; cmake --build $releaseBuildDirectory --target clang_format_inplace_edit",
        "Format C++ code clang_format", $_verbose);
}

sub _runClangTidy {
    # arguments:
    #    - verbose (default = 0)
    my $_verbose = $_[1] || 0;
    executeTestCommand("cmake --build $releaseBuildDirectory --target clang_tidy",
        "Check C++ code with clang-tidy", $_verbose);
}

1;
