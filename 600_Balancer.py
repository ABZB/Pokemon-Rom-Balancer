import io
import string
import math
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from constants_pokemon import *

def error_msg_box(tittext, msgtext):
	#Msgbox = tk.messagebox.askquestion(tittext, msgtext, icon = 'warning')
	print(tittext)
	print(msgtext)
	
def scale(stat_arr, base_exp, target, gen_number, exp_bool, shedinja_bool = False, mega_bool = False):
	bst = stat_arr[0] + stat_arr[1] + stat_arr[2] + stat_arr[3] + stat_arr[4] + stat_arr[5] 
	
	print('A', stat_arr, bst)
	
	if(mega_bool):
		temp_hp = stat_arr[0]
		
		for t, s in enumerate(stat_arr):
			stat_arr[t] = round((s*(700 - temp_hp))/(bst - temp_hp))
		stat_arr[0] = temp_hp
		
	#is not a Pokemon Forme changed to in battle that keeps the same HP
	else:
		for t, s in enumerate(stat_arr):
			stat_arr[t] = round((s*target)/bst)
	
	#If Pokemon is Shedinja, set HP to 1
	if(shedinja_bool):
		stat_arr[0] = 1
	
	#scale EXP if desired	
	if(exp_bool):
		base_exp = round(base_exp*target/bst)
		if(gen_number >= 5):
			base_exp = min(1023, base_exp)
		else:
			base_exp = min(255, base_exp)
	
	print('B', stat_arr)
	return(stat_arr, base_exp)

