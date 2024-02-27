import subprocess
import os

def download_data(obj_name, date, obs_id):
    try:
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
        subprocess.run(wget_command_auxil, shell=True)
        subprocess.run(wget_command_xrt, shell=True)
        subprocess.run(wget_command_uvot, shell=True)
        print("Download complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Get user input for the name of the TDE
    TDE_name = input("Enter the name of the object (ex: ASASSN-15oi): ")

    # Get user input for the observation date 
    date = input("Enter the observation date (ex: 2015_09): ")

    # Get user input for the observation ID
    obs_id = input("Enter the observation ID (ex: 00033999001): ")

    # Call the download_data function with the provided input
    download_data(TDE_name, date, obs_id)