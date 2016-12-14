# import sys
import socket
# from concurrent.futures import ProcessPoolExecutor
# def fetch(i):
#     s = socket(AF_INET, SOCK_STREAM)
#     s.connect(('localhost', 15000))
#     print("sending, i",i)
#     s.send("a={}".format(i).encode())
#     print("sent")
#     return s.recv(65536)
# pool = ProcessPoolExecutor(10)
# thrs=[]
# for i in range(40):
#     t = pool.submit(fetch, i)
#     thrs.append(t)
# for i in range(40):
#     print('i', i, thrs[i].result())

def connectRBTree():
	port = 15000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()
	s.connect((host, port))
	print("Connecting")
	return s

if __name__ == '__main__':
	connectRBTree()