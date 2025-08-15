import os, re

def formatURLs(str):
    newStr = str
    # Probably far to complex regex for finding urls
    urls = re.findall(r"#(.*?)#", str)
    for url in urls:
        newStr = newStr.replace(url, '<a href="' + url + '">' + url + "</a>").replace('#', '')
    return newStr

monthDict = { 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12' }

for file in os.listdir('./temp/speakersWorkfiles'):
    with open('./temp/speakersWorkfiles/' + file, encoding='utf8') as f:
#with open('./temp/speakersWorkfiles/Fall2018.txt', encoding='utf8') as f:
        term = file[:-8] + ' ' + file[-8:-4]
        lines = f.readlines()
        f.close()
        output = []
        i = 0
        while i < len(lines):
            with open('./temp/NewTalkInfo/' + (lines[i+1].strip() + '-' + lines[i].strip()).replace(' ', '') + '.txt', 'w', encoding='utf8') as f:
                f.write('Term: ' + term + '\n')
                f.write('Date: ' + lines[i])
                i += 1
                f.write('Speaker: ' + lines[i])
                i += 1
                f.write('School: ' + lines[i])
                i += 1
                f.write('Title: ' + lines[i])
                i += 1
                f.write('YouTube: ' + lines[i])
                i += 1
                if lines[i].strip() != '':
                    f.write('Slides: ' + lines[i].strip() + '-' + term[-4:] + '-' + monthDict[lines[i-5].strip()[:3]] + '-' + ('0' + lines[i-5].strip()[-2:].strip())[-2:] + '-HoTTEST.pdf\n')
                else:
                    f.write('Slides:\n')
                i += 1
                f.write('Abstract: ' + formatURLs(lines[i].replace('>', '&gt;')))
                i += 1
                while i < len(lines) and lines[i].strip() != '':
                    f.write(formatURLs(lines[i].replace('>', '&gt;')))
                    i += 1
                i += 1
                f.close()