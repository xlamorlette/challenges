package PythonStatic;

use lib '.';
use Execute;
use Platform;

use POSIX;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    runPythonCheck
);

sub runPythonCheck {
    # run pylint and compare result with a reference
    # arguments:
    #    - mypy configuration file
    #    - pycodestyle configuration file
    #    - pylint configuration file
    #    - pylint result reference file
    #    - files to check
    #    - verbose (defaut = 0)
    checkPlatformIsLinux();
    my ($mypyConfigFile, $pycodestyleConfigFile, $pylintRcFile, $pylintReferenceFile, $pythonFiles) = @_;
    my $_verbose = $_[5] || 0;
    _runMypy($mypyConfigFile, $pythonFiles, $_verbose);
    _runPycodestyle($pycodestyleConfigFile, $pythonFiles, $_verbose);
    _runPylint($pylintRcFile, $pylintReferenceFile, $pythonFiles, $_verbose);
}

sub _runMypy {
    # arguments:
    #    - mypy configuration file
    #    - files to check
    #    - verbose
    my ($mypyConfigFile, $pythonFiles, $_verbose) = @_;
    executeTestCommand("$pyenv; mypy --config-file=$mypyConfigFile --install-types --non-interactive $pythonFiles", "run mypy", $_verbose);
}

sub _runPycodestyle {
    # arguments:
    #    - pycodestyle configuration file
    #    - files to check
    #    - verbose
    my ($pycodestyleConfigFile, $pythonFiles, $_verbose) = @_;
    executeTestCommand("$pyenv; pycodestyle --config=$pycodestyleConfigFile $pythonFiles", "run pycodestyle", $_verbose);
}

sub _runPylint {
    # run pylint and compare result with a reference
    # arguments:
    #    - pylint configuration file
    #    - pylint result reference file
    #    - files to check
    #    - verbose
    my ($pylintRcFile, $pylintReferenceFile, $pythonFiles, $_verbose) = @_;
    $pylintResultFile = "/tmp/pylint_result";
    executeCommandIgnoreReturnCode("$rm  $pylintResultFile", "clean pylint temporary result file");
    $pylintCommand = "pylint --rcfile=$pylintRcFile --reports=n --score=no --jobs=0 $pythonFiles";
    executeTestCommand("$pyenv; $pylintCommand 2>/dev/null | grep -v \"^\*\" | sort | tee $pylintResultFile",
        "run pylint", $_verbose, 1, 1);
    executeTestCommand("diff --strip-trailing-cr $pylintReferenceFile $pylintResultFile", "compare pylint result with reference");
    executeCommandIgnoreReturnCode("$rm  $pylintResultFile", "clean pylint temporary result file");
}

1;
