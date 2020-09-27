from multiprocessing import Process, Pipe, Manager

from datetime import datetime



def local_time(counter):
    return ' (VECTOR_TIME={}, LOCAL_TIME={})'.format(counter,
                                                     datetime.now())



def calc_recv_timestamp(recv_time_stamp, counter):
    for id  in range(len(counter)):
        counter[id] = max(recv_time_stamp[id], counter[id])
    return counter


def event(pid, counter):
    counter[pid] += 1
    print('Something happened in {} !'.\
          format(pid) + local_time(counter))
    return counter

def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter

def recv_message(pipe, pid, counter):
    counter[pid] += 1
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid)  + local_time(counter))
    return counter


def process_one(pipe12):
    pid = 0
    vector = [0, 0, 0]
    vector = send_message(pipe12, pid, vector)
    vector = send_message(pipe12, pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe12, pid, vector)
    vector = event(pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe12, pid, vector)



def process_two(pipe21, pipe23):
    pid = 1
    vector = [0, 0, 0]
    vector = recv_message(pipe21, pid, vector)
    vector = recv_message(pipe21, pid, vector)
    vector = send_message(pipe21, pid, vector)
    vector = recv_message(pipe23, pid, vector)
    vector = event(pid, vector)
    vector = send_message(pipe21, pid, vector)
    vector = send_message(pipe23, pid, vector)
    vector = send_message(pipe23, pid, vector)



def process_three(pipe32):
    pid = 2
    vector = [0, 0, 0]
    vector = send_message(pipe32, pid, vector)
    vector = recv_message(pipe32, pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe32, pid, vector)



if __name__ == '__main__':



    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one,
                       args=(oneandtwo,))
    process2 = Process(target=process_two,
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_three,
                       args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

    # print(final_vector[0])
    # print(final_vector[1])
    # print(final_vector[2])

