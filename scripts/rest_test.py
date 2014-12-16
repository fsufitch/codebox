import requests, sys, time

def main():
    apiurl = sys.argv[1]
    filename = sys.argv[2]
    
    files = {'upload': open(filename, 'rb')}
    
    jobsubmit = requests.post(apiurl+'job/new', files=files)
    job_id = jobsubmit.json()['job_id']

    while True:
        jobget = requests.get(apiurl+'job/get/'+job_id)
        data = jobget.json()
        if data['run_done']:
            print(data['run_result'])
            break
        else:
            #print("Not yet done...")
            time.sleep(1)

if __name__=='__main__':
    main()
