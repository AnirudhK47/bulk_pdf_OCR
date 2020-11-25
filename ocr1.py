'''
2020-11-24
Program to bulk OCR scanned/image PDFs into textual PDFs
Original program by PG Bhat, some modifications by Nikhil VJ, https://answerquest.github.io/

Install these first:
sudo apt install tesseract-ocr libtesseract-dev ghostscript
pip3 install pytesseract==0.3.4 ocrmypdf==9.7.2

Mention all input folders in "acFolders" list, keep them in same location as this program.
Outputs will be in new folders with "out_" prefix.
You can interrupt the program and resume later - it will pick up where it left off.
'''

import os
import ocrmypdf
import datetime
import time

root = os.path.dirname(__file__)


def logmessage( *content ):
    timestamp = '{:%Y-%m-%d %H:%M:%S} :'.format(datetime.datetime.now()) # from https://stackoverflow.com/a/26455617/4355695
    line = ' '.join(str(x) for x in list(content))
    # str(x) for x in list(content) : handles numbers in the list, converts them to string before concatenating. # from https://stackoverflow.com/a/3590168/4355695
    print(line) # print to screen also
    with open('log.txt', 'a', newline='\r\n', encoding='utf8') as f: #open in append mode
        print(timestamp, line, file=f) # `,file=f` argument at end writes the line, with newline as defined, to the file instead of to screen. from https://stackoverflow.com/a/2918367/4355695
    # f.close()


def files2process(src_dir, tgt_dir) -> list:
    processed = [os.path.splitext(file)[0] for file in os.listdir(tgt_dir)]
    to_process = [os.path.join(src_dir,file) for file in os.listdir(src_dir) if not os.path.splitext(file)[0] in processed]
    return to_process


if __name__ == '__main__':

    acFolders = ['AC156', 'AC157', 'AC158', 'AC159', 'AC160', 'AC161', 'AC162', 'AC163', 'AC164', 'AC165']
    for oneFolder in acFolders:
        logmessage('-'*50)
        logmessage(oneFolder)
        in_dir = os.path.join(root,oneFolder)
        out_dir = os.path.join(root,f'out_{oneFolder}')

        # os.makedirs(in_dir, exist_ok=True)
        os.makedirs(out_dir, exist_ok=True)

        start = time.time()
        files = files2process(in_dir, out_dir)

        for f_in in files:
            logmessage(f"Processing {f_in}")
            f_out = os.path.join(out_dir, os.path.basename(f_in))

            ocrmypdf.ocr(f_in, f_out, deskew=True) # MAIN STUFF HAPPENING HERE!

            logmessage(os.path.basename(f_in)[:-4])

        logmessage(f'\n{len(files)} done; time taken: {round(time.time() - start,2)} seconds.')

 