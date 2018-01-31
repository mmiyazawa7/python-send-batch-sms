# For Python 3.5

#!/usr/bin/python
# coding=utf-8

import csv
import sys
import getopt
import requests
import ratelimiter
import datetime

# SETTINGS
SENDER_ID = ''
CALLBACK_URL = ''


def main(argv):
    api_key = ''
    api_secret = ''
    infile = ''
    outfile = ''

    try:
        opts, args = getopt.getopt(
            argv, "hk:s:i:o:", ["api_key", "secret_key", "infile", "outfile"])
    except getopt.GetoptError:
        print('SendMassSMS.py -k <api_key> -s <api_secret> -i <infile> -o <outfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('SendMassSMS.py -k <api_key> -s <api_secret> -i <infile> -o <outfile>')
            sys.exit()
        elif opt in ("-k", "--api_key"):
            api_key = arg
        elif opt in ("-s", "--api_secret"):
            api_secret = arg
        elif opt in ("-i", "--infile"):
            infile = arg
        elif opt in ("-o", "--outfile"):
            outfile = arg

    sendmasssms(api_key=api_key, api_secret=api_secret, infile=infile, outfile=outfile)


def sendmasssms(api_key, api_secret, infile, outfile):
    with open(infile) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=';')
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, dialect=dialect)
        with open(outfile, 'w') as csvfile2:
            spamwriter = csv.writer(csvfile2, delimiter=';')
            spamwriter.writerow(['timestamp', 'telephone', 'message', 'messageid', 'status'])

            # x call per x seconds - Do not exceed 25 calls per seconds
            rate_limiter = ratelimiter.RateLimiter(max_calls=25, period=1)

            for row in reader:
                # print(row)
                messageTXT = row['message'] + " STOP au 36179"
                with rate_limiter:
                    params = {
                        'api_key': api_key,
                        'api_secret': api_secret,
                        'to': row['telephone'],
                        'from': SENDER_ID,
                        'text': messageTXT,
                        'type': 'text',
                        'client-ref': SENDER_ID,
                        'callback': CALLBACK_URL
                    }

                    response = requests.get('https://rest.nexmo.com/sms/json?', params=params)

                    # Error handling

                    # Check for HTTP codes other than 200
                    if response.status_code != 200:
                        print('Status:', response.status_code,
                              ' unexpected response from Nexmo api')
                        exit()

                    # Decode the JSON response into a dictionary and use the data
                    data = response.json()
                    # print(data)

                    status = data['messages'][0]['status']
                    msg_count = data['message-count']
                    msg_id = data['messages'][0]['message-id']
                    # print(status)
                    # print(msg_count)

                    time_stamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
                    telephone = row['telephone']
                    spamwriter.writerow([time_stamp, telephone, messageTXT, msg_id, status])


if __name__ == "__main__":
    main(sys.argv[1:])
