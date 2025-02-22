"""
    MoinMoin - Blog macro

    version 1.0-Beta

    (c) 2003 Mark Proctor, athico.com
    Licensed under GNU GPL - see COPYING for details.

    ----
    Overview:

    This is a simply Blog macro that utilises a javascript calendar and the Include macro to hack together a pseudo bwiki (blog/wiki).
    The calendar is used to choose the entries to show, the number of visible entries is controlled by the select control "max entries".
    The button to the left of "max entries" allows you to toggle between the two modes "Show All" and "Show Published".
     *  "Show Published" only shows those days that contain entries up to the given "max entries", from the chosen calendar date.
     *  "Show All" Show all the dates, previous to the chosen calendar date, up to a maximum of "max entries".
     This is the mode you  will need to use to enter new  blog entries

    Dependencies
     * Include

    To install:
     * Save this macro in your macros directory

    To Use:
     * <date>       : in the format of yyyy-mm-dd
     * <showAll>    : 1 or 0, where 1 shows all and 0 shows published
     * <entries>    : the maximum visible number of entries
     * <maxEntries> : the maximum value that <entries> can be, this is used to restrict the web gui
     * <startDay>   : The start Day for the calendar
      * values      : "Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"


    defaults:
     * <date>      : today
     * <showAll>   : 0
     * <entries>   : 5
     * <maxEntries>: 20
     * <startDay>  : 'Mo'

    [[Blog[<date>, <showAll>, <entries>, <maxEntries>
    [[Blog(, 1, 7)]] - Shows all days, up to 7 days, from todays date.
    [[Blog(2003-05-23, 0, 5)]] - Shows upto 5 published entries from the given date.
    [[Blog( , , , 10)]] - Shows upto 5(default) published(default) entries from todays date(default), but does not allow the user to speficy max entries to be more than 10.
    [[Blog( , , , , We)]] - Shows upto 5(default) published(default) entries from todays date(default), maxEntries(20) with start calendar  day Wednesday.
    [[Blog(2003-05-23, 0, 5, ,Sa)]] - Shows upto 5 published entries from the given date, with start calendar day Saturday

    $Id$
"""

from MoinMoin import config, wikiutil
from MoinMoin.Page import Page
import re, time, string
import MoinMoin.macro.Include
import os.path

def getStyle():
    style = """
<style type="text/css">
    .calendarButton {
        font-size:10;
        cursor:pointer;
        cursor:hand;
    }

    .calendarHeader {
        background-color:#C0DED1;
        font-size:12;
        text-decoration:none;
        cursor:pointer;
        cursor:hand;
    }

    .calendarValue {
        background-color:#FDFAD1;
        font-size:10;
        font-color:black;
        cursor:pointer;
        cursor:hand;
    }

    .calendarValueSelected {
        background-color:#FD0000;
        font-size:10;
        font-color:black;
        cursor:pointer;
        cursor:hand;
    }
</style>
"""

    return style

