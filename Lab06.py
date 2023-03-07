import requests
import hashlib
import subprocess
import os


def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()
    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()
    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):
        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)
        # Silently run the VLC installer
        run_installer(installer_path)
        # Delete the VLC installer from disk
        delete_installer(installer_path)


def get_expected_sha256():

    # Send GET message to download the file
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    resp_msg = requests.get(file_url)
    # Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
    # Extract text file content from response message body
        file_content = resp_msg.text
    # Split the text file content into a list of jokes
    expected_hash = file_content.split()[0]
    # Print the 5th joke in the list
    return expected_hash


def download_installer():

    # Download the VLC installer from the VLC website
    url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp = requests.get(url)
    # Check whether the download was successful
    if resp.status_code != requests.codes.ok:
        raise Exception('Download failed')
    # Extract binary file content from response message body
    installer_data = resp.content
    return installer_data


def installer_ok(installer_data, expected_sha256):

    # Calculate the SHA-256 hash value of the downloaded installer
    computed_hash = hashlib.sha256(installer_data).hexdigest()
    # Check whether the computed hash value matches the expected value
    return computed_hash == expected_sha256


def save_installer(installer_data):

    # Save the downloaded VLC installer to disk
    installer_path = os.path.join(os.getcwd(), 'vlc_installer.exe')
    with open(installer_path, 'wb') as f:
        f.write(installer_data)
    return installer_path


def run_installer(installer_path):
    
    # Silently run the VLC installer
    subprocess.run([installer_path, '/L=1033', '/S'])


def delete_installer(installer_path):
  
    # Delete the VLC installer from disk
    os.remove(installer_path)


if __name__ == '__main__':
    main()