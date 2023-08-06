
# ssh-Colab
ssh-Colab is a Python module to facilitate remote access to Google Colaboratory (Colab) through Secure Shell (SSH) connections, secured by a third-party software, ngrok. The module automates the tedious routine to set up ngrok tunnels needed for TPU runtime applications and services like TensorBoard. It also provides subroutines for (1) Kaggle Data API installation, (2) Kaggle competition data downloads, (3) data transfers between Colab and Google Cloud Storage (GCS), and (4) Google Drive mounting.

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
![python version](https://img.shields.io/badge/python-3.6%2C3.7%2C3.8-blue?logo=python)

# Prerequisites
- [ngrok](https://ngrok.com/) tunnel authtoken.
- Google account to access a [Colab](https://colab.research.google.com/notebooks/intro.ipynb) notebook.
- Local code editors such as VS Code or PyCharm to make the most of coding on Colab.

# Usage
1. Launch a Colab notebook. Choose a runtime type you prefer.

2. Install ssh-Colab. Type and run the following command in a new notebook cell:
   ```shell
   !pip install ssh-Colab
   ```
   
   Or you can use this command:
   
   ```shell
   !pip install git+https://github.com/libinruan/ssh_Colab.git#egg=ssh_Colab
   ```
   
   Another way to install this package is to Git clone its repository to Colab. Run in a new notebook cell:
   
   ```shell
   !git clone https://github.com/libinruan/ssh_Colab.git
   %cd ssh_Colab
   !sudo python setup.py install
   ```
   
   
   
3. Initiate the establishment of tunnels:
   ```python
   import sshColab
   sshColab.connect([LOG_DIR='/path/to/log/'])
   ```
   The default TensorBoard log directory is `/log/fit`. 
   
4. Retrieve information that is used for establishing the SSH connection:
   ```python
   sshColab.info()
   ```
   If you are running a non-TPU-enabled notebook, the setup instruction of TPU resolver is skipped.
   
5. To activate Kaggle API installation/authentication and download competition data, run:
   
   ```python
   sshColab.kaggle([data=<name-of-competition>, output=<output-directory>])
   ```
   Note that the default competition name is `tabular-playground-series-mar-2021`. The data is unzipped to the destination folder `/kaggle/input` by default. 

6. To mount a google drive, run:

7. To connect with GCS, initiate the connection:
   ```python
   sshColab.GCSconnect()
   ```
   To create a GCS Bucket, run:
   ```python
   sshColab.create_bucket(<project_id>, <bucket_name>)
   ```
   To list blobs in a GCS bucket, run:
   ```python
   sshColab.list_blobs(<project_id>, <bucket_name>)
   ```
   To upload files from Colab to a GCS Bucket, run:
   ```python
   sshColab.upload_to_gcs(<project_id>, <bucket_name>, [file=<local_file> ,ext=<file_extension>])
   ```
   To download files from a GCS Bucket to Colab, run:
   ```python
   sshColab.download_to_colab(<project_id>, <bucket_name>, [file=<local_file>])
   ```
   
8. To disable ngrok tunnels created, run the command below:
   ```python
   sshColab.kill()
   ```

# Quickstart
A short Colab notebook is provided in the link below. Users can
find a simple end-to-end application starting from ssh-Colab installation, SSH
tunnel creation, to the use of TensorBoard after training a 3-layer MNIST
convolutional neural network. 

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uvLXA5hC8tyMjsA09H3Y5IPi_N54aXbw?usp=sharing) 

What's missed in this quick start guide is how to may our way to Colab instances from
local machines. The reference listed below can be a start point for interested
users:

1. [Remote development over SSH on local VS Code](https://code.visualstudio.com/docs/remote/ssh-tutorial)
2. [Run SSH terminal on local PyCharm](https://www.jetbrains.com/help/pycharm/running-ssh-terminal.html)

# Releases

version 0.3.3: Addition of the output argument for function kaggle().

version 0.3.0: Addition of functions for communicating with Google Cloud Storage.

version 0.2.0: Addition of Google Drive mounting function.

version 0.1.3: Addition of Kaggle API installation/authentication and competition data downloading function.


# Feedback
Comments and suggestions are welcome and appreciated. They can be sent to
lipin.juan02@gmail.com.