def manipulate(personal, pokemon, base_formes, start_offset, offset, second_offset, gen_number, exp_bool, shedinja_bool, ability_bool, legend_bool, all_bool):
	
	
	#if Gen II, we can search through the file for the literal index numbers
	
	if(gen_number == 2.1):
		for j in range(len(personal)):
			#j is 01 and the next 6 values are Bulbasaur's stats
			try:
				if(personal[j] == 01 and personal[j + 1] == 45 and personal[j + 2] == 49 and personal[j + 3] == 49 and personal[j + 4] == 45 and personal[j + 5] == 65 and personal[j + 6] == 65):
					#j is the index number, want to point to the next value, HP stat
					start_offset = j + 1
					break
			except:
				break
				
	if(gen_number == 3.1 or gen_number == 3.2):
		for j in range(len(personal)):
			#j is 01 and the next 6 values are Bulbasaur's stats
			try:
				if(personal[j] == 45 and personal[j + 1] == 49 and personal[j + 2] == 49 and personal[j + 3] == 45 and personal[j + 4] == 65 and personal[j + 5] == 65):
					#j is the index number, want to point to the next value, HP stat
					start_offset = j
					break
			except:
				break
		
	
	if(gen_number == 7.1):
		in_first_block = True
		
	max_index = len(pokemon) - 1
	
	stat_arr = [0, 0, 0, 0, 0, 0]
	
	
	#Start with the first triplet - Bulba's HP and the following space
	pointer = start_offset
	
	dex_number = 1
	
	output_stats = [["HP","ATK","DEF","SPD","SpA","SpD"]]
	mega_list = []
	
	#read the file character by character
	while True:
		
		print(dex_number)
		#get the stats, the first 6 bytes
		for i in range(6):
			stat_arr[i] = personal[pointer + i]
			#stat_sum += personal[pointer + i]
		#print(stat_sum)
		
		#begin mega/alt forme (that changes in battle) handling
		try:
			#if the Pokemon is a Mega, copy the HP from the base form:
			if(pokemon[dex_number][1] == 6 or pokemon[dex_number][1] == 8):
				#calls the updated HP from the base form (HP is the first stat)
				base_number = base_form_reference_gen_7[dex_number][1]
				stat_arr[0] = output_stats[base_number][1][0]
		#for Gen V, there are only two that can forme change in battle and have different stats - Meloetta and Darmanitan, and the former won't get scaled anyway (base 600).
		except:
			if(dex_number == 701):
				stat_arr[0] = output_stats[555][1][0]

		#calculate the BST
		bst = stat_arr[0] + stat_arr[1] + stat_arr[2] + stat_arr[3] + stat_arr[4] + stat_arr[5] 
		
		#scale the stats
		
		#gen III has different index numbers, needs different catches
		if(gen_number == 3.1 or gen_number == 3.2):
			
			if(all_bool):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool)
				if(dex_number == 303 and shedinja_bool):
					stat_arr[0] = 1
			elif(dex_number == 303 and shedinja_bool):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 400, gen_number, exp_bool, shedinja_bool = True)
			#slakoth
			elif(dex_number == 364):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool)
			#slaking
			elif(dex_number == 366):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 720, gen_number, exp_bool)
			#evolves once more
			elif(pokemon[dex_number][1] == 1):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 450, gen_number, exp_bool)
			#evolves twice more
			elif(pokemon[dex_number][1] == 2):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 300, gen_number, exp_bool)
			#everything else that isn't greater than 600 gets scaled to 600
			elif(bst < 600):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool)
			elif(legend_bool and bst > 600):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool)
				
				
				
		else:
		
			if(all_bool):
				if(pokemon[dex_number][1] == 6 or pokemon[dex_number][1] == 7):
					stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 700, gen_number, exp_bool, mega_bool = True)
				elif(pokemon[dex_number][1] == 8):
					stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool, mega_bool = True)
				else:
					stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool)
				if(dex_number == 292):
					stat_arr[0] = 1
			#evolves one more time
			elif(pokemon[dex_number][1] == 1):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 450, gen_number, exp_bool)
			#evolves two more times
			elif(pokemon[dex_number][1] == 2):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 300, gen_number, exp_bool)
			#shedinja, scale everything as if to 400 but don't scale HP
			elif(dex_number == 292):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 400, gen_number, exp_bool, shedinja_bool = True)
			#Slakoth without changed ability
			elif(dex_number == 287 and not(ability_bool)):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool)
			#slaking without changed ability
			elif(dex_number == 289 and not(ability_bool)):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 720, gen_number, exp_bool)
			#Regigigas with changed ability
			elif(dex_number == 486 and ability_bool):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool)
			#fully evolved or Legendary with <= 600 BST (scale to 600)
			elif(pokemon[dex_number][1] == 0 or pokemon[dex_number][1] == 5):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool)
			#Mega Evolution of a Pokemon with <= 600 BST (Mega has <= 700 BST) (scale to 700)
			elif(pokemon[dex_number][1] == 6):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 700, gen_number, exp_bool, mega_bool = True)
			elif(pokemon[dex_number][1] == 8):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool, mega_bool = True)
			#legendary_Pokemon
			elif(legend_bool and bst > 600 and (pokemon[dex_number][1] != 7 and pokemon[dex_number][1] != 6)):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 600, gen_number, exp_bool)
			elif(legend_bool and bst > 700 and (pokemon[dex_number][1] == 7 or pokemon[dex_number][1] == 6)):
				stat_arr, personal[pointer + 4] = scale(stat_arr, personal[pointer + 4], 700, gen_number, exp_bool)
		
		#if stat is over 255, redistribute the excess
		while True:
			
			overage_count = 0
			overage = 0
			#checks if there is anything over 255
			for counter, stat in enumerate(stat_arr):
				if(stat > 255):
					overage_count += 1
					overage += stat - 255
					stat_arr[counter] = 255
			#if nothing is over 255, proceed
			if(overage == 0):
				break
			#otherwise redistribute, then loop around to make sure we didn't break anything else
			else:
				#if the Pokemon is a Mega, don't change HP
				if(pokemon[dex_number][1] == 6):
					redistribute = max(round(overage/(5 - overage_count)),1)
					for counter, stat in enumerate(stat_arr):
						if(stat != 255 and counter != 0):
							stat_arr[counter] = stat + redistribute
				else:
					redistribute = max(round(overage/(6 - overage_count)),1)
					for counter, stat in enumerate(stat_arr):
						if(stat != 255):
							stat_arr[counter] = stat + redistribute
							

		#checks if the rounding error is greater 5, for Megas, who can have this problem (might have fixed this elsewhere)
		if(pokemon[dex_number][1] == 6):
			while True:
				BST = 0
				for counter, stat in enumerate(stat_arr):
					BST += stat
				rounding_error = BST - 700
				
				#if I can subtract 1 from each non-HP stat (because this should only happen to Pokemon that had weird scaling, the Megas), and still be above the intended BST, do so
				if(rounding_error >= 5):
					for counter, stat in enumerate(stat_arr):
						if(counter != 0):
							stat_arr[counter] = stat - 1
				#if that much below, add 5
				elif(rounding_error <= -5):
					for counter, stat in enumerate(stat_arr):
						if(counter != 0):
							stat_arr[counter] = stat + 1
				#otherwise, we're good, so end this loop
				else:
					break
			#write the non-Mega/Mega pair to the list
			mega_list.append([base_number, dex_number])
		
		

		temp = []
		for stat in stat_arr:
			temp.append(stat)
		
		
		
		#sticks the new stats in this array
		output_stats.append([dex_number, temp])
		
		#overwrite the source string with the new values
		for i in range(6):
			personal[pointer + i] = temp[i]
				
		if(ability_bool):
			#The below offset shifts (24 from the sixth DV to the first Ability) did change from Gen IV to Gen IV, at least
			#change Slakoth's and Slaking's Abilities to Comatose (D5) in gen VII and on, Unaware (6D) otherwise
			if(dex_number == 287 or dex_number == 289):
				if(gen_number >= 7):
					personal[pointer + 24] = 213
					personal[pointer + 1 + 24] = 213
					personal[pointer + 2 + 24] = 213					
				else:
					personal[pointer + 24] = 109
					personal[pointer + 1 + 24] = 109
					
			#change Regigigas' Abilities to Sheer Force or Iron Fist
			if(dex_number == 486):
				personal[pointer + 24] = 125
				personal[pointer + 1 + 24] = 89
				if(gen_number >= 5):
					personal[pointer + 2 + 24] = 125
		
		if(dex_number >= max_index):
			
			#gen vii has a second, repeat block
			if(gen_number == 7.1):
				if(in_first_block):
					in_first_block = False
					pointer = second_offset
					#will get incremented at the end of the loop
					dex_number = 0
				#otherwise print the results and finish
				else:
					#print list of modified stats
					for elm in output_stats:
						print(elm)
						
					#print mega and base list
					if(gen_number >= 6):
						print('\n')
						for elm in mega_list:
							print(output_stats[elm[0]])
							print("m", output_stats[elm[1]])
					break
			#otherwise print the results and finish
			else:
				#print list of modified stats
				for elm in output_stats:
					print(elm)

				break
			
		#zero out the stat array and sum
		for stat in stat_arr:
			stat_arr[counter] = 0
		stat_sum = 0
		stats_counted = 0
		
		#jump to the start of the next Pokemon
		pointer += offset
		#next dex number
		dex_number += 1
	return(personal)
	
	