def getJavascript(page, date, entries, showAll, startDay):
    javascript = """
<script>

var global = {};
global.page = "%s";
global.date = "%s";
global.entries = "%s";
global.showAll = "%s";

global.daysLookup = {"Su":0, "Mo":1, "Tu":2, "We":3, "Th":4, "Fr":5, "Sa":6};
global.days = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
global.startDay = "%s";

function gotoDate() {
    if (!this.date) return;
    global.date = this.date;
    updateBlog();
}

function updateBlog() {
    window.location.href = "/"+global.page+"?date="+global.date+"&entries="+global.entries+"&showAll="+global.showAll
}

function setToday() {
    var now   = new Date();
    var day   = now.getDate();
    var month = now.getMonth();
    var year  = now.getYear();
    if (year < 2000)    // Y2K Fix, Isaac Powell
    year = year + 1900; // http://onyx.idbsu.edu/~ipowell
    this.focusDay = day;
    document.calControl.month.selectedIndex = month;
    document.calControl.year.value = year;
    updateCalendar(month, year);
}

function isFourDigitYear(year) {
    if (year.length != 4) {
        alert ("Sorry, the year must be four-digits in length.");
        document.calControl.year.select();
        document.calControl.year.focus();
        return false;
    } else {
        return true;
    }
}

function selectDate() {
    var year  = document.calControl.year.value;
    if (isFourDigitYear(year)) {
        var day   = 0;
        var month = document.calControl.month.selectedIndex;
        updateCalendar(month, year);
    }
}

function setPreviousYear() {
    var year  = document.calControl.year.value;
    if (isFourDigitYear(year)) {
        var day   = 0;
        var month = document.calControl.month.selectedIndex;
        year--;
        document.calControl.year.value = year;
        updateCalendar(month, year);
   }
}
function setPreviousMonth() {
    var year  = document.calControl.year.value;
    if (isFourDigitYear(year)) {
        var day   = 0;
        var month = document.calControl.month.selectedIndex;
        if (month == 0) {
            month = 11;
            if (year > 1000) {
                year--;
                document.calControl.year.value = year;
            }
        } else {
            month--;
        }
        document.calControl.month.selectedIndex = month;
        updateCalendar(month, year);
   }
}
function setNextMonth() {
    var year  = document.calControl.year.value;
    if (isFourDigitYear(year)) {
        var day   = 0;
        var month = document.calControl.month.selectedIndex;
        if (month == 11) {
            month = 0;
            year++;
            document.calControl.year.value = year;
        } else {
            month++;
        }
        document.calControl.month.selectedIndex = month;
        updateCalendar(month, year);
   }
}
function setNextYear() {
    var year = document.calControl.year.value;
    if (isFourDigitYear(year)) {
        var day = 0;
        var month = document.calControl.month.selectedIndex;
        year++;
        document.calControl.year.value = year;
        updateCalendar(month, year);
   }
}

function makeCalendar() {
    var cal = document.getElementById("calendarTbody");
    if (cal) return;
    var i;
    var table = document.createElement("table");
    table.style.cssText = "border-left:1px solid black; border-top:1px solid black";
    table.cellSpacing = 0;
    table.cellPadding = 2;
    var thead = document.createElement("thead");

    var cell;
    var row = document.createElement("tr");

    var titleDays = [];
    var startDay = global.daysLookup[global.startDay];

    for (i=startDay;i<7;i++) {
        titleDays.push(global.days[i]);
    }

    for (i=0;i<startDay;i++) {
        titleDays.push(global.days[i]);
    }

    for  (i=0;i<titleDays.length;i++) {
        cell = document.createElement("td");
        cell.style.cssText = "border-right:1px solid black; border-bottom:1px solid black";
        cell.className = "calendarHeader";
        cell.innerHTML =  titleDays[i];
        row.appendChild(cell);
    }
    thead.appendChild(row);
    table.appendChild(thead);

    var tbody = document.createElement("tbody");
    tbody.id = "calendarTbody";
    row = document.createElement("tr");
    for (i=0; i<42; i++)  {
        if ( i%%7 == 0 ) { //start new line
            tbody.appendChild(row);
            row = document.createElement("tr");
        }
        cell = document.createElement("td");
        cell.className = "calendarValue";
        cell.style.cssText = "border-right:1px solid black; border-bottom:1px solid black";
        cell.innerHTML = "&nbsp;";
        cell.date = null;
        cell.onclick = gotoDate
        row.appendChild(cell);
    }
    tbody.appendChild(row);
    table.appendChild(tbody);

    var  calendar = document.getElementById("calendar");
    calendar.appendChild(table);
}

function updateCalendar(month, year) {
    month = parseInt(month);
    year = parseInt(year);
    var i = 0;
    var days = getDaysInMonth(month+1,year);
    var startDay = global.daysLookup[global.startDay];
    var firstOfMonth = new Date (year, month, 1).getDay();
    var startingPos =  (firstOfMonth >= startDay) ? firstOfMonth - startDay : 7 - (startDay - firstOfMonth);
    days += startingPos;

    var cal = document.getElementById("calendarTbody");

    var cells = cal.getElementsByTagName("td");
    var cell;
    for (i = 0; i < startingPos; i++) {
        cell = cells[i];
        cell.innerHTML = "&nbsp;";
        cell.date = null;
        cell.className = "calendarValue";
    }

    var value;
    month++;
    if (month<10) month = "0" + month;
    date = year+"-"+month+"-";
    for (i = startingPos; i < days; i++) {
        cell = cells[i];
        value = "";
        value = i-startingPos+1;
        if (value < 10) value = "0" + value;
        cell.date = year+'-'+(month)+'-'+value;
        cell.innerHTML = value;
        if (global.date != date+value) cell.className = "calendarValue";
        else cell.className = "calendarValueSelected";
    }

    for (i = days; i < 42; i++) {
        cell = cells[i];
        cell.date = null;
        cell.className = "calendarValue";
        cell.innerHTML = "&nbsp;";
    }
}

function getDaysInMonth(month,year)  {
    var days;
    if (month==1 || month==3 || month==5 || month==7 || month==8 || month==10 || month==12)  days=31;
    else if (month==4 || month==6 || month==9 || month==11) days=30;
    else if (month==2)  {
        if (isLeapYear(year)) { days=29; }
        else { days=28; }
    }
    return (days);
}

function isLeapYear (Year) {
    if (((Year %% 4)==0) && ((Year %% 100)!=0) || ((Year %% 400)==0)) {
    return (true);
    } else { return (false); }
}
</script>
""" % (page, date, entries, showAll, startDay);

    return javascript

