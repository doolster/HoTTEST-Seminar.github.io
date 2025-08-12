from yattag import Doc, indent
import os, re

# Any new term types must be added to this dictionary for sorting
termIDDict = { 'Spring': 'b', 'Fall': 'd', 'HoTTEST Event For Junior Researchers': 'a', 'HoTTEST Conference' : 'c'}
monthDict = { 'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6', 'Jul': '7', 'Aug': '8', 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12' }

class Talk:
    def __init__(self, term, date, speaker, school, title, ytlink, slides, abstract):
        self.term = term
        self.termID = ''
        self.date = date
        self.dateID = ''
        self.speaker = speaker
        self.school = school
        self.title = title
        self.ytlink = ytlink
        self.slides = slides
        self.abstract = abstract

# Function for formatting text with urls for html output (UNUSED)
def formatURLs(str):
    newStr = str
    # Probably far to complex regex for finding urls
    urls = re.findall(r"""((?:(?:https|http)?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|org)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|ac)\b/?(?!@)))""", str)
    for url in urls:
        newStr = newStr.replace(url, '<a href="' + url + '">' + url + "</a>")
    return newStr

# Given file name in the folder "TalkInfo", parses file into a Talk objects
def readFile(fileName):
    newTalk = Talk('', '', '', '', '', '', '', '')
    with open('./TalkInfo/' + fileName, encoding='utf8') as f:
        lines = f.readlines()
        f.close()
        lines = [x for x in lines if x.strip()] # Remove blank lines from files
        inAbstract = False
        lineNumber = 0
        for line in lines:
            line = line.strip()
            lineNumber += 1
            if line.lower().startswith('abstract:') or inAbstract:
                line = line.replace('>', '&gt;').replace('<','&lt;') # Replacing characters that will cause problems with html
                if not inAbstract:
                    newTalk.abstract = '<p>' + line[9:].strip() + '</p>'
                    inAbstract = True
                else:
                    newTalk.abstract += '<p>' + line +'</p>'
            elif line.lower().startswith('term:'):
                newTalk.term = line[5:].strip()
                if newTalk.term[:-5] in termIDDict:
                    newTalk.termID = newTalk.term[-2:] + termIDDict[newTalk.term[:-5]]
                else:
                    raise Exception(fileName + ': Term type not found - new term types must be added to termIDDict for sorting')
            elif line.lower().startswith('date:'):
                newTalk.date = line[5:].strip()
                if newTalk.date[:3] in monthDict:
                    newTalk.dateID = monthDict[newTalk.date[:3]] + newTalk.date[-2:]
                else:
                    raise Exception(fileName + ': Date entry ill-formed')
            elif line.lower().startswith('speaker:'):
                newTalk.speaker = line[8:].strip()
            elif line.lower().startswith('school:'):
                newTalk.school = line[7:].strip()
            elif line.lower().startswith('title:'):
                newTalk.title = line[6:].strip()
            elif line.lower().startswith('youtube:'):
                newTalk.ytlink = line[8:].strip()
            elif line.lower().startswith('slides:'):
                newTalk.slides = line[7:].strip()
            elif line == '':
                pass
            else:
                raise Exception(fileName + ': Improperly formatted label in line ' + str(lineNumber) + ' - "' + line + '"')
        return newTalk

# Function for testing if a talk object is missing any critical components
def testTalk(talk):
    if talk.date.strip() == '':
        raise Exception('Talk missing date entry')
    elif talk.term.strip() == '':
        raise Exception('Talk on ' + talk.date + ' missing term entry')
    elif talk.speaker.strip() == '':
        raise Exception('Talk on ' + talk.date + ', ' + talk.term + ' missing speaker name')
    elif talk.title.strip() == '':
        raise Exception('Talk "' + talk.speaker + '-' + talk.date + '" missing talk title')
    elif talk.abstract.strip() == '':
        raise Exception('Talk "' + talk.speaker + '-' + talk.date + '" missing abstract')

# Putting all talks into an array
talks = []
for file in os.listdir('./TalkInfo'):
    if not (file.startswith('.') or file.endswith('~')): # Ignore files with unusual names (system generated, etc.)
        newTalk = readFile(file)
        testTalk(newTalk)
        talks.append(newTalk)

# Labeling talks with their term and date
pageInfo = {}
for talk in talks:
    if talk.termID not in pageInfo:
        pageInfo[talk.termID] = { talk.dateID : [talk] }
    else:
        if talk.dateID not in pageInfo[talk.termID]:
            pageInfo[talk.termID][talk.dateID] = [talk]
        else:
            pageInfo[talk.termID][talk.dateID].append(talk)

# Start creating HTML document
doc, tag, text, line = Doc().ttl()

docHead = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="css/style.css">
<base target="_blank">
<title>HoTTEST</title>
<link rel="icon" type="image/x-icon" href="/images/favicon.svg">
</head>
<body>

<div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-top: 20px;">
    <div style="width: 300px;"></div>
    <h1 style="flex: 1;text-align: center; margin: 0;">HoTTEST</h1>
    <img src="images/Universal Cover.png" alt="Universal Cover of S^1" style="width: 250px;">
</div>
<hr style="border: 1px solid #888ebe;">
<p style="margin-left: auto; margin-right: auto; text-align: center; max-width: 1000px;">
    Homotopy Type Theory Electronic Seminar Talks (HoTTEST) is a series of research talks by leading experts in Homotopy Type Theory. 
    The seminar is open to all, although <strong>familiarity with Homotopy Type Theory will be assumed</strong>. 
    To attend a talk, please follow the instructions below.</p>
<hr style="border: 1px solid #888ebe;">

<h2>Essential Information</h2>
<ul>
    <li><strong>Time: </strong>Alternate Thursdays at 11:30 AM Eastern (60-minute talk + 30-minute discussion).</li>
    <li><strong>Mailing list: </strong><a href="https://groups.google.com/forum/#!forum/hott-electronic-seminar-talks">HoTT Electronic Seminar Talks</a> (for updates).</li>
    <li><strong>Google calendar: </strong><a href="https://calendar.google.com/calendar/embed?src=0a4ik9o5vhkgjlnk6no3ttnuko%40group.calendar.google.com&amp;ctz=America%2FToronto">Seminar Calendar</a>.</li>
    <li><strong>YouTube channel: </strong><a href="https://www.youtube.com/channel/UC-9jDbJ-HegCFuWuam1SfvQ">HoTTEST</a>.</li>
    <li><strong>Organizers: </strong>
        <a href="https://www.cs.cmu.edu/&#126;cangiuli/">Carlo Angiuli</a>, 
        <a href="http://jdc.math.uwo.ca/">Dan Christensen</a>, 
        <a href="https://www.math.uwo.ca/faculty/kapulkin/index.html">Chris Kapulkin</a>, and 
        <a href="https://emilyriehl.github.io/">Emily Riehl</a>.</li>
    <li><strong>Website by: </strong><a href="https://doolster.github.io/">Zack Dooley</a></li>
</ul>

<h2>How to Attend?</h2>
<p>We are using <a href="http://zoom.us">Zoom</a>&#160;for the talks. Please install the software and make at least one test call before joining a talk. To join follow the link:</p>
<p style="text-align: center;"><a data-saferedirecturl="https://www.google.com/url?hl=en&amp;q=https://zoom.us/j/994874377&amp;source=gmail&amp;ust=1516649126192000&amp;usg=AFQjCNHCEHJZSi1kztYapVu1OwD5g_wJQg" href="https://zoom.us/j/994874377">https://zoom.us/j/994874377</a></p>

<div class="expand-all-container">
    <button id="expand-term-btn" class="button expand-all">Expand Terms</button>
    <button id="expand-abst-btn" class="button expand-all">Expand Abstracts</button>
</div>
"""

# Adding the static top of the page to doc (Title to "Expand All" button) (probably a better way to do this)
doc.asis(docHead)

# Loop through pageInfo to generate relevant HTML (sorting in reverse order by term)
termIDs = list(pageInfo.keys())
termIDs.sort(reverse=True)
for termID in termIDs:
    currentTerm = pageInfo[termID] # Dictionary of the current term
    dateIDs = list(currentTerm.keys())
    dateIDs.sort(reverse=True)
    with tag('button', klass='accordion'):
        text(currentTerm[dateIDs[0]][0].term)
    with tag('div', klass='panel'):
        with tag('table'):
            with tag('tr'):
                line('th', 'Date')
                line('th', 'Speaker')
                line('th', 'Talk Information')
            for dateID in dateIDs: # Looping through all talks in the current term and creating entries for them
                for talk in currentTerm[dateID]:
                    with tag('tr'):
                        line('td', talk.date, klass='date')
                        with tag('td', klass='speaker'):
                            text(talk.speaker)
                            if talk.school != '':
                                line('div', talk.school, klass='school')
                        with tag('td'):
                            with tag('p', klass='talk-title'):
                                text(talk.title)
                                if talk.ytlink != '':
                                    with tag('a', href=talk.ytlink):
                                        doc.stag('img', src='images/YouTube icon.webp', klass='icon')
                                if talk.slides != '':
                                    with tag('a', href='hottestfiles/' + talk.slides):
                                        doc.stag('img', src='images/PDF_file_icon.png', klass='icon')
                            with tag('div', klass='abstract'):
                                doc.asis(talk.abstract)

docFoot = """
<script src="js/control.js"></script>

</body>
</html>
"""

# Add static end to doc and write doc to file
doc.asis(docFoot)

with open('index.html', 'w', encoding='utf8') as f:
    f.write(indent(doc.getvalue()))
f.close()
