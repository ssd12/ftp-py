Instructions for client_ftp.py and server_ftp.py

0. Folder structure
    
   ftp
    client
     data
        simpleFunc.py
     client_ftp.py
     ftp_util.py
     file.jpeg
     
    server
     data
        file.pdf
     ftp_util.py
     server_ftp.py
   
   ftp is the parent folder, while client and server are subfolders that contain
   the client and server programs with ftp_util.py (a utilities file used by both client and server), and
   miscellaneous sample files for transfer (file.pdf, file.jpeg, simpleFunc.py).    

1. server_ftp.py arguments flags are -p (port), -d (working directory), and -c (the maximum number of clients allowed). 

    Examples:
    > python server_ftp.py -p 12345
    In the above example, program will run on porst 12345
    > python server_ftp.py -d  '/home/cs/projects'
    In the above example, the servers current working directory will be set to  '/home/cs/projects'
    >python server_ftp.py -c 10
    In the above example, servers max no. of client to 10

2. client_ftp.py argument flags are -p (port) and -host

3. Client Commands and Examples:

    All examples assume that client and server are run with default flags/settings

    list: list will provide a list of all the files and folders for the server's current working directory
    
    cd: cd changes the server's current working directory. 
        cd .. : go back to parent folder
        cd [folder] : attempt to change directory to folder, i.e. current server working path + /folder
    
    close: closes client connection
    
    download: client can download a file with the 'download' command followed by file name. Files are downloaded from
    server's current working directory to the client's working directory. If the file cannot be downloaded, the client will get a message that  the file was not found.
    
    Example:
    (running in client shell)
    >cd data
    >download file.pdf
        
        When we start the server and client programs, the server's default working directory is the folder it is running in, i.e. /ftp/server
        folder. However, to download the file.pdf, which is located in the 'data' folder, we change directories by entering 'cd data'.
        Once we have changed the server's working directory to ftp/server/data, we can then download 'file.pdf'. File will be downloaded
        to /ftp/client
    
    upload: client uploads files from the directory that it is running in, i.e. /ftp/client. The client will upload the file to whatever the
    server's current working directory is (as set by client). 
    
    Example:
    >upload file.jpeg
    
    The command above will upload the file.jpeg to /ftp/server.
    
    If we want to upload the file to /ftp/server/data, then we change the directory to data by entering 'cd data', and then
    enter upload file.jpeg. Since the current working directory has been changed to /ftp/server/data, the file will be downloaded there
    instead of just /ftp/server.
    
    NOTE: You can upload files from the data folder in client, but pass the arguments as such data/[file], where file is the file to upload. There
    shouldn't be any backslashes before data. 
    
