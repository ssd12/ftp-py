import socket, os, sys, re, os

def create_socket(host, port, backlog):
  # create a TCP socket (SOCK_STREAM)
  s = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  # bind to host, port
  s.bind((host, port))
  # start listening - backlog = no. of unaccepted conns before refusing
  s.listen(backlog)
  return s


#d is dir, f is the file name
def read_file(fn):
  f = open(fn, 'rb')
  return f

def save_file(d, fn, fbytes):
  f = open(d+'/'+fn, 'wb')
  f.write(fbytes)
  f.close()

#d will be current working directory
def list_files(d):
  return os.listdir(d)

#fl is a list of files
def print_list_files(fl):
  for i in fl: print('\t '+ i)

#returns T/F based on if file is in directory
#f is name of file
def file_present(f, d):
  files = list_files(d)
  return (f in files)

def send_file(s, c):
  s.sendfile(c)

def send_msg(s, c):
  s.send(c.encode('utf-8'))

def get_message(s, bufsize):
  data = s.recv(bufsize)
  return data

