function displayCalender() {
	var dayOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
		monthOfYear = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
		Calendar = new Date(),
		year = Calendar.getFullYear(),
		month = Calendar.getMonth(),
		today = Calendar.getDate(),
		cal, highlight_start = '<TD WIDTH="30"><TABLE BGCOLOR=D3D3D3><TR><TD WIDTH=20><B><CENTER>',
		highlight_end = '</CENTER></TD></TR></TABLE></B>',
		week_day = 0;
	Calendar.setDate(1); // Start the calendar day at '1'
	Calendar.setMonth(month); // Start the calendar month at now
	// code for calender
	cal = '<TR><TD>';
	cal += '<TABLE CELLPADDING=2><TR>';
	cal += '<TD COLSPAN="' + 7 + '" BGCOLOR="#E3E3E3"><CENTER><B>';
	cal += monthOfYear[month] + '   ' + year + '</B></TD></TR>';
	cal += '<TR>';
	// loops for each day of the week    
	for (i = 0; i < 7; i++) {
		cal += '<TD WIDTH="30">' + dayOfWeek[i] + '</TD>';
	}
	cal += '</TD></TR>';
	cal += '<TR>';
	// fills in the blanks
	for (i = 0; i < Calendar.getDay(); i++) {
		cal += '<TD WIDTH="30">' + '  ' + '</TD>';
	}
	// loops for each day
	for (i = 0; i < 31; i++) {
		if (Calendar.getDate() > i) {
			week_day = Calendar.getDay(); // returns the next day to print
		}
		// starts a new row for new week
		if (week_day === 0) {
			cal += '<TR>';
		}
		if (week_day != 7) {
			var day = Calendar.getDate();
			// highlights todays date
			if (today == Calendar.getDate()) {
				cal += highlight_start + day + highlight_end + '</TD>'; // prints out the day
			} else {
				cal += '<TD WIDTH="30">' + day + '</TD>';
			}
			// end row for the last day of the week
		}
		if (week_day == 7) {
			cal += '</TR>';
		}
		// increments till the end of the month
		Calendar.setDate(Calendar.getDate() + 1);
	} // end for loop
	cal += '</TD></TR></TABLE>';
	//prints calender
	document.write(cal);
}