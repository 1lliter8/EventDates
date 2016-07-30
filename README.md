# EventDates
Very rough script for turning common formats of event lists into weekly patterns


Usage

-----

This script takes a hard-coded input (currently testdata2.txt) which is intended to be one of a handful of formats of event listings manually taken from a website. It then prints these events as weekly patterns because this is a propriatary format useful for my current job. Other applications could be verifying hand-created event listings match written performance schedules.

This tool has been written around British, and particularly London-based theatre events, so drop-down list boxes of events available from companies like Nimax provide the hard data. Other companies, like Spectrix, might display information in hidden <li> elements or tables. This tool isn't intended to be exhaustive, and requires tweaking for each data set it's used on, though it's saved me countless hours of effort and avoided, I'm sure, a great deal of human error.

Different formats of data need to be commented in and out, and the parsing of date data will need to be tweaked to appease the strptime module. Common handles are in my comments to avoid going back and forth between the documentation.


Known bugs

----------

For dates across the 2016/17 divide the script sometimes gets Sunday January 1st mixed up and puts it as the last date in 2017 even though it belongs to a pattern of the final week of 2016. This is to do with the ISO standard weeks that I've used to group things weekly. Weeks run Monday-Sunday and the year break confuses things. It's not worth fixing because it would take too long for the time I save by using this, and also because Christmas schedules typically fall outside normal patterns so it doesn't cost me time anyway.
