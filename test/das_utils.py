from subprocess import run as subprocess_run

# ---------------------------------------------------------------------------------
# Get file corresponding to a dataset/run/ls from DAS
def get_file(dataset_name, runNumber, ls):
    # Das query
    command = f"-query='file dataset={dataset_name} run={runNumber} lumi={ls}'"

    # Run the query
    das_res = subprocess_run(' '.join(['dasgoclient', command]),
        check=True,
        capture_output=True,
        text=True,
        shell=True
    )

    # Parse response
    if len(das_res.stdout) < 10:
        print("  File not found for run={R} ls={L}".format(R=runNumber,L=ls))
        return None

    # Return file name
    return das_res.stdout.strip("\n")

# ---------------------------------------------------------------------------------
# Get lumis from run and dataset
def get_max_lumi(dataset_name, runNumber):
    # Das query
    command = f"-query='lumi dataset={dataset_name} run={runNumber} | grep lumi.max_lumi'"

    # Run the query
    das_res = subprocess_run(' '.join(['dasgoclient', command]),
        check=True,
        capture_output=True,
        text=True,
        shell=True
    )

    # Parse response
    if len(das_res.stdout) < 10:
        msg = "Max Lumi not found, with:\n  out: %s\n  err:%s" % (das_res.stdout, das_res.stderr)
        raise Exception(msg)

    # Return max lumi
    return int(das_res.stdout.strip())

# ---------------------------------------------------------------------------------
# Parse the input '--runs' argument
# Produces a ist of dictionaries [{run1:(ls,ls)}, {run2:(ls,ls)}...]
def get_run_ranges(dataset_name, run_string):
    # Parse run numbers
    run_ranges = [(int(run.split('-')[0                ].split(':')[0]),
                   int(run.split('-')[int('-' in run)  ].split(':')[0])
                  ) for run in run_string]
    assert all(r2>=r1 for (r1,r2) in run_ranges), "ERROR: run ranges are ill defined"

    # Parse lumisections
    ls_ranges = [(int(run.split('-')[0                ].split(':')[1]),
                  int(run.split('-')[int('-' in run)  ].split(':')[1])
                 ) for run in run_string]

    # Collect all run-lumi ranges
    res = []
    for i,run_range in enumerate(run_ranges):

        runls = {}

        # Case 1: one run only
        if run_range[0] == run_range[1]:
            runls[run_range[0]] = ls_ranges[i]

        # Case 2: two consecutive runs
        elif run_range[0] + 1 == run_range[1]:
            max_lumi = get_max_lumi(dataset_name, run_range[0])
            runls[run_range[0]] = (ls_ranges[i][0], max_lumi)
            runls[run_range[1]] = (1, ls_ranges[i][1])

        # Case 3: more than two runs
        else:
            for run in range(run_range[0], run_range[1]+1):
                # First run
                if run == run_range[0]:
                    max_lumi = get_max_lumi(dataset_name, run)
                    runls[run] = (ls_ranges[i][0], max_lumi)
                # Last run
                elif run == run_range[1]:
                    runls[run] = (1, ls_ranges[i][1]+1)
                # Middle runs
                else:
                    max_lumi = get_max_lumi(dataset_name, run)
                    runls[run] = (1, max_lumi)

        # Store parsed output
        res.append(runls)

    return res
