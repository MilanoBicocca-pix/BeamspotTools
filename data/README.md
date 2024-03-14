# Description
The file `fills.txt` needs to be update manually every once in a while to keep up with LHC fills as they appear on the [CMS OMS](https://cmsoms.cern.ch/) website.

This is needed for plotting purposes, especially for displaying re-processed BeamSpot measurements.

# How to
Set up the needed Kerberos ticket with:
```
kinit <user>
```
Get the new fills run the `fetch_from_OMS.py` script with:
```
python3 fetch_fills_from_OMS.py \
    -n [number_of_fills] \
    -s [number_of_streams] \
    -S [size_of_stream] \
    -u [file_to_update] \
    -o [output_file]
```
Add the new fills to the `fills.txt` file (or update it directly with the `-u` option).

### Important note:
By default the scripts only considers Fills:
 - of type `PROTONS`
 - with Stable Beams declared

### Requirements:
- `python3`
- `auth-get-sso-cookie` (available on all lxplus nodes)
- **DO NOT** set `cmsenv` environment!
