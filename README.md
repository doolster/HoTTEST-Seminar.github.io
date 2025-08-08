<h2>EXAMPLE OF CORRECT FORMATTING FOR TALK FILES</h2>

Term: TERM YYYY<br>
Date: MON DD<br>
Speaker: SPEAKER NAME<br>
Title: TALK TITLE<br>
YouTube: YOUTUBE LINK<br>
Slides: SLIDE LINK<br>
Abstract: ABSTRACT CONTENT<br>
ABSTRACT CONTENT<br>
...<br>


(new talk files should be added to the TalkInfo folder)<br>
NOTES:
<ul>
  <li>TERM should be either "Spring" or "Fall" for regular sessions, special terms can be added (such as the Jr. Researcher Event), but a corresponding entry must be added to termIDDict in indexGenerator.py for sorting purposes.</li>
  <li>YYYY is the year, although only the last two digits are used for sorting.</li>
  <li>MON should be the shortened form of the month (Jan, Sept, etc. this is just for consistency purposes, as long as MON starts with the correct three letters it will be sorted correctly).</li>
  <li>DD is the day, if it is a single digit, make sure there is a space between MON and DD.</li>
  <li>TALK TITLE is the title of the talk.</li>
  <li>YOUTUBE LINK and SLIDE LINK are the relevant links, these are the only entries which are okay to leave empty.</li>
  <li>ABSTRACT CONTENT is the abstract, which should be split into lines for the desired paragraph breaks. The abstract can be as long as you would like, but it must always be the last entry.</li>
  <li>HTML can be added to ABSTRACT CONTENT and will be rendered correctly, such as, if you want to include a hyperlink.</li>
</ul>

THINGS THAT WILL AFFECT PAGE GENERATION (indexGenerator.py will throw an exception):
<ul>
  <li>Misspelled line starters</li>
  <li>Improperly formatted term or date entries</li>
  <li>Missing entries (other than youtube/pdf links)</li>
  <li>"Abstract:" not being the last entry (the exception that will show up in this case is for missing entries of whatever was below "Abstract:")</li>
</ul>

THINGS THAT WILL _NOT_ AFFECT PAGE GENERATION:
<ul>
  <li>File name</li>
  <li>Whitespace differences (either before or after lines, or between entry label and content)</li>
  <li>Capitolization</li>
  <li>Missing youtube/slide links</li>
  <li>Ordering of entries (besides "Abstract:" which must go last)</li>
</ul>
