From the readme:

Section I: Purpose

    To make all Pokemon competitive. The difficulty is also  increased, as even a Raticate has a BST of 600.


Section II: Description of Edits
    This program scales the Base Stat Totals of all Pokemon as follows:
    
    1) Pokemon that evolve twice (like Bulbasaur or Porygon) get a BST of 300
    2) Pokemon that evolve once (like Ivysaur or Eevee) get a BST of 450
    3) Pokemon that don't evolve:
        a) Legendaries with BST greater than 600 are not scaled
        b) Legendaries with a BST of less than 600, and all Pokemon that do not evolve (like Venusaur or Tauros), get a BST of 600, except for:
            i) Wishiwashi School Forme is scaled to 700, its base Forme is left as is
            ii) Porygon2 and Scyther are scaled to 600
            iii) Shedinja is scaled to 400, then its HP is reset to 1
            iv) Regigigas is scaled to 600, and gains the Abilities Iron Fist and Sheer Force
            v) Slaking is scaled to 600, and both it and Slakoth gain Unaware, except in Generation VII and on, where they gain Comatose.
            vi) Darmanitan-Zen is scaled to 630
            v) Greninja-Ash is left as is.
        c) Mega Evolutions of Pokemon with BST not greater than 600 are scaled to 700, holding their HP to the value of their base forms
        d) All in-battle Forme changes are scaled as above, holding their HP constant to keep the game mechanics constant.
            
    Details, including a Speed Tier calculator, can be found in the included Excel file.


Section III:: Explanation of Options:
	Checkbutton(master, text = 'Also scale Base Exp.', variable = exp_bool, onvalue = True, offvalue = False).grid(row = 1, sticky = W)
	Checkbutton(master, text = 'Scale Down Shedinja', variable = shedinja_bool, onvalue = True, offvalue = False).grid(row = 2, sticky = W)
	Checkbutton(master, text = 'Change Abilities of Slakoth, Slaking, and Regigigas', variable = ability_bool, onvalue = True, offvalue = False).grid(row = 3, sticky = W)
	Checkbutton(master, text = 'Scale down [Legendary] Pokemon to 600', variable = legend_bool, onvalue = True, offvalue = False).grid(row = 4, sticky = W)
	Checkbutton(master, text = 'Scale every Pokemon to 600, no matter what', variable = ability_bool, onvalue = True, offvalue = False).grid(row = 5, sticky = W)
	
	(1) Also scale Base Exp - multiplies the base experience yield by the same multiplier that the base stats get multiplied by. This scales up the experience commensurately with the increased difficulty of the respective Pokemon. However, it can throw off level curves. I do not reccomend using this option except when the experience yield is scaled by relative level (like in Gen V), or in conjuction with a mod with a sharply increased level curve.
	(2) 'Scale Down Shedinja' - Shedinja's BST will be scaled to 400 instead of 600.
	(3) Change Abilities of Slakoth, Slaking, and Regigigas:
		* Gen IV, Slakoth & Slaking get Unaware and are scaled to 300 and 600, and Regigigas gets Iron Fist and is scaled down to 600
		* Gen V-VI Slakoth & Slaking get Unaware and are scaled to 300 and 600, and Regigigas gets Iron Fist and Sheer Force and is scaled down to 600
		* Gen VII  Slakoth & Slaking get Comatose and are scaled to 300 and 600, and Regigigas gets Iron Fist and Sheer Force and is scaled down to 600
	(4) Scale down [Legendary] Pokemon to 600 - All Legendary Pokemon with BTST > 600 are scaled down to 600
	(5) Scale every Pokemon to 600, no matter what - All Pokemon, no matter their evolutionary stage, are scaled to 600. All Megas and Primal Reversions are scaled to 700.

	* Note that option (3) cannot be selected for Gen III, and options (4) and (5) cannot both be selected at once.

Section IV: Instructions 

	(A) Gen IV and later

		1) Decompress the NDS or 3DS file using an appropriate tool.

		2) Run 600 Balancer

		3) Check the desired options, then select the appropriate target game.

		4) Select the appropriate file:

				* HGSS: /a/0/0/2
				* Platinum /poketool/personal/pl_personal.narc
				* BW & B2W2: /a/0/1/6
				* USUSM: a/0/1/7

		5) You will be prompted to save a backup of the original file.
		
		6) You will be prompted to save the edited file.
		
		7) Exit 600 Balancer
		
		7) Rebuild the file or use Luma, Hans, etc. as desired.

	(B) Gen II or III (Gold, Silver, Crystal, FireRed, LeafGreen, Emerald)
		1) Run 600 Balancer
		
		2) Check the desired options, then select target game from the menu.
		
		3) Select the target .gbc or .gba file.

		4) You will be prompted to save a backup of the original file.
		
		5) You will be prompted to save the edited file.
		
		6) Exit 600 Balancer