#takes in bytearray, saves bytes to file
def save_binary_file(data, file_name, path):

	root = Tk()
	root.update()
	output_path = asksaveasfilename(initialdir = path,  defaultextension = "", initialfile = file_name)
	root.destroy()
	
	output_binary = bytes(data)
	
	with open(output_path, 'wb') as f:
		f.write(output_binary)
		
def get_files(personal_file_path):

	#get hex file locations:
	#root = Tk()
	#root.update()
	personal_location = askopenfilename(filetypes = (("Select Personal File", "*.*"), ("All Files", "*.*")))
	#root.destroy()
	
	#get the data
	with open(personal_location, 'rb') as f:
		personal_bin = f.read()

	
	#convert the binary data into bytearrays. each index is one hex-pair
	personal = bytearray(personal_bin)
	
	return(personal, personal_location)


def main(gen_number, exp_bool, shedinja_bool, ability_bool, legend_bool = False, all_bool = False):
	try:
		gen_number = int(gen_number)
	except:
		try:
			gen_number = float(gen_number)
		except:
			print("Problem with Gen number:", gen_number, type(gen_number))
	pokemon, base_formes, start_offset, offset, second_offset, personal_file_path = set_constants(gen_number)
	
	#print(shedinja_bool, ability_bool, legend_bool, all_bool)
	if(legend_bool and all_bool):
		error_msg_box('Conflicting Options Error', 'Scaling everything to 600 and scaling down Legendaries creates conflicts, please select at most one.')
		return(False)
	if(ability_bool and gen_number < 4):
		error_msg_box('Ability Option Error', 'Ability modifier only available for Gen IV and later.')
		return(False)
	if(gen_number < 3 and (shedinja_bool or ability_bool)):
		error_msg_box('Option Error', 'Ability and Shedinja modifiers do not apply to Gen II.')
	#root_main_menu.destroy()
	
	#get the data files and the output path
	personal, output_path = get_files(personal_file_path)
	
	
	personal_new = manipulate(personal, pokemon, base_formes, start_offset, offset, second_offset, gen_number, exp_bool, shedinja_bool, ability_bool, legend_bool, all_bool)
	
	#seperates the file name (always a single character from HGSS on) from path
	file_name = output_path[-1]
	output_path = output_path[:-1]
	
	
	save_binary_file(personal, file_name + '.bak', output_path)
	
	save_binary_file(personal_new, file_name, output_path)

