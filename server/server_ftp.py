import socket, threading, argparse, re, os, sys

import ftp_util as su


# func to handle a client request
def client_req_handler(cs, addr, d):
  cur_dir = d
  client_address = str(addr)
  print("Client connected from: %s" %client_address)
  bufsize = 1024
  payloads=[]
  while True:
    try:
      payload = su.get_message(cs, bufsize)    # this recv gets a string message = command
      # since payload is a command it needs to be decoded
      payload = payload.decode('utf-8')
    except (EOFError, ConnectionError, UnicodeDecodeError):
      #handle_disconnect(cs, addr)
      break

    #decode message
    contents = re.split(' ', payload)
    print(client_address,' request: ', contents)
    if (len(contents) > 1): # either cd, upload, download
      if contents[0] == 'upload':
        fBytes = cs.recv(int(contents[2]))
        su.save_file(cur_dir, contents[1], fBytes)
      elif contents[0] == 'download':
        abs_file_name = cur_dir + '/' + contents[1]
        if (os.path.exists(abs_file_name)):
          file_size = str(os.path.getsize(abs_file_name))
          file_to_tranfer = su.read_file(abs_file_name)
          message = 'download '+contents[1]+' '+file_size
          print('\t', message)
          su.send_msg(cs, message)
          su.send_file(cs, file_to_tranfer)
        else:
          message = 'FileNotFound'
          su.send_msg(cs, message)

      elif contents[0] == 'cd':
        try:
          os.chdir(contents[1])
          cur_dir = os.getcwd()
          su.send_msg(cs,'Directory changed.')
        except FileNotFoundError:
          su.send_msg(cs, 'Directory not found')
    else: # list and close
      if contents[0] == 'list':
        lst = str(su.list_files(cur_dir))
        su.send_msg(cs, lst)
      elif contents[0] == 'close':
        break
  cs.close()


# port : port on which server runs
# max_clients : max number of clients that can connect to ftp server
# cur_dir : working directory, i.e. where to upload/download files
def server(port, max_clients, cur_dir):
  print("Server running on port ", port)
  print("Working directory: ", cur_dir)
  server_sock = su.create_socket('localhost', port, max_clients)
  try:
    num_clients = 0
    while True:
      print('Current clients: ', num_clients)
      # accept a client
      client_sock, addr = server_sock.accept()
      # check if adding new client greater than max client connections
      if (num_clients >= max_clients):
        msg = 'Error: Server at full capacity. Try again later'
        print(msg)
        try:
          client_sock.close()
        except:
          pass
      else:
        t = threading.Thread(target = client_req_handler,
                           args = [client_sock, addr, cur_dir], daemon = True)
        num_clients += 1
        t.start()
    # server shutdown
    server_sock.close()
  except:
    print("Shutting server gracefully")
    server_sock.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--port', default = '9022')
  #directory is the server file directory. Default directory is server's working directory
  parser.add_argument('-d', '--directory', default = os.getcwd())
  parser.add_argument('-c', '--clients', default = 3)
  args = parser.parse_args()
  server(int(args.port), int(args.clients), args.directory)
