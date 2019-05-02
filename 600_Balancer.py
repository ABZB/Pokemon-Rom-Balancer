import io
import string
import math
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from constants_pokemon import *



def manipulate(personal, pokemon, base_formes, start_offset, offset, second_offset, gen_number):

	
	if(gen_number == 7.1):
		in_first_block = True
		
	max_index = len(pokemon) - 1
	
	stat_arr = [0, 0, 0, 0, 0, 0]
	
	stat_sum = 0
	
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
			stat_sum += personal[pointer + i]
		print(stat_sum)
		
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

		
		#scale the stats
		
		#gen III has different index numbers, needs different catches
		if(gen_number == 3.1 or gen_number == 3.2):
			bst = stat_arr[0] + stat_arr[1] + stat_arr[2] + stat_arr[3] + stat_arr[4] + stat_arr[5] 
			for counter, stat in enumerate(stat_arr):
				#shedinja, scale everything as if to 400 but don't scale HP
				if(dex_number == 303):
					if(counter != 0):
						stat_arr[counter] = round((stat*400)/stat_sum)
					if(counter == 0):
						personal[pointer + 4] = min(round((stat*400)/stat_sum), 255)
				#slakoth
				elif(dex_number == 364):
					stat_arr[counter] = round((stat*500)/stat_sum)
					if(counter == 0):
						personal[pointer + 4] = min(round((stat*500)/stat_sum), 255)
				#slaking
				elif(dex_number == 366):
					stat_arr[counter] = round((stat*720)/stat_sum)	
					if(counter == 0):
						personal[pointer + 4] = min(round((stat*720)/stat_sum), 255)
				#evolves once more
				elif(pokemon[dex_number][1] == 1):
					stat_arr[counter] = round((stat*450)/stat_sum)
					if(counter == 0):
						personal[pointer + 4] = min(round((stat*450)/stat_sum), 255)
				#evolves twice more
				elif(pokemon[dex_number][1] == 2):
					stat_arr[counter] = round((stat*300)/stat_sum)
					if(counter == 0):
						personal[pointer + 4] = min(round((stat*300)/stat_sum), 255)
				#everything else that isn't greater than 600 gets scaled to 600
				elif(bst < 600):
					stat_arr[counter] = round((stat*600)/stat_sum)
					if(counter == 0):
						personal[pointer + 4] = min(round((stat*600)/stat_sum), 255)
					
				
				
		else:
			for counter, stat in enumerate(stat_arr):
				#evolves one more time
				if(pokemon[dex_number][1] == 1):
					stat_arr[counter] = round((stat*450)/stat_sum)
				#evolves two more times
				elif(pokemon[dex_number][1] == 2):
					stat_arr[counter] = round((stat*300)/stat_sum)
				#shedinja, scale everything as if to 400 but don't scale HP
				elif(dex_number == 292):
					if(counter != 0):
						stat_arr[counter] = round((stat*400)/(stat_sum))
				#Slakoth
				elif(dex_number == 287 and gen_number < 7):
					stat_arr[counter] = round((stat*600)/stat_sum)
				#slaking
				elif(dex_number == 289 and gen_number < 7):
					stat_arr[counter] = round((stat*720)/stat_sum)
				#fully evolved or Legendary with <= 600 BST (scale to 600)
				elif(pokemon[dex_number][1] == 0 or pokemon[dex_number][1] == 5):
					stat_arr[counter] = round((stat*600)/stat_sum)
				#Mega Evolution of a Pokemon with <= 600 BST (Mega has <= 700 BST) (scale to 700)
				elif(pokemon[dex_number][1] == 6):
					#don't change HP
					if(counter != 0):
						stat_arr[counter] = round((stat*(700 - stat_arr[0]))/(stat_sum - stat_arr[0]))
				elif(pokemon[dex_number][1] == 8):
					#don't change HP
					if(counter != 0):
						stat_arr[counter] = round((stat*(600 - stat_arr[0]))/(stat_sum - stat_arr[0]))
		
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
				
		
		#The below offset shifts (24 from the sixth DV to the first Ability) did change from Gen IV to Gen IV, at least
		#change Slakoth's and Slaking's Abilities to Comatose (D5) in gen VII and on, Unaware (6D) otherwise
		if(dex_number == 287 or dex_number == 289 and gen_number >= 7):
			personal[pointer + 24] = 213
			personal[pointer + 1 + 24] = 213
			personal[pointer + 2 + 24] = 213
			
		#change Regigigas' Abilities to Sheer Force or Iron Fist
		if(dex_number == 486 and gen_number >= 4):
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


def main(gen_number):
	try:
		gen_number = int(gen_number)
	except:
		try:
			gen_number = float(gen_number)
		except:
			print("Problem with Gen number:", gen_number, type(gen_number))
	pokemon, base_formes, start_offset, offset, second_offset, personal_file_path = set_constants(gen_number)
	
	#root_main_menu.destroy()
	
	#get the data files and the output path
	personal, output_path = get_files(personal_file_path)
	
	
	personal_new = manipulate(personal, pokemon, base_formes, start_offset, offset, second_offset, gen_number)
	
	#seperates the file name (always a single character from HGSS on) from path
	file_name = output_path[-1]
	output_path = output_path[:-1]
	
	
	save_binary_file(personal, file_name + '.bak', output_path)
	
	save_binary_file(personal_new, file_name, output_path)

def main_menu():
	global root_main_menu
	root_main_menu = Tk()

	frame_main_menu = Frame(root_main_menu)
	frame_main_menu.pack()
		
	root_main_menu.title('Select Game to modify')

	Button(frame_main_menu, text = 'Fire Red/Leaf Green', command = lambda: main('3.1'), height = 2, width = 50, pady = 1).pack()
	
	Button(frame_main_menu, text = 'Emerald', command = lambda: main('3.2'), height = 2, width = 50, pady = 1).pack()
	
	Button(frame_main_menu, text = 'Heart Gold/Soul Silver', command = lambda: main('4.1'), height = 2, width = 50, pady = 1).pack()
	
	Button(frame_main_menu, text = 'Platinum', command = lambda: main('4.2'), height = 2, width = 50, pady = 1).pack()
	
	Button(frame_main_menu, text = 'Black2/White2', command = lambda: main('5.1'), height = 2, width = 50, pady = 1).pack()
	
	Button(frame_main_menu, text = 'Ultra Sun/Ultra Moon', command = lambda: main('7.1'), height = 2, width = 50, pady = 1).pack()
	
	Button(frame_main_menu, text="Exit", command = root_main_menu.destroy, height = 2, width = 25, pady = 1).pack()
	
	root_main_menu.mainloop()

main_menu()
