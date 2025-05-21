import pdfcrowd
import sys  ,os    
MYDIR = os.path.dirname(__file__)

try:
    # create the API client instance
    client = pdfcrowd.HtmlToPdfClient('Aristideoued', '37b6a3e765beb602fabe6a230374ba22')

    # run the conversion and write the result to a file
    client.convertUrlToFile('https://ecvback.codingagain.com/user/cv?id=15', MYDIR+'/result.pdf')
    #return send_file(MYDIR+"/result.pdf", as_attachment=True)

except pdfcrowd.Error as why:
    # report the error
    sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

    # rethrow or handle the exception
    raise
