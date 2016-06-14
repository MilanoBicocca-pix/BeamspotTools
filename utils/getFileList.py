import glob
import os
import subprocess
import fnmatch


def eos_command():

  shell = os.getenv('SHELL')
  cmd = subprocess.Popen(shell+' -c "which eos"', shell=True, stdout=subprocess.PIPE)

  for i, line in enumerate(cmd.stdout):
      if i > 0 : break
      eos = line.split(' ')[-1].rstrip()

  return eos


def get_eos_files_old(path, pattern, prependPath):

    eos = eos_command()
    list_files_cmd = '{EOS} ls {PATH}'.format(EOS = eos, PATH = path)
    cmd = subprocess.Popen(list_files_cmd, shell = True,
                           stdout = subprocess.PIPE)
    files = []

    for i, line in enumerate(cmd.stdout):
        file = line.split(' ')[-1].rstrip()
        if len(pattern):
            if not fnmatch.fnmatch(file, pattern):
                continue
        files.append('/'.join([prependPath * path, file]))

    return files

def get_eos_files(path, pattern, prependPath):

    eos = eos_command()
    dirs = path.split('*')
    
    # put an escape if len(dirs) == 1
    
    combinatorics = [[] for i in range(len(dirs))]
    
    for i, dir in enumerate(dirs):
        import pdb ; pdb.set_trace()
        for k in combinatorics[max(0, i-1)]:
            import pdb ; pdb.set_trace()
            mydir = '/'.join(dir.split('/')[:-1] + [k])
            
            list_dirs_cmd = '{EOS} ls {PATH}'.format(EOS = eos, PATH = mydir)
            cmd = subprocess.Popen(list_dirs_cmd, shell = True,
                                   stdout = subprocess.PIPE)
    
            for j, line in enumerate(cmd.stdout):
                element = line.split(' ')[-1].rstrip()
                if not fnmatch.fnmatch(element, dir.split('/')[-1] + '*'):
                   continue
                combinatorics[i].append(element)

    import pdb ; pdb.set_trace()



#     return files


def get_afs_files(path, pattern, prependPath):
    '''
    accepts wildcards too, e.g.
    PATH1/*PATH2*/CommonString*.root
    '''
    allfiles = glob.iglob(path)
    files = []
    for f in allfiles:
        if len(pattern):
            if not fnmatch.fnmatch(file, pattern):
                continue
        if prependPath:        
           files.append(f)
        else:
           files.append(f.split('/')[-1])           
    return files


def get_files(path, pattern = '', prependPath = False):

    if path.startswith('/store'):
        return get_eos_files(path, pattern, prependPath)
    else:
        return get_afs_files(path, pattern, prependPath)





if __name__ == '__main__':
#     for file in get_files('/store/relval/CMSSW_8_1_0_pre6/RelValTenMuE_0_200/GEN-SIM-DIGI-RAW/80X_mcRun2_asymptotic_v14_2023tilted-v1/00000'):
#         print file

#     for file in get_files('/store/relval/CMSSW_8_1_0_pre6/RelValTenMuE_0_200/GEN-SIM-DIGI-RAW/80X_mcRun2_asymptotic_v14_2023tilted-v1/00000', '76F3*'):
#         print file

#     for file in get_files('./*'):
#         print file

    get_files('/store/relval/CMSSW_8_1_0_pre6/RelValTenMuE_0_200/*/*/00000')





