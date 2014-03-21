'''
Created on 20 mrt. 2014

@author: Pieter
'''
import practicumbank
from practicumbank import CloudConvert

def main():
    apikey = practicumbank.CLOUDCONVERT_API_KEY

    process = CloudConvert.ConversionProcess(apikey)

    # This should autodetect file extension. if not, you can
    # always set process.fromformat and .toformat to the correct
    # values
    process.init("test.docx", "test.pdf")
    process.start()
    # Will block until file is done processing. You can set
    # the interval between checks.
    process.wait_for_completion(check_interval=5)

    # Returns a file-like obj to download the processed file
    download = process.download()

    with open("test.pdf", "wb") as f:  # Important to set mode to wb
        f.write(download.read())
if __name__=="__main__":
    main()