def getCalendar():
    calendar = """

<FORM NAME="calControl" onsubmit="return false;" >
<TABLE CELLPADDING=0 CELLSPACING=0 BORDER=0 >
<TR><TD>
<CENTER>
<SELECT class="calendarButton" NAME="month" onchange="selectDate()">
<OPTION>January
<OPTION>February
<OPTION>March
<OPTION>April
<OPTION>May
<OPTION>June
<OPTION>July

<OPTION>August
<OPTION>September
<OPTION>October
<OPTION>November
<OPTION>December
</SELECT>
<INPUT NAME="year" class="calendarButton" TYPE=TEXT SIZE=4 MAXLENGTH=4>
<INPUT TYPE="button" class="calendarButton" NAME="Go" value="Update Year" onClick="selectDate()">
</CENTER>
</TD>
</TR>
</FORM>
<FORM NAME="calButtons">
<TR><TD id="calendar" align="center" onsubmit="return false;" >

</TD><TR><TD><CENTER>
<INPUT class='calendarButton' TYPE=BUTTON NAME="previousYear" VALUE=" <<  "    onClick="setPreviousYear()">
<INPUT class='calendarButton' TYPE=BUTTON NAME="previousYear" VALUE="  <  "    onClick="setPreviousMonth()">
<INPUT class='calendarButton' TYPE=BUTTON NAME="previousYear" VALUE="Today"    onClick="setToday()">
<INPUT class='calendarButton' TYPE=BUTTON NAME="previousYear" VALUE="  >  "    onClick="setNextMonth()">
<INPUT class='calendarButton' TYPE=BUTTON NAME="previousYear" VALUE="  >> "    onClick="setNextYear()">
</CENTER></TD></TR>
</TABLE></FORM>
<script>
 onload=function() {
    var date = global.date.split("-");
    document.calControl.month.selectedIndex = date[1]-1;
    document.calControl.year.value = date[0];
    makeCalendar();
    updateCalendar(date[1]-1, date[0]);
 };
</script>
"""
    return calendar

#def execute(macro, text, args_re=re.compile(_args_re_pattern)):

