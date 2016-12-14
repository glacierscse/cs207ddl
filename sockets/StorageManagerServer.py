
from timeseries.FileStorageManager import FileStorageManager
from timeseries.ArrayTimeSeries import ArrayTimeSeries


def clientThread(conn, storage_manager):
    while True:
    	rec = conn.recv(1024*4)
    	if not rec:
    		break
    	print("Server has been received:", rec)
    	
    	recv_data = pickle.loads(rec)

        if recv_data['cmd'] == "GET_BY_ID":
        	ts = storage_manager.get(recv_data['id'])
        	ts_dict = {"time": list(ts.times()), "value": list(ts.values()), "id": recv_data['id']}
        	conn.send(pickle.dumps(toSend))

        elif recv_data['cmd'] == 'ADD_TS':
        	id = recv_data['id']
        	time = recv_data['time']
        	value = recv_data['value']
        	storage_manager.store(id, ArrayTimeSeries(list(time.values)), list(value.values()))
        	conn.send(pickle.dumps("Saved to DataBase."))
        	
    conn.close()



if __name__ == "main":
	storage_manager = FileStorageManager()

	HOST = gethostname()
	PORT = 15001
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
    s.listen(5)

    try:
    	while True:
			conn, addr = s.accept()
			print('Connected by', addr)
			t = threading.Thread(target=clientThread,args=(conn, storage_manager))
			t.start()
	finally:
		s.close()    