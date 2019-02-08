import socket, sys, threading, re, argparse, os, time
import ftp_util as su

#handles client input
def handle_client_io(cs):
  bufsize = 1024
  print('Type messages, enter to send: ')
  while True:
    payload = input() # blocks
    contents = re.split(' ', payload)
    #print('\tcontents ', contents)
    if (len(contents) > 1):
      #content is either upload, download, cd, or an unrecognized command
      if contents[0] == 'upload':
        file_name = contents[1]
        abs_file_name = os.getcwd() + '/' + file_name
        if (os.path.exists(abs_file_name)):
          file_to_tranfer = su.read_file(abs_file_name)
          file_size = str(os.path.getsize(abs_file_name))
          #send message to server that file will uploaded
          upload_message = 'upload '+file_name+' '+file_size
          print('\t', upload_message)
          su.send_msg(cs, upload_message)
          su.send_file(cs, file_to_tranfer)
        else:
          print("File not found.", abs_file_name)
      elif contents[0] == 'download':
        file_name = contents[1]
        su.send_msg(cs, payload)
        # get message back from serve
        recv_payload = su.get_message(cs, bufsize).decode('utf-8')
        recv_contents = re.split(' ', recv_payload)
        if (recv_contents[0] == 'FileNotFound'):
          print('\tFile not found.')
        else:
          print('\tReceiving content ', recv_contents)
          fBytes = cs.recv(int(recv_contents[2]))
          su.save_file(os.getcwd(), contents[1], fBytes)

      elif contents[0] == 'cd':
         su.send_msg(cs, payload)
         msg = cs.recv(bufsize)
         print('\t',msg.decode('utf-8'))
      else:
        print("Unrecognized command.")
    else:
      if contents[0] == 'list':
        print('\tRequesting Files list')
        su.send_msg(cs,'list')
        lst = cs.recv(bufsize).decode('utf')
        print('\t', lst)
      elif contents[0] == 'close':
        su.send_msg(cs,'close')
        break
      else:
        print("Unrecognized command")


def run_client(host, port):
  try:
    #create socket and connect to port (hardcoded as server)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((host, port))
    print("Connected to {} on port {}".format(host, port))
    handle_client_io(client_sock)
    client_sock.close()
  except socket.error as err:
    print("Error: %s" %str(err))
    sys.exit();



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-host', '--host', default='127.0.0.1')
  parser.add_argument('-p', '--port', default='9022')
  args = parser.parse_args()
  run_client(args.host, int(args.port))
