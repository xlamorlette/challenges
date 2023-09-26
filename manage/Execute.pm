package Execute;

use lib '.';
use Platform;

use POSIX;

use Exporter;
our @ISA = qw(Exporter);
our @EXPORT = qw(
    executeCommandIgnoreReturnCode
    executeTestCommand
);

sub executeCommandIgnoreReturnCode {
    # arguments:
    #    - command to execute
    #    - title of the command for verbose mode
    #    - verbose (default = 0)
    my ($command, $title) = @_;
    my $_verbose = $_[2] || 0;
    return executeTestCommand($command, $title, $_verbose, 1);
}

sub executeTestCommand {
    # execute a given command which is a test
    # arguments:
    #    - command to execute
    #    - title of the command for verbose mode
    #    - verbose (default = 0)
    #    - ignore return code (default = 0)
    my ($command, $title) = @_;
    my $_verbose = $_[2] || 0;
    my $ignoreReturnCode = $_[3] || 0;
    chomp($command);
    chomp($title);
    die "No command to execute\n" if (! $command);
    print "${titleColour}$title...${normalText}\n" if ($title && ! $quiet);
    print "${commandColour}> $command${normalText}\n" if ($_verbose);
    my $commandHandler;
    if (platformIsWindows()) {
        open $commandHandler, "powershell $command |";
    } else {
        open $commandHandler, "$command 2>&1 |";
    }
    my $output = "";
    while (<$commandHandler>) {
        print "$_" if ($_verbose);
        $output .= "$_";
    }
    close $commandHandler;
    my $returnCode = $?;
    if ((! $ignoreReturnCode) && ($returnCode != 0)) {
        print "$output" if (! $_verbose);
        print "$errorColour";
        print "$title " if ($title);
        print "failed${normalText}\n";
        die "Error (return code: ${returnCode}) while executing: $command\n";
    }
    print "${okColour}OK${normalText}\n" if (! $quiet);
    return $output;
}

1;
