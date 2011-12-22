#!/usr/bin/python
import csv
import urllib2
from BeautifulSoup import BeautifulSoup 

#file IO stuff
csv_in = csv.reader(open('input.csv', 'rb'));
csv_out = csv.writer(open('output.csv', 'wb'));

#column labels
csv_out.writerow(["Channel URL", "Channel Views", "Total Upload Views", "Subscribers", "Age", "Joined", "Website" ]);	

#process each row in the input csv
for row in csv_in:
	if len(row[0]) > 0:
		print "Fetching " + row[0] + "...",;

		#init variables
		subscribers = "";
		age = "";
		channel_views = "";
		video_views = "";
		member_since = "";
		name = "";
		url = "";

		#try:
		response = urllib2.urlopen(row[0]);
		source = response.read();
		doc = BeautifulSoup(source);

		#this div contains all the info
		profile_data = doc.find("div", {"class":"profile_info vcard"});

		#grab all the data !!!!!
		field = profile_data.find("div", {"id":"profile_show_subscriber_count"});
		if not field is None:
			subscribers = field.string		
		
		field = profile_data.find("div", {"id":"profile_show_age"});
		if not field is None:
			age = field.string;
		
		field = profile_data.find("div", {"id":"profile_show_viewed_count"});
		if not field is None:
			channel_views = field.string	
		
		field = profile_data.find("div", {"id":"profile_show_total_video_views"});
		if not field is None:
			video_views = field.string
			
		field = profile_data.find("div", {"id":"profile_show_member_since"});
		if not field is None:
			member_since = field.string
		
		field = profile_data.find("div", {"id":"profile_show_first_name"});
		if not field is None:
			name = field.string
		
		field = profile_data.find("div", {"class":"uix-redirect-link-url"});
		if not field is None:
			url = field.string

		print "DONE";
		
		#except:
		#	print "ERROR";

		#write it out so we dont forget
		csv_out.writerow([str(row[0]), channel_views, video_views, subscribers, age, member_since, url]);	

print "Done.";
