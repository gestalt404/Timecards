# Timecards
Timecard program for cssd

Instructions:
0. Make sure you have Python 3 installed onto your computer, you can get it at https://www.python.org/downloads/
1. Put timecards.py into a folder
2. Create .xlsx (excel) files for shifts and logins
3. Put those files into the folder with timecards.py and rename them to "Shifts.xlsx" and "Logins.xlsx"
4. Open command prompt/terminal and move into the folder
5. Run "python3 timecards.py"
6. "calc" command will display all late/early/none/good shift times
7. entering in a PID for an employee will display a detailed breakdown of all of their logins (approximate spelling allowed ex. "abc12" you could just type "abc" and it will display for every employee that has a PID that contains "abc")
8. "end" or just pressing enter with no text will end the program
9. IF YOU DON'T END THE PROGRAM PROPERLY IT WON'T DELETE SEVERAL HELPER FILES IN THE FOLDER


Quirks:
This program is a pretty nieve take on the problem of trying to find lates and early logoffs. Thus, there are some quirks that you need to take into account when using this.

"GOOD" - outputs are very trustworthy because I specifically wanted it to be fairly strict. So you can trust generally the "GOOD"s.

"LATE" and "EARL" - are a little less trustworthy. The main thing you need to know is that the time output is always the earliest/latest login/logout for that day. So if, for instance someone didn't show up for their shift on time yet logged into a lab computer 5 hours after their shift, it would show "LATE" and output the time of their login 5 hours later. It "should" show up as a red "NONE" but that is hard to do for various reasons. So you should always check to make sure if the output time makes sense and if it doesn't you can always type in their PID to get all their logins for each day

 "BOTH" - is by far the worst and has the most mess-ups. It has the same problems as "LATE"/"EARL" combined. Most times when "BOTH" messes up it should be a "NONE" so I double check them when the times don't make sense.
 
 "NONE" - is by far the most trustworthy output because it just checks if the employee had ANY logins at all during the day. "NONE" is foolproof.
 
 THIS PROGRAM DOESN"T TAKE INTO ACCOUNT THE TYPES OF SHIFTS - so if someone has a "timecard" shift or a "reimbursement for online training" shift it will say they didn't show up.
 
 This program also generates some helper files in the folder you put it into when you run it. These files are deleted when you "end" the program properly, but if you just crash it or close out the terminal window without ending it properly these files won't be deleted. They won't ruin anything and will be overwritten next time you run it but if they are annoying to you it's fine to just delete the .csv files in the folder.
