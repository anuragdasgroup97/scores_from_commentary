from datetime import datetime
start_time = datetime.now()

import os
os.system("cls") # clearing screen
os.chdir(r'C:\anurag python folder\project cricket scoreboard') # making the parent directory as current directory
import csv

def get_runs(r): # gettings runs from string
	if r=="FOUR" or r=='4': return 4
	else: return int(r)
	
def do_work(lines,bowl_map,bat_map,team_bat,team_bowl,team_extras,team_runs,team_wic,team_w,team_pow_runs,team_last,bowl_line_up,bat_line_up):
	prev_over=0; run_over=0; prev_bowl=""
	# print(len(lines))
	for i in range(0,len(lines),2):
		# print("hi")
		li1=lines[i].split(',') # over bowler to batsman, run,...
		li2=li1[0].split(" to ") # over bowler, batsman
		try:
			bat=bat_map[li2[1]] # batsman
		except Exception as e:
			print(e)
			print("Unable to get batsman name from the map")
			exit()
		li3=li2[0].split() # over, bowler
		ball=li3[0] # over
		bowl=""
		
		try:
			for j in range(1,len(li3)): 
				bowl+=li3[j] # bowler name
				if j!=len(li3)-1: bowl+=" "
		except Exception as e:
			print(e)
			print("Unable to get bowler name from the team")
			exit()
			
		if bowl_map[bowl] not in bowl_line_up: bowl_line_up.append(bowl_map[bowl]) # bowling line up
		if bat not in bat_line_up: bat_line_up.append(bat) # batting line up
		
		li1[1]=li1[1].strip() # removing extra space
		li4=li1[1].split() # runs part
		runs=li4[0]
		over=int(ball.split('.')[0])
		ball_no=int(ball.split('.')[1])
		
		if prev_over!=over: # next over starts
			if prev_over==5: # powerplay runs
				team_pow_runs=team_runs
			
			team_bowl[prev_bowl]["O"]+=1
			
			if run_over==0: # maiden over
				team_bowl[prev_bowl]["M"]+=1
			else:
				team_bowl[prev_bowl]["R"]+=run_over
			
			run_over=0
		prev_over=over
		prev_bowl=bowl_map[bowl]
		team_bat[bat]["B"]+=1
		team_bat[bat]["status"]="not out"
		
		if runs=="1":
			run_over+=1
			team_runs+=1
			team_bat[bat]["R"]+=1
		elif runs=="2":
			run_over+=2
			team_runs+=2
			if li4[1]=="wides":
				team_bowl[bowl_map[bowl]]["WD"]+=2
				ball_no-=1
				team_bat[bat]["B"]-=1
				team_extras["w"]+=2
			else:
				team_bat[bat]["R"]+=2
		elif runs=="3":
			run_over+=3
			team_runs+=3
			if li4[1]=="wides":
				team_bowl[bowl_map[bowl]]["WD"]+=3
				ball_no-=1
				team_bat[bat]["B"]-=1
				team_extras["w"]+=3
			else:
				team_bat[bat]["R"]+=3
		elif runs=="out":
			team_w+=1
			if li4[1][0]=='L':
				team_bat[bat]["status"]="lbw "
			elif li4[1][0]=='C':
				temp=""
				if li4[3][-1]=='!': temp=li4[3][:-2]
				else: temp=li4[3]+" "+li4[4][:-2]
				team_bat[bat]["status"]="c " + temp +" "
			else:
				team_bat[bat]["status"]=""
			
			team_bat[bat]["status"]+="b " + bowl_map[bowl]
			
			try:
				team_wic+=str(team_runs) + "-"+ str(team_w) + " (" + bat + ", " + ball + "), "
			except Exception as e:
				print(e)
				print("Unable to write in team_wic for the wickets fallen")
		elif runs=="wide":
			run_over+=1
			team_runs+=1
			ball_no-=1
			team_bat[bat]["B"]-=1
			team_bowl[bowl_map[bowl]]["WD"]+=1
			team_extras["w"]+=1
		elif runs=="FOUR":
			run_over+=4
			team_runs+=4
			team_bat[bat]["R"]+=4
			team_bat[bat]["4s"]+=1
		elif runs=="SIX":
			run_over+=6
			team_runs+=6
			team_bat[bat]["R"]+=6
			team_bat[bat]["6s"]+=1
		elif runs=="leg" or runs=="byes":
			li1[2]=li1[2].strip()
			li5=li1[2].split()
			r=get_runs(li5[0])
			team_runs+=r
			if runs=="byes": team_extras["b"]+=r
			else: team_extras["lb"]+=r
			
	team_bowl[bowl_map[prev_bowl]]["R"]+=run_over
	if ball_no==6: # last ball case
		team_bowl[bowl_map[prev_bowl]]["O"]+=1
		team_last=prev_over+1
		if run_over==0:
			team_bowl[bowl_map[prev_bowl]]["M"]+=1
	else:
		team_last=prev_over+ball_no/10
		team_bowl[bowl_map[prev_bowl]]["O"]+=ball_no/10
		
	extras=0
	for item in team_extras: extras+=team_extras[item] # summing the complete extras
	extras=str(extras)+" ("
	try:
		for key,value in team_extras.items(): 
			try:
				extras+=str(key)+" "+ str(value)+", "
			except Exception as e:
				print(e)
				exit()
	except Exception as e:
		print(e)
		print("Unable to get extras of the bowling team")
		exit()
	extras=extras[:-2]+")"
	return [team_bat,team_bowl,extras,team_runs,team_wic[:-2],team_w,team_pow_runs,team_last,bowl_line_up,bat_line_up]

