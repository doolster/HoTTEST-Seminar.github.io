fetch("SpeakerData.txt")
.then((res) => res.text())
// Run all code inside the ".then" so we can modify the content that is being added asynchonously (there's probably a better way to do this...)
.then((rawText) => {
  var lines = rawText.split('\n');
  if (lines[0].substring(0, 6) != "Term: ") {
    console.log("SpeakerData.txt not formatted correctly on line 0");
  };
  var newAcc;
  var newPanel;

  var newTable;
  var newTr;
  var newDateTh;
  var newSpeakerTh;
  var newTalkTh;

  var newDate;
  var newSpeaker;
  var newTd;
  var newTalkTitle;
  var newYTLink;
  var newSlideLink;
  var newIcon;
  var newAbst;
  var newLink;
  for (i = 0; i < lines.length; i++) {
    switch (true) {
      // Append the last accordion and panel and create a new one to be filled
      case (lines[i].substring(0, 6) == "Term: "):
        if (newAcc) {
          document.body.appendChild(newAcc);
          document.body.appendChild(newPanel);
        }
        newAcc = document.createElement("button");
        newAcc.classList.add('accordion');
        newAcc.textContent = lines[i].substring(6);
        newPanel = document.createElement('div');
        newPanel.classList.add('panel');
        newTable = document.createElement('table');
        newTr = document.createElement('tr');
        newDateTh = document.createElement('th');
        newDateTh.textContent = 'Date';
        newSpeakerTh = document.createElement('th');
        newSpeakerTh.textContent = 'Speaker';
        newTalkTh = document.createElement('th');
        newTalkTh.textContent = 'Talk Information';
        newPanel.appendChild(newTable);
        newTable.appendChild(newTr);
        newTr.appendChild(newDateTh);
        newTr.appendChild(newSpeakerTh);
        newTr.appendChild(newTalkTh);
        i++;
        break;
      case (lines[i].substring(0, 6) == "Date: "):
        newTr = document.createElement('tr'); // Only create new tr element with date
        newDate = document.createElement('td');
        newDate.classList.add('date');
        newDate.textContent = lines[i].substring(6);
        newTr.appendChild(newDate);
        break;
      case (lines[i].substring(0, 9) == "Speaker: "):
        newSpeaker = document.createElement('td');
        newSpeaker.classList.add('speaker');
        newSpeaker.textContent = lines[i].substring(9);
        newTr.appendChild(newSpeaker);
        break;
      case (lines[i].substring(0, 7) == "Title: "):
        newTd = document.createElement('td')
        newTalkTitle = document.createElement('p');
        newTalkTitle.classList.add('talk-title');
        newTalkTitle.textContent = lines[i].substring(7);
        newTd.appendChild(newTalkTitle);
        break;
      case (lines[i].substring(0, 13) == "YouTube_Link:"):
        if (lines[i].substring(14) != "") {
          newYTLink = document.createElement('a');
          newYTLink.href = lines[i].substring(14);
          newIcon = document.createElement('img');
          newIcon.classList.add('icon');
          newIcon.src = "images/YouTube icon.webp";
          newYTLink.appendChild(newIcon);
          newTalkTitle.appendChild(newYTLink);
        }
        break;
      case (lines[i].substring(0, 12) == "Slides_Link:"):
        if (lines[i].substring(13) != "") {
          newSlideLink = document.createElement('a');
          newSlideLink.href = lines[i].substring(13);
          newIcon = document.createElement('img');
          newIcon.classList.add('icon');
          newIcon.src = "images/PDF_file_icon.png";
          newSlideLink.appendChild(newIcon);
          newTalkTitle.appendChild(newSlideLink);
        }
        break;
      case (lines[i].substring(0, 10) == "Abstract: "):
        newAbst = document.createElement('p');
        newAbst.classList.add('abstract');
        newAbst.textContent = lines[i].substring(10);
        break;
      case (lines[i].substring(0, 4) == "    "):
        //if (lines[i].trim().substring(0, 4) == "http") {
        //  newLink = document.createElement('a');
        //  newLink.href = lines[i].trim();
        //  newLink.textContent = lines[i];
        //  newAbst.appendChild(newLink);
        //} else {
          newAbst.appendChild(document.createElement('br'))
          newAbst.textContent += ("\n" + lines[i]);
        //}
        break;
      case (lines[i] == ""):
        newTd.appendChild(newAbst);
        newTr.appendChild(newTd);
        newTable.appendChild(newTr);
        break;
      default:
        console.log("Unexpected formatting in SpeakerData.txt on line " + (i + 1));
    }
  }
  document.body.appendChild(newAcc);
  document.body.appendChild(newPanel);


// Places 'Past Talks' header after first accordion menu
const pastTalks = document.createElement('h2');
pastTalks.textContent = 'Past Talks';
document.querySelector('.panel').insertAdjacentElement('afterend', pastTalks);


// Accordion animation
var acc = document.getElementsByClassName('accordion');
var i;
for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener('click', function() {
    this.classList.toggle('active');
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + 'px';
    } 
  });
}