def main_menu():
	global master
	master = Tk()

	row_iter = 0
	#frame_main_menu = Frame(master)
	#frame_main_menu.pack()
		
	master.title('Select Game to modify & modifications to apply')
	#booleans variables for checkboxes
	
	#also scale base exp.
	exp_bool = BooleanVar()
	
	#Scale down Shedinja
	shedinja_bool = BooleanVar()
	
	#Change abilities
	ability_bool = BooleanVar()
	
	#Scale all pokemon with BST greater than 600 to 600
	legend_bool = BooleanVar()
	
	#Scale all Pokemon, no matter what, to 600
	all_bool = BooleanVar()
	
	#checkboxes and accompanying text
	Label(master, text = 'Options', font = (16)).grid(row = row_iter)
	
	row_iter +=1
	
	Checkbutton(master, text = 'Also scale Base Exp.', variable = exp_bool, onvalue = True, offvalue = False).grid(row = row_iter, sticky = W)
	
	row_iter +=1
	
	Checkbutton(master, text = 'Scale Down Shedinja', variable = shedinja_bool, onvalue = True, offvalue = False).grid(row = row_iter, sticky = W)
	
	row_iter +=1
	
	Checkbutton(master, text = 'Change Abilities of Slakoth, Slaking, and Regigigas', variable = ability_bool, onvalue = True, offvalue = False).grid(row = row_iter, sticky = W)
	
	row_iter +=1
	
	Checkbutton(master, text = 'Scale down [Legendary] Pokemon to 600', variable = legend_bool, onvalue = True, offvalue = False).grid(row = row_iter, sticky = W)
	
	row_iter +=1
	
	Checkbutton(master, text = 'Scale every Pokemon to 600, no matter what', variable = all_bool, onvalue = True, offvalue = False).grid(row = row_iter, sticky = W)
	
	row_iter +=1
	
	
	#game selection
	Label(master, text = 'Select Target', font = (16)).grid(row = row_iter)
	
	row_iter +=1
	
	Button(master, text = 'Crystal', command = lambda: main('2.1', exp_bool.get(), shedinja_bool.get(), ability_bool.get(), legend_bool.get(), all_bool.get()), height = 2, width = 50, pady = 1).grid(row = row_iter)
	
	row_iter +=1
	
	Button(master, text = 'Fire Red', command = lambda: main('3.1', exp_bool.get(), shedinja_bool.get(), ability_bool.get(), legend_bool.get(), all_bool.get()), height = 2, width = 50, pady = 1).grid(row = row_iter)
	
	row_iter +=1
	
	Button(master, text = 'Emerald', command = lambda: main('3.2', exp_bool.get(), shedinja_bool.get(), ability_bool.get(), legend_bool.get(), all_bool.get()), height = 2, width = 50, pady = 1).grid(row = row_iter)
	
	row_iter +=1
	
	Button(master, text = 'Heart Gold/Soul Silver', command = lambda: main('4.1', exp_bool.get(), shedinja_bool.get(), ability_bool.get(), legend_bool.get(), all_bool.get()), height = 2, width = 50, pady = 1).grid(row = row_iter)
	
	row_iter +=1
	
	Button(master, text = 'Platinum', command = lambda: main('4.2', exp_bool.get(), shedinja_bool.get(), ability_bool.get(), legend_bool.get(), all_bool.get()), height = 2, width = 50, pady = 1).grid(row = row_iter)
	
	row_iter +=1
	
	Button(master, text = 'Black/White', command = lambda: main('5.0', exp_bool.get(), shedinja_bool.get(), ability_bool.get(), legend_bool.get(), all_bool.get()), height = 2, width = 50, pady = 1).grid(row = row_iter)
	
	row_iter +=1
	
	Button(master, text = 'Black2/White2', command = lambda: main('5.1', exp_bool.get(), shedinja_bool.get(), ability_bool.get(), legend_bool.get(), all_bool.get()), height = 2, width = 50, pady = 1).grid(row = row_iter)
	
	row_iter +=1
	
	Button(master, text = 'Ultra Sun/Ultra Moon', command = lambda: main('7.1', exp_bool.get(), shedinja_bool.get(), ability_bool.get(), legend_bool.get(), all_bool.get()), height = 2, width = 50, pady = 1).grid(row = row_iter)
	
	row_iter +=1
	
	Button(master, text="Exit", command = master.destroy, height = 2, width = 25, pady = 1).grid(row = row_iter)
	
	master.mainloop()
	
	

main_menu()
