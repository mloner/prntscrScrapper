import string, random, os, sys, _thread, httplib2, shutil

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python3 " + sys.argv[0] + " (Number of threads)")

THREAD_AMOUNT = int(sys.argv[1])
INVALID = [0, 503, 5082, 4939, 4940, 4941, 12003, 5556]
picsInThread = []
currentPicsInThread = []
done = False
count = int(sys.argv[2]) // int(sys.argv[1])

for i in range(int(sys.argv[1])):
    currentPicsInThread.append(0)

for i in range(int(sys.argv[1])):
    picsInThread.append(count)

if int(sys.argv[2]) % int(sys.argv[1]) != 0:
    last = int(sys.argv[2]) - int(sys.argv[1]) * count
    picsInThread[int(sys.argv[1]) - 1] += last

def scrape_pictures(thread):
    global done
    while True:
        if len(sys.argv) > 2 and int(currentPicsInThread[int(thread)-1]) >= int(picsInThread[int(thread)-1]):
            print("thread " + thread + " done")
            if currentPicsInThread == picsInThread:
                print("All threads are done")
                done = True
            sys.exit()
        url = 'http://i.imgur.com/'
        length = random.choice((5, 6))
        if length == 5:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        else:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
            url += ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
        url += '.jpg'
        filename = url.rsplit('/', 1)[-1]
        h = httplib2.Http('.cache' + thread)
        response, content = h.request(url)
        response = h.request(url)[0]
        if response.status == 200:
            out = open('pcs/' + filename, 'wb')
            out.write(content)
            out.close()
            file_size = os.path.getsize('pcs/' + filename)
            if file_size in INVALID:
                os.remove('pcs/' + filename)
            else:
                currentPicsInThread[int(thread) - 1] += 1
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.cache' + thread)
            shutil.rmtree(path)

for thread in range(1, THREAD_AMOUNT + 1):
    thread = str(thread)
    try:
        _thread.start_new_thread(scrape_pictures, (thread,))
    except:
        print('Error starting thread ' + thread)
print('Succesfully started ' + thread + ' threads.')

while not done:
    pass