// Show More/Less for last column
document.querySelectorAll('.panel table').forEach(function(table) {
  // For each row except the header
  table.querySelectorAll('tr').forEach(function(row, idx) {
    // Skip header row
    if (idx === 0) return;
    let cells = row.querySelectorAll('td');
    if (cells.length === 0) return;
    let lastCell = cells[cells.length - 1];
    if (!lastCell.classList.contains('show-more-processed')) {
        lastCell.classList.add('show-more-processed');
        let abst = lastCell.querySelector('.abstract');
        // Make title into a button
        let btn = lastCell.querySelector('.talk-title')
        let img = new Image(10, 10);
        img.src = 'images/expand-button.png';
        img.style.marginInlineEnd = '5px';
        btn.insertAdjacentElement('afterbegin', img);
        btn.addEventListener('click', function() {
          let expanded = abst.classList.toggle('expanded');
          img.src = expanded ? 'images/retract-button.png' : 'images/expand-button.png';
          // Update panel height if inside accordion
          let panel = lastCell.closest('.panel');
          if (panel) {
              requestAnimationFrame(function() {
                  panel.style.maxHeight = panel.scrollHeight + "px";
              });
            }
        });
    }
    });
});

// Stops icons from expanding abstract
function stopEvent(event) { event.stopPropagation(); }
document.querySelectorAll('.icon').forEach(function(icon) {
  icon.addEventListener('click', stopEvent, false);
});

// Opens first accordion on start
var firstPanel = document.getElementsByClassName('panel')[0];
firstPanel.style.maxHeight = firstPanel.scrollHeight + 'px';
document.getElementsByClassName('accordion')[0].classList.toggle('active');

// Opens first 'Show More' button on start
var firstBtn = document.querySelector('.talk-title');
if (firstBtn) {
    var abst = document.querySelector('.abstract');
    if (abst && abst.classList) {
        abst.classList.add('expanded');
        firstBtn.childNodes[0].src = 'images/retract-button.png';
        // Update panel height if inside accordion
        let panel = firstBtn.closest('.panel');
        if (panel) {
            requestAnimationFrame(function() {
                panel.style.maxHeight = panel.scrollHeight + "px";
            });
        }
    }
}

// "Expand All" button functionality
document.getElementById('expand-all-btn').addEventListener('click', function() {
  for (i = 0; i < acc.length; i++) {
    if (!acc[i].classList.contains('active')) {
      var accPanel = acc[i].nextElementSibling;
      accPanel.style.maxHeight = accPanel.scrollHeight + 'px';
      acc[i].classList.toggle('active');
    }
  }
});

// Sets all links to "noreferrer"
document.querySelectorAll('a').forEach((el) => {
    el.setAttribute('rel', 'noreferrer');
});

})
.catch((e) => console.error(e));
