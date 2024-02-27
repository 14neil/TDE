import os
import subprocess

def download_data(obj_name, date, obs_id):
    # Set the base path to the raw folder
    base_path = os.path.join(os.environ['HOME'], 'TDE', obj_name, 'raw')

    # Build the wget command with the provided input and updated path
    wget_command_auxil = (
        f"wget -q -nH --no-check-certificate --cut-dirs=5 -r -l0 -c -N -np "
        f"-R 'index*' -erobots=off --retr-symlinks "
        f"https://heasarc.gsfc.nasa.gov/FTP/swift/data/obs/{date}/{obs_id}/auxil/ -P {base_path}"
    )

    wget_command_xrt = (
        f"wget -q -nH --no-check-certificate --cut-dirs=5 -r -l0 -c -N -np "
        f"-R 'index*' -erobots=off --retr-symlinks "
        f"https://heasarc.gsfc.nasa.gov/FTP/swift/data/obs/{date}/{obs_id}/xrt/ -P {base_path}"
    )

    wget_command_uvot = (
        f"wget -q -nH --no-check-certificate --cut-dirs=5 -r -l0 -c -N -np "
        f"-R 'index*' -erobots=off --retr-symlinks "
        f"https://heasarc.gsfc.nasa.gov/FTP/swift/data/obs/{date}/{obs_id}/uvot/ -P {base_path}"
    )

    # Run the wget commands using subprocess
    os.system(wget_command_auxil)
    os.system(wget_command_xrt)
    os.system(wget_command_uvot)
    print('Download complete.')

def get_uvotimsum_sk(obj_name, obs_id, filtr):
    uvotimsum_sk_command = (
    f'uvotimsum infile=$HOME/TDE/{obj_name}/raw/{obs_id}/uvot/image/sw{obs_id}{filtr}_sk.img.gz'
    f' outfile=$HOME/TDE/{obj_name}/sum/sum_{obs_id}{filtr}_sk.img.gz'
    ' method=EXPMAP clobber=yes exclude=DEFAULT ignoreframetime=yes'
    )
    # Run the uvotimsum_sk command
    os.system(uvotimsum_sk_command)   

def get_uvotimsum_ex(obj_name, obs_id, filtr):
    uvotimsum_ex_command = (
    f'uvotimsum infile=$HOME/TDE/{obj_name}/raw/{obs_id}/uvot/image/sw{obs_id}{filtr}_ex.img.gz'
    f' outfile=$HOME/TDE/{obj_name}/sum/sum_{obs_id}{filtr}_ex.img.gz'
    ' method=EXPMAP clobber=yes exclude=DEFAULT ignoreframetime=yes'
    )
    # Run the uvotimsum_ex command
    os.system(uvotimsum_ex_command) 

def get_uvotsource(obj_name, obs_id, filtr):
    uvotsource_command = (
    f'uvotsource image=$HOME/TDE/{obj_name}/sum/sum_{obs_id}{filtr}_sk.img.gz'
    f' srcreg=$HOME/TDE/{obj_name}/reg/sou_{filtr}_5as.reg'
    f' bkgreg=$HOME/TDE/{obj_name}/reg/bkg_{filtr}_clear.reg sigma=3 zerofile=caldb'
    f' coinfile=caldb psffile=caldb apercorr=CURVEOFGROWTH syserr=y'
    f' expfile=$HOME/TDE/{obj_name}/sum/sum_{obs_id}{filtr}_ex.img.gz lssfile=caldb'
    f' sensfile=caldb fwhmsig=-1 deadtimecorr=yes cleanup=yes clobber=y chatter=1'
    f' output=ALL outfile=$HOME/TDE/{obj_name}/flux/sum_{obs_id}{filtr}_5as.fit'
    )
    # Run the uvotsource command 
    os.system(uvotsource_command)

if __name__ == '__main__':
    # Get user input for the name of the TDE
    TDE_name = input('Enter the name of the object (ex: ASASSN-15oi): ')

    # Get user input of the observation ID(s)
    obs_IDs_input = input('Enter a comma separated list of obs. IDs (ex: 00033999001, ...): ')
    obs_IDs_list = [word.strip() for word in obs_IDs_input.split(',')]
    
    # Get user input for the observation date(s)
    dates_input = input('Enter their respective dates (ex: 2015_09, ...): ')
    dates_list = [word.strip() for word in dates_input.split(',')]


    # Call all of the commands
    for i in range(len(obs_IDs_list)):
        download_data(TDE_name, dates_list[i], obs_IDs_list[i])
        filters = ['ubb', 'um2', 'uuu', 'uvv', 'uw1', 'uw2']
        for filt in filters: 
            get_uvotimsum_sk(TDE_name, obs_IDs_list[i], filt)
            get_uvotimsum_ex(TDE_name, obs_IDs_list[i], filt) 
            get_uvotsource(TDE_name, obs_IDs_list[i], filt)