def eco(over,run): # getting economy
	over=over//1+(over%1)*10/6
	return round(run/over,2)

def scorecard():
	with open(r'teams.txt','r') as f:
		line=f.readline()
		try:
			temp=line.split(":") # splitting the team name from palyers list
			pakistan=(temp[1]).split(',') # splitting the players name and storing in list
		except Exception as e:
			print(e)
			print("Unable to get the names of Pakistan player from teams.txt")
			exit()
		
		f.readline() # as there is one empty line
		
		line=f.readline()
		temp=line.split(":") # splitting the team name from palyers list
		india=(temp[1]).split(',') # splitting the players name and storing in list
		
		pakistan=[i.strip() for i in pakistan] # removing the extra spaces from the names of the players
		india=[i.strip() for i in india] # removing the extra spaces from the names of the players
	
	pak_map={'Babar Azam':'Babar Azam(c)','Rizwan':'Mohammad Rizwan(w)','Fakhar Zaman':'Fakhar Zaman','Iftikhar Ahmed':'Iftikhar Ahmed','Khushdil':'Khushdil Shah','Shadab Khan':'Shadab Khan','Asif Ali':'Asif Ali','Mohammad Nawaz':'Mohammad Nawaz','Haris Rauf':'Haris Rauf','Naseem Shah':'Naseem Shah','Dahani':'Shahnawaz Dahani'} # a map between the name used in commentary and their complete names
	
	ind_map={'Rohit':'Rohit Sharma(c)','Rahul':'KL Rahul','Kohli':'Virat Kohli','Bhuvneshwar':'Bhuvneshwar Kumar','Arshdeep Singh':'Arshdeep Singh','Hardik Pandya':'Hardik Pandya','Avesh Khan':'Avesh Khan','Chahal':'Yuzvendra Chahal','Jadeja':'Ravindra Jadeja','Karthik':'Dinesh Karthik(w)','Suryakumar Yadav':'Suryakumar Yadav',} # a map between the name used in commentary and their complete names
	
	pak_bat={}; pak_bowl={}; pak_bowl_line=[]; pak_bat_line=[] # line up is a list where we will have the bowlers, batsman in order of batting/bowling lineup
	for player in pakistan: # making a dictionary for all the players where we will maintain the counts needed of their batting 
		pak_bat[player]={"status":"Did not Bat","R":0,"B":0,"4s":0,"6s":0,"SR":0.00}
		pak_bowl[player]={"status":"Did not Bowl","O":0,"M":0,"R":0,"W":0,"NB":0,"WD":0,"ECO":0.00}
	
	ind_bat={}; ind_bowl={}; ind_bowl_line=[]; ind_bat_line=[] # line up is a list where we will have the bowlers, batsman in order of batting/bowling lineup
	for player in india: # making a dictionary for all the players where we will maintain the counts needed of their batting 
		ind_bat[player]={"status":"Did not Bat","R":0,"B":0,"4s":0,"6s":0,"SR":0.00}
		ind_bowl[player]={"status":"Did not Bowl","O":0,"M":0,"R":0,"W":0,"NB":0,"WD":0,"ECO":0.00}
	
	# variables that we will be needing
	extras_pak={"b":0,"lb":0,"w":0,"nb":0,"p":0}; pak_runs=0; wic_pak=""; wic_p=0; pow_runs_p=0; last_p=0 
	extras_ind={"b":0,"lb":0,"w":0,"nb":0,"p":0}; ind_runs=0; wic_ind=""; wic_i=0; pow_runs_i=0; last_i=0
	
	with open(r'pakistan_innings1.txt','r') as f: # Pakistan Innings
		lines=f.readlines()
		pak_bat,ind_bowl,extras_ind,pak_runs,wic_pak,wic_p,pow_runs_p,last_p,ind_bowl_line,pak_bat_line=do_work(lines,ind_map,pak_map,pak_bat,ind_bowl,extras_ind,pak_runs,wic_pak,wic_p,pow_runs_p,last_p,ind_bowl_line,pak_bat_line)
		
	with open(r'india_innings2.txt','r') as f: # India Innings
		lines=f.readlines()
		ind_bat,pak_bowl,extras_pak,ind_runs,wic_ind,wic_i,pow_runs_i,last_i,pak_bowl_line,ind_bat_line=do_work(lines,pak_map,ind_map,ind_bat,pak_bowl,extras_pak,ind_runs,wic_ind,wic_i,pow_runs_i,last_i,pak_bowl_line,ind_bat_line)
	
	with open('scorecard.csv', 'w', newline='') as f: # writing in csv file
		writer=csv.writer(f)
		
		writer.writerow(["India won by 5 wkts"])
		writer.writerow([])
		
		writer.writerow(["Pakistan Innings","","","","","",str(pak_runs)+"-"+str(wic_p)+" (" +str(last_p) +" Ov)"])
		writer.writerow([])
		
		writer.writerow(["Batter","","R","B","4s","6s","SR"])
		writer.writerow([])
		
		for batter in pak_bat_line: # batsman
			writer.writerow([batter,pak_bat[batter]["status"],pak_bat[batter]["R"],pak_bat[batter]["B"],pak_bat[batter]["4s"],pak_bat[batter]["6s"],round((pak_bat[batter]["R"]/pak_bat[batter]["B"])*100,2)])
		
		writer.writerow([])
		writer.writerow(["Extras","",extras_ind]) # extras
		writer.writerow(["Total","",str(pak_runs)+" ("+str(wic_p)+" wkts, "+str(last_p)+" Ov)"]) # total
		if len(pak_bat_line)!=11: # Did not bat
			temp=""
			try:
				for player in pakistan:
					if player not in pak_bat_line: temp+=player+", "
			except Exception as e:
				print(e)
				print("Unable to get players who did not bat from the Pakistan team")
			writer.writerow(["Did not Bat",temp[:-2]])
		
		writer.writerow([])
		writer.writerow(["Fall of wickets"])
		writer.writerow([wic_pak]) # fall of wickets
		writer.writerow([])
		
		writer.writerow(["Bowler","O","M","R","W","NB","WD","ECO"])
		writer.writerow([])
		for bowler in ind_bowl_line: # bowlers
			writer.writerow([bowler,ind_bowl[bowler]["O"],ind_bowl[bowler]["M"],ind_bowl[bowler]["R"],ind_bowl[bowler]["W"],ind_bowl[bowler]["NB"],ind_bowl[bowler]["WD"],eco(ind_bowl[bowler]["O"],ind_bowl[bowler]["R"])])
			
		writer.writerow([])
		writer.writerow(["Powerplays","Overs","Runs"])
		writer.writerow(["Mandatory","0.1-6",str(pow_runs_p)]) # powerplay
		writer.writerow([])
		
		writer.writerow(["India Innings",str(ind_runs)+"-"+str(wic_i)+" (" +str(last_i) +" Ov)"]) # India Innings
		writer.writerow([])
		
		writer.writerow(["Batter","","R","B","4s","6s","SR"])
		writer.writerow([])
		
		for batter in ind_bat_line:
			writer.writerow([batter,ind_bat[batter]["status"],ind_bat[batter]["R"],ind_bat[batter]["B"],ind_bat[batter]["4s"],ind_bat[batter]["6s"],round((ind_bat[batter]["R"]/ind_bat[batter]["B"])*100,2)])
		
		writer.writerow([])
		writer.writerow(["Extras","",extras_pak])
		writer.writerow(["Total","",str(ind_runs)+" ("+str(wic_i)+" wkts, "+str(last_i)+" Ov)"])
		if len(ind_bat_line)!=11:
			temp=""
			try:
				for player in india:
					if player not in ind_bat_line: temp+=player+", "
			except Exception as e:
				print(e)
				print("Unable to get players who did not bat from the Indian team")
			writer.writerow(["Did not Bat",temp[:-2]])
		
		writer.writerow([])
		writer.writerow(["Fall of wickets"])
		writer.writerow([wic_ind])
		writer.writerow([])
		
		writer.writerow(["Bowler","O","M","R","W","NB","WD","ECO"])
		writer.writerow([])
		for bowler in pak_bowl_line:
			writer.writerow([bowler,pak_bowl[bowler]["O"],pak_bowl[bowler]["M"],pak_bowl[bowler]["R"],pak_bowl[bowler]["W"],pak_bowl[bowler]["NB"],pak_bowl[bowler]["WD"],eco(pak_bowl[bowler]["O"],pak_bowl[bowler]["R"])])
			
		writer.writerow([])
		writer.writerow(["Powerplays","Overs","Runs"])
		writer.writerow(["Mandatory","0.1-6",str(pow_runs_i)])
			
from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

scorecard()

end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