def execute(macro, text):
    thisPage = macro.formatter.page.page_name


    #get incoming macro args, else set to []
    if text:
        args = string.split(text, ",")
    else:
        args = []

    #remove all leading and trailing spaces
    for i in range(len(args)):
        args[i] = string.strip(args[i])

    #set date
    if macro.form.has_key('date'):
        date = macro.form['date'].value
    elif (len(args) >= 0) and (not args[0] == ""):
        date = args[0]
    else:
        date = ""


    #set showAll
    if macro.form.has_key('showAll'):
        showAll = macro.form['showAll'].value
    elif (len(args) >= 1) and (not args[1] == ""):
        showAll = args[1]
    else:
        showAll = "0"

    #set entries
    if macro.form.has_key('entries'):
        entries = macro.form['entries'].value
    elif (len(args) >= 2) and (not args[2] == ""):
        entries = args[2]
    else:
        entries = -1

    #set max entries
    if (len(args) >= 3) and (not args[3] == ""):
        maxEntries = int(args[3])
        if maxEntries < 0:
            maxEntries = 20
    else:
        maxEntries = 20

    if (len(args) >= 4) and (not args[4] == ""):
        startDay = args[4]
    else:
        startDay = "Mo";


    #set the number of visible entries
    if not entries == -1:
        args_re=re.compile(r'(?P<entries>\d+)')
        args = args_re.match(entries)
        if not args:
            return ('<p><strong class="error">%s</strong></p>' %('Invalid entries "%s"!')) % (macro.form['beforeDate'].value)
        entries = int(macro.form['entries'].value)
        if entries > maxEntries:
            entries = maxEntries
        if entries < 0:
            entries = 5
    else:
        entries = 5

    #get the date
    if not date == "":
        args_re=re.compile(r'(?P<year>\d\d\d\d)-(?P<month>\d?\d)-(?P<day>\d?\d)')
        args = args_re.match(date)
        if not args:
            return ('<p><strong class="error">%s</strong></p>' %('Invalid date "%s"!')) % (macro.form['date'].value)
        year  = int(args.group('year'))
        month = int(args.group('month'))
        day   = int(args.group('day'))
    else:
        datetofind = time.time()
        (year,month,day,h,m,s,wd,yd,ds) = time.localtime(datetofind)

    ret  = getStyle()
    ret += getJavascript(thisPage, "%d-%02d-%02d" % (year, month, day), entries, showAll, startDay)
    ret += getCalendar()

    #get the entries to display
    if (showAll == '1'):
        ret += getShowAll(macro, thisPage, year, month, day, entries, maxEntries)
    else:
        ret += getShowEntered(macro, thisPage, year, month, day, entries, maxEntries)

    return ret

def getShowAll(macro, thisPage,  year, month, day, entries, maxEntries):
    ret = "<input class='calendarButton' type=button value='Show Published' onclick='global.showAll=0;updateBlog();'>"

    ret += " max entries: <select class='calendarButton' onchange='if (this.value&&(this.value != \"\")) {global.entries=this.value; updateBlog();}'>"
    ret += "<option value=''>--Entries--</option>"
    for i in range(maxEntries):
        if (i==entries-1):
            ret += "<option selected value='"+str(i+1)+"'>"+str(i+1)+"</value>"
        else:
            ret += "<option value='"+str(i+1)+"'>"+str(i+1)+"</value>"
    ret += "</select>"

    for i in range(entries):
        includeParams = '%s/BlogEntry-%d-%02d-%02d, "%d-%02d-%02d", 1' % (thisPage, year, month, day, year, month, day)
        ret += MoinMoin.macro.Include.execute(macro, includeParams)
        #date = strftime("%Y-%m-$d", (year,month,day, 0, 0, 0, 0, 0, 0)
        day = day - 1
        date = time.mktime((year,month,day, 0, 0, 0, 0, 0, 0))
        (year,month,day,h,m,s,wd,yd,ds) = time.localtime(date)
    return ret

def getShowEntered(macro, thisPage, year, month, day, entries, maxEntries):
    ret = "<input class='calendarButton' type=button value='Show All' onclick='global.showAll=1;updateBlog();'>"
    ret += " max entries: <select class='calendarButton' onchange='if (this.value&&(this.value != \"\")) {global.entries=this.value; updateBlog();}'>"
    ret += "<option value=''>--Entries--</option>"
    for i in range(maxEntries):
        if (i==entries-1):
            ret += "<option selected value='"+str(i+1)+"'>"+str(i+1)+"</value>"
        else:
            ret += "<option value='"+str(i+1)+"'>"+str(i+1)+"</value>"
    ret += "</select>"
    return ret
    #pages = wikiutil.getPageList(config.text_dir)
    #fname = os.path.join(macro.request.cfg.data_dir, "pages", macro.formatter.page.page_name)
    #pages = macro.formatter.page.getPageList(fname)
    displayPages = []
    for page_name in pages:
        if re.match('^' + thisPage + '/', page_name):
            displayPages.append(page_name)

    displayPages.sort()
    displayPages.reverse()
    selectedDate = int( "%d%02d%02d" % (year, month, day))
    pages = 0
    for pageName in displayPages:
        pageDate = int(pageName[-10:-6] + pageName[-5:-3] + pageName[-2:])
        if (pageDate <= selectedDate):
            pages = pages + 1
            includeParams = pageName + ', "%s-%s-%s", 1' % (pageName[-10:-6], pageName[-5:-3], pageName[-2:])
            ret += MoinMoin.macro.Include.execute(macro, includeParams)
            if (pages  >= entries):
                break
    return ret

