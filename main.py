#Credits to 'nazarpechka' for helping out with this code

import string, random, os, sys, _thread, httplib2, time
# from PIL import Image

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python3 " + sys.argv[0] + " (Number of threads)")
THREAD_AMOUNT = int(sys.argv[1])

INVALID = [0, 503, 5082, 4939, 4940, 4941, 12003, 5556]
countOfPictures = 0
def scrape_pictures(thread):
    while True:
        global countOfPictures
        url = 'http://i.imgur.com/'
        length = random.choice((5, 6))
        if length == 5:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        else:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
            url += ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
        url += '.jpg'
        # print (url)

        filename = url.rsplit('/', 1)[-1]
        # print (filename)

        h = httplib2.Http('.cache' + thread)
        response, content = h.request(url)
        response = h.request(url)[0]
        if response.status == 200:
            out = open('pcs/' + filename, 'wb')
            out.write(content)
            out.close()

            file_size = os.path.getsize('pcs/' + filename)
            if file_size in INVALID:
                #print(str(response.status) + "[-] Invalid: " + url)
                os.remove('pcs/' + filename)
            else:
                countOfPictures += 1
                if countOfPictures >= 10:
                    print('done' + str(_thread.get_ident()))
                    sys.exit()
                #print(str(response.status) + " [+] Valid: " + url)

for thread in range(1, THREAD_AMOUNT + 1):
    thread = str(thread)
    try:
        _thread.start_new_thread(scrape_pictures, (thread,))
    except:
        print('Error starting thread ' + thread)
print('Succesfully started ' + thread + ' threads.')

while True:
    time.sleep(1)