package Platform;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    $buildBaseDirectory
    $commandColour
    $debugBuildDirectory
    $errorColour
    $infoColour
    $mkdir
    $ninja
    $normalText
    $okColour
    $pyenv
    $pyenvDirectory
    $pytest
    $python
    $releaseBuildDirectory
    $rm
    $titleColour
    $underlined
    checkPlatformIsLinux
    checkPlatformIsWindows
    platformIsLinux
    platformIsWindows
);

$platform = $^O;
sub platformIsWindows() {
    return ($platform eq "MSWin32");
}
sub platformIsLinux() {
    return ($platform eq "linux");
}
sub checkPlatformIsWindows() {
    die "You can run this only on Windows" if (! platformIsWindows());
}
sub checkPlatformIsLinux() {
    die "You can run this only on Unix" if (! platformIsLinux());
}

$ninja = "ninja";

$gccCompilerDirectory = "x64/g++-11.3.0";
$vccCompilerDirectory = "x64/vc15";

if (platformIsWindows()) {
    $compilerDirectory = $vccCompilerDirectory;
    $mkdir = "mkdir -ErrorAction Ignore -p";
    $platformDirectory = "Windows";
    $pyenvDirectory = ".pyenv-windows";
    $pyenv = "$pyenvDirectory/Scripts/Activate.ps1";
    $python = "python";
    $pytest = "py.test.exe";
    $rm = "rm -Force -Recurse -ErrorAction Ignore";
} else {
    $compilerDirectory = $gccCompilerDirectory;
    $mkdir = "mkdir -p";
    $platformDirectory = "Linux";
    $pyenvDirectory = ".pyenv-linux";
    $pyenv = ". $pyenvDirectory/bin/activate";
    $python = "python3";
    $pytest = "python3 -m pytest";
    $rm = "rm -rf";
}

$buildBaseDirectory = "build/$platformDirectory";
$buildDirectory = "$buildBaseDirectory/$compilerDirectory";

$debugBuildDirectory = "$buildDirectory/Debug";
$releaseBuildDirectory = "$buildDirectory/Release";

if (platformIsWindows()) {
    `powershell Write-Host`;
    $normalText = "\e[0m";
    $underlined = "\e[4m";
    $inversed   = "\e[7m";
    $yellow    = "\e[1m";
    $red       = "\e[31m";
    $green     = "\e[32m";
    $blue      = "\e[34m";
    $darkBlue  = "\e[35m";
    $turquoise = "\e[36m";
    $grey      = "\e[37m";
    $backBlack     = "\e[40m";
    $backRed       = "\e[41m";
    $backGreen     = "\e[42m";
    $backWhite     = "\e[43m";
    $backBlue      = "\e[44m";
    $backDarkBlue  = "\e[45m";
    $backTurquoise = "\e[46m";
    $backGrey      = "\e[47m";
    $okColour      = $backGreen;
    $errorColour   = $backRed;
    $infoColour    = $backBlue;
    $titleColour   = $yellow;
    $commandColour = $turquoise;
} else {
    $normalText = "\033[0m";
    $red       = "\033[1;31m";
    $green     = "\033[1;32m";
    $yellow    = "\033[1;33m";
    $blue      = "\033[1;34m";
    $pink      = "\033[1;35m";
    $turquoise = "\033[1;36m";
    $okColour      = $green;
    $errorColour   = $red;
    $titleColour   = $blue;
    $commandColour = $yellow;
}

1;
