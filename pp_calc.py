import math
import requests
import sys

class bm:
	class Beatmap:
		def __init__(self, file):
			self.searchfile = file
			self.main()
		def main(self):

			## Setting init beatmap values
			# Metadata
			self.title = None
			self.artist = None
			self.creator = None
			self.version = None

			# difficulty
			self.hp = 0
			self.cs = 0
			self.od = 0
			self.ar = 0
			self.sv = 0
			self.tick_rate = 1
			self.speed = 1

			# Combo
			self.num_circles = 0
			self.num_sliders = 0
			self.num_spinners = 0
			self.max_combo = 0
			self.num_objects = 0

			# Slider data
			class slider_data:
				def __init__(self, s_type, points, repeats, length):
					self.s_type = s_type
					self.points = points
					self.repeats = repeats
					self.length = length

			# Hit Object
			# 1 = Circle
			# 2 = Slider
			# 3 = Spinner
			self.objects = []
			ho_num = 0
			class hit_object:
				def __init__(self,pos,time,h_type,end_time,slider):
					self.pos = pos
					self.time = time
					self.h_type = h_type
					self.end_time = end_time
					self.slider = slider


			# Timing points
			self.timing_points = []
			tp_num = 0
			class timing_point:
				def __init__(self,time,ms_per_beat,inherit):
					self.time = time
					self.ms_per_beat = ms_per_beat
					self.inherit = inherit

			# Some init variables
			tp_sec = False
			ho_time = False
			valid = False

			# Gathering Metadata
			def metadata(self,line):
				if "Title:" in line:
					self.title = line.split("Title:")[1].split("\r")[0].split("\n")[0]
					#print "Title: "+self.title
				elif "Artist:" in line:
					self.artist = line.split("Artist:")[1].split("\r")[0].split("\n")[0]
					#print "Artist: "+self.artist
				elif "Creator:" in line:
					self.creator = line.split("Creator:")[1].split("\r")[0].split("\n")[0]
					#print "Mapper: "+self.creator
				elif "Version:" in line:
					self.version = line.split("Version:")[1].split("\r")[0].split("\n")[0]
					#print "Dfifficulty: "+self.version
			# Gather difficulty -> remember to check for exceptions
			def difficulty(self,line):
				if "HPDrainRate:" in line:
					self.hp = float(line.split(":")[1].split("\n")[0])
					#print "HP: "+str(self.hp)
				elif "CircleSize:" in line:
					self.cs = float(line.split(":")[1].split("\n")[0])
					#print "CS: "+str(self.cs)
				elif "OverallDifficulty:" in line:
					self.ar = float(line.split(":")[1].split("\n")[0])
					self.od = float(line.split(":")[1].split("\n")[0])
					#print "OD: "+str(self.od)
				elif "ApproachRate:" in line:
					self.ar = float(line.split(":")[1].split("\n")[0])
					#print "AR: "+str(self.ar)
				elif "SliderMultiplier:" in line:
					self.sv = float(line.split(":")[1].split("\n")[0])
					#print "SV: "+str(self.sv)
				elif "SliderTickRate:" in line:
					self.tick_rate = float(line.split(":")[1].split("\n")[0])
					#print "TR: "+str(self.tick_rate)

			# Parse the tp object
			def tp_ptr(self,line):
				temp_tp = line.split("\r")[0].split("\n")[0].split(",")
				
				if temp_tp[0] != '':
					if len(temp_tp) < 3:
						self.timing_points.append(timing_point(temp_tp[0],temp_tp[1],0))
					else:
						self.timing_points.append(timing_point(temp_tp[0],temp_tp[1],temp_tp[6]))
					#print timing_points[tp_num].ms_per_beat

			# Parse the HO. This may take a while
			def ho_ptr(self,line):
				# Start to global stuff. Need to learn more about this
				# Split commas for each line which should be a hit object
				temp_tp = line.split("\r")[0].split("\n")[0].split(",")
				# Only if the line is not null do something
				if temp_tp[0] != '':
					# Set variables to send to hit object
					pos = [temp_tp[0],temp_tp[1]]
					time = temp_tp[2]
					h_type = temp_tp[3]
					end_time = 0
					slider = 0
					slider_true = 0
					if len(line.split("|")) > 1:
						slider_true = 1

					#Circle type
					if h_type == "1" or h_type == "5" or (slider_true == 0 and int(h_type) > 12):
						self.num_circles += 1
						h_type = 1
					#Slider type. Need to do some more math on sliders
					elif h_type == "2" or h_type == "6" or slider_true:
						#print "Found slider beginning analysis..."
						self.num_sliders += 1
						h_type = 2
						pos_s = []
						# split into pipeline for slider logic
						sl_line = line.split("\r")[0].split("\n")[0].split("|")
						sl_type = sl_line[0][len(sl_line[0])-1]
						sl_line = sl_line[1:]
						counter = 0
						# add first slider point
						pos_s.append(pos)
						# iterate line for the rest of the slider points
						l_pos = None
						for l_pos in sl_line:
							pos_s.append([l_pos.split(":")[0],l_pos.split(":")[1].split(",")[0]])
							if len(l_pos.split(",")) > 2:
								break
						if l_pos:
							repeats = float(l_pos.split(",")[1])
							length = float(l_pos.split(",")[2])
						else:
							self.num_circles += 1
							h_type = 1
							self.num_objects += 1
							self.max_combo += 1
							self.objects.append(hit_object(pos,time,h_type,end_time,slider))
							return
						#print "Repeats: "+repeats+" Length: "+length+" Points: "
						#print pos_s
						time_p = self.timing_points[0]
						parent = self.timing_points[0]
						# Get timing point
						for tp in self.timing_points:
							if float(tp.time) > float(time):
								break
							time_p = tp
						# Get the parent point
						for tp in self.timing_points:
							if int(tp.inherit) == 1:
								parent = tp
							if tp == time_p:
								break
						# Begin to calculte the amount of ticks for max combo
						sv_mult = 1
						if time_p.inherit == "0" and float(tp.ms_per_beat) < 0:
							sv_mult = (-100.0 / float(time_p.ms_per_beat))
						px_per_beat = self.sv * 100.0 * sv_mult
						num_beats = (length * repeats) / px_per_beat
						duration = math.ceil(num_beats * float(parent.ms_per_beat))
						end_time = float(time) + duration
						slider = slider_data(sl_type,pos_s,repeats,length)
						ticks = math.ceil((num_beats - 0.1) / repeats * self.tick_rate)
						ticks -= 1
						raw_ticks = ticks
						ticks *= repeats
						ticks += repeats + 1
						self.max_combo += ticks - 1




					#Spinner type.
					elif h_type == "8" or h_type == "12":
						self.num_spinners += 1
						h_type = 3
					else:
						print("HELP "+h_type)
					self.num_objects += 1
					self.max_combo += 1
					self.objects.append(hit_object(pos,time,h_type,end_time,slider))

			# Begin to parse beatmap
			try:
				for line in self.searchfile:
					# Gather metadata
					metadata(self,line)
					# Gather Difficulty information
					difficulty(self,line)
					#print "AR: "+str(self.ar)
					if ho_time:
						ho_ptr(self,line)
						ho_num += 1
					if "[HitObjects]" in line:
						ho_time = True
					if "osu file format v" in line:
						valid = True
					if "Mode: 1" in line or "Mode: 2" in line or "Mode: 3" in line:
						valid = False
					# Section for timing points
					if tp_sec:
						tp_ptr(self,line)
						tp_num += 1
					if "[TimingPoints]" in line:
						tp_sec = True
					if tp_sec and (line == "\n" or line == "\r\n" or line == ""):
						tp_sec = False
				#print "Circles: "+str(self.num_circles)+" Sliders: "+str(self.num_sliders)+" Spinners: "+str(self.num_spinners)
				#print "Max combo: "+str(self.max_combo)
				if valid != True:
					print("ERROR: Unsupported gamemode")
					raise()
			except:
				print("ERROR: Processing beatmap failed")
				raise()
    
		def apply_mods(self,mods):
			# Ugly shouldput somewhere else
			od0_ms = 79.5
			od10_ms = 19.5
			ar0_ms = 1800
			ar5_ms = 1200
			ar10_ms = 450

			od_ms_step = 6.0
			ar_ms_step1 = 120.0
			ar_ms_step2 = 150.0
			
			if mods.map_changing == 0:
				return

			speed = 1

			if mods.dt or mods.nc:
				speed *= 1.5

			if mods.ht: 
				speed *= 0.75

			self.speed = speed

			od_multiplier = 1

			if mods.hr:
				od_multiplier *= 1.4

			if mods.ez:
				od_multiplier *= 0.5

			self.od *= od_multiplier
			odms = od0_ms - math.ceil(od_ms_step * self.od)

			ar_multiplier = 1

			if mods.hr:
				ar_multiplier = 1.4

			if mods.ez:
				ar_multiplier = 0.5

			self.ar *= ar_multiplier

			arms = (ar0_ms - ar_ms_step1 * self.ar) if self.ar <= 5 else (ar5_ms - ar_ms_step2 * (self.ar-5))

			cs_multipier = 1

			if mods.hr:
				cs_multipier = 1.3

			if mods.ez:
				cs_multipier = 0.5

			odms = min(od0_ms, max(od10_ms,odms))
			arms = min(ar0_ms,max(ar10_ms,arms))

			odms /= speed
			arms /= speed

			self.od = (od0_ms - odms) / od_ms_step

			self.ar = ((ar0_ms - arms) / ar_ms_step1) if self.ar<= 5.0 else (5.0 + (ar5_ms - arms) / ar_ms_step2)
			self.cs *= cs_multipier
			self.cs = max(0.0,min(10.0,self.cs))

			if mods.speed_changing == 0:
				return

			for tp in self.timing_points:
				tp.time = float(tp.time)
				if int(tp.inherit) == 0:
					tp.ms_per_beat = float(tp.ms_per_beat)


			for obj in self.objects:
				obj.time = float(obj.time)
				obj.end_time = obj.end_time

class diff_calc:
	def main(file):
		map = file
		objects = []
		radius = (512 / 16) * (1. - 0.7 * (map.cs - 5) / 5);
		class consts:
			decay_base = [0.3,0.15]

			almost_diameter = 90

			aim_angle_bonus_begin = math.pi / 3;
			speed_angle_bonus_begin = 5 * math.pi / 6;
			timing_threshold = 107;

			stream_spacing = 110
			single_spacing = 125

			min_speed_bonus = 75 # 200bpm
			max_speed_bonus = 45 # 330bpm
			speed_balancing_factor = 40

			weight_scaling = [1400,26.25]

			circlesize_buff_threshhold = 30

		class d_obj:
			def __init__(self,base_object, radius,prev):
				self.radius = float(radius)
				self.ho = base_object
				self.strains = [0, 0]
				self.norm_start  = 0
				self.norm_end = 0
				self.prev = prev
				self.delta_time = 0
				# We will scale distances by this factor, so we can assume a uniform CircleSize among beatmaps.
				self.scaling_factor = 52.0 / self.radius
				if self.radius < consts.circlesize_buff_threshhold:
					self.scaling_factor *= 1 + min((consts.circlesize_buff_threshhold - self.radius), 5) / 50.0
				self.norm_start = [float(self.ho.pos[0]) * self.scaling_factor,float(self.ho.pos[1])*self.scaling_factor]
				self.norm_end = self.norm_start
				self.jump_distance = 0
				self.angle = None
				self.travel_distance = 0
				# Calculate jump distance for objects
				if((self.ho.h_type == 1 or self.ho.h_type == 2) and prev != None ):
					self.jump_distance = math.sqrt(math.pow(self.norm_start[0] - prev.norm_end[0],2) + math.pow(self.norm_start[1] - prev.norm_end[1],2))
				# Not working, need to figure out how sliders work
				if(self.ho.h_type == 2):
					self.comp_slider_pos()
				if(prev != None and prev.prev != None):
					# Calculate angle with lastlast last and base object
					v1 = [prev.prev.norm_start[0] - prev.norm_start[0], prev.prev.norm_start[1] - prev.norm_start[1]]
					v2 = [self.norm_start[0] - prev.norm_start[0], self.norm_start[1] - prev.norm_start[1]]
					dot = v1[0]*v2[0] + v1[1]*v2[1]
					det = v1[0]*v2[1] - v1[1]*v2[0]
					self.angle = abs(math.atan2(det,dot))
				if(prev != None):
					self.delta_time = (int(self.ho.time) - int(prev.ho.time)) / map.speed
					if(self.ho.h_type !=  3):
						# Calculate speed
						self.strains[0] = prev.strains[0]*math.pow(consts.decay_base[0],self.delta_time / 1000.0) + self.calculate_speed(prev)*consts.weight_scaling[0]
						# Calculate aim
						self.strains[1] = prev.strains[1]*math.pow(consts.decay_base[1],self.delta_time / 1000.0) + self.calculate_aim(prev)*consts.weight_scaling[1]

			# needs work. Do not understand how sliders work
			def comp_slider_pos(self):
				approx_rad = self.radius * 3
				if self.ho.slider.length > approx_rad:
					self.travel_distance = self.ho.slider.length


			# Calculate aim strain
			def calculate_aim(self,prev):
				result = 0
				strain_time = max(50,self.delta_time)
				prev_strain_time = max(50,prev.delta_time)
				if(prev != None):
					if(self.angle != None and self.angle > consts.aim_angle_bonus_begin):
						scale = 90
						angle_bonus = math.sqrt(max(prev.jump_distance - scale,0) * math.pow(math.sin(self.angle - consts.aim_angle_bonus_begin),2) * max(self.jump_distance - scale,0))
						result = 1.5 * math.pow(max(0,angle_bonus),0.99) / max(consts.timing_threshold, prev_strain_time)
				jump_dist_exp = math.pow(self.jump_distance,0.99)
				travel_dist_exp = 0
				return max(result + jump_dist_exp / max(strain_time, consts.timing_threshold), jump_dist_exp / strain_time)

			# Calculate speed strain
			def calculate_speed(self,prev):
				distance = min(consts.single_spacing, self.jump_distance)
				strain_time = max(50,self.delta_time)
				delta_time = max(consts.max_speed_bonus,self.delta_time)
				speed_bonus = 1.0
				if(delta_time < consts.min_speed_bonus):
					speed_bonus = 1 + math.pow((consts.min_speed_bonus - delta_time) / consts.speed_balancing_factor,2)
				angle_bonus = 1.0
				if(self.angle != None and self.angle < consts.speed_angle_bonus_begin):
					angle_bonus = 1 + math.pow(math.sin(1.5 * (self.angle - consts.speed_angle_bonus_begin)),2) / 3.57
					if(self.angle < math.pi / 2):
						angle_bonus = 1.28
						if(distance < 90 and self.angle < math.pi / 4):
							angle_bonus += (1 - angle_bonus)*min((90 - distance) / 10, 1)
						elif (distance < 90):
							angle_bonus += (1 - angle_bonus)*min((90 - distance) / 10,1) * math.sin(((math.pi / 2 )- self.angle) / (math.pi / 4))
				return (1 + (speed_bonus - 1)*0.75) * angle_bonus * (0.95 + speed_bonus*math.pow(distance / consts.single_spacing,3.5)) / strain_time

		def calculate_difficulty(type, objects):
			strain_step = 400 * map.speed
			prev = None
			max_strain = 0
			decay_weight = 0.9
			highest_strains = []
			interval_end = math.ceil(float(map.objects[0].time) / strain_step) * strain_step
			for obj in objects:
				while int(obj.ho.time) > interval_end:
					highest_strains.append(max_strain)
					if prev == None:
						max_strain = 0
					else:
						decay = math.pow(consts.decay_base[type],(interval_end - int(prev.ho.time)) / 1000.0)
						max_strain = prev.strains[type] * decay
					interval_end += strain_step
				prev = obj
				max_strain = max(obj.strains[type],max_strain)
			highest_strains.append(max_strain)
			difficulty = 0
			weight = 1.0
			highest_strains = sorted(highest_strains, reverse = True)
			for strain in highest_strains:
				difficulty += weight * strain
				weight *= decay_weight
			return difficulty
		star_scaling_factor = 0.0675
		extreme_scaling_factor = 0.5
		prev = None
		for obj in map.objects:
			new = d_obj(obj, radius,prev)
			objects.append(new)
			prev = new
		aim = calculate_difficulty(1, objects)
		speed = calculate_difficulty(0, objects)
		aim = math.sqrt(aim) * star_scaling_factor
		speed = math.sqrt(speed) * star_scaling_factor
		stars = aim + speed + abs(speed-aim) * extreme_scaling_factor
		return [aim,speed,stars, map]

class pp_calc1:
	class mods:
		def __init__(self):
			self.nomod = 1,
			self.nf = 0
			self.ez = 0
			self.hd = 0
			self.hr = 0
			self.dt = 0
			self.ht = 0
			self.nc = 0
			self.fl = 0
			self.so = 0
			speed_changing = self.dt | self.ht | self.nc
			map_changing = self.hr | self.ez | speed_changing

	def base_strain(strain):
		return math.pow(5.0 * max(1.0, strain / 0.0675) - 4.0, 3.0) / 100000.0

	def acc_calc(c300, c100, c50, misses):
		total_hits = c300 + c100 + c50 + misses
		acc = 0.0
		if total_hits > 0:
			acc = (c50 * 50.0 + c100 * 100.0 + c300 * 300.0) / (total_hits * 300.0)
		return acc

	class pp_calc_result:
		def __init__(self):
			self.acc_percent = 0
			self.pp = 0
			self.aim_pp = 0
			self.speed_pp = 0
			self.acc_pp = 0

	def pp_calc(aim, speed, b, misses, c100, c50, used_mods = mods() ,combo = 0xFFFF, score_version = 1, c300 = 0xFFFF):
		res = pp_calc1.pp_calc_result()
		od = b.od
		ar = b.ar
		circles = b.num_circles

		if c100 > b.num_objects or c50 > b.num_objects or misses > b.num_objects:
			print("Invalid accuracy number")
			return res

		if c300 == 0xFFFF:
			c300 = b.num_objects - c100 - c50 - misses

		if combo == 0xFFFF:
			combo = b.max_combo
		elif combo == 0:
			print("Invalid combo count")
			return res

		total_hits = c300 + c100 + c50 + misses
		if total_hits != b.num_objects:
			print("warning hits != objects")

		if score_version != 1 and score_version != 2:
			print("Score version not found")
			return res

		acc = pp_calc1.acc_calc(c300,c100,c50,misses)
		res.acc_percent = acc * 100.0

		if used_mods.td:
			aim = math.pow(aim, 0.8)

		aim_value = pp_calc1.base_strain(aim)

		total_hits_over_2k = total_hits / 2000.0
		length_bonus = 0.95 + 0.4 * min(1.0, total_hits_over_2k) + (math.log10(total_hits_over_2k) * 0.5 if total_hits > 2000 else 0.0)

		miss_penalty = math.pow(0.97,misses)

		combo_break = math.pow(combo, 0.8) / math.pow(b.max_combo,0.8)

		aim_value *= length_bonus
		aim_value *= miss_penalty
		aim_value *= combo_break
		ar_bonus = 1.0

		if ar > 10.33:
			ar_bonus += 0.3 * (ar - 10.33)
		elif ar < 8:
			ar_bonus += 0.01*(8.0 - ar)

		

		aim_value *= ar_bonus
		hd_bonus = 1.0
		if used_mods.hd:
			hd_bonus = 1.0 + 0.04*(12 - ar)
		aim_value *= hd_bonus

		if used_mods.fl:
			aim_value *= 1.0 + 0.35 * min(1.0,total_hits / 200.0) + ((0.3 * min(1,(total_hits - 200) / 300.0) + ((total_hits - 500) / 1200.0 if total_hits > 500 else 0)) if total_hits > 200 else 0)

		acc_bonus = 0.5 + acc / 2.0

		od_bonus = 0.98 + math.pow(od,2) / 2500.0

		aim_value *= acc_bonus
		aim_value *= od_bonus

		res.aim_pp = aim_value

		speed_value = pp_calc1.base_strain(speed)

		speed_value *= length_bonus
		speed_value *= miss_penalty
		speed_value *= combo_break
		if(ar > 10.33):
			speed_value *= ar_bonus
		speed_value *= hd_bonus
		speed_value *= 0.02 + acc
		speed_value *= 0.96 + (math.pow(od, 2) / 1600)
		
		res.speed_pp = speed_value

		real_acc = 0.0

		if score_version == 2:
			circles = total_hits
			real_acc = acc
		else:
			if circles:
				real_acc = ((c300 - (total_hits - circles)) * 300.0 + c100 * 100.0 + c50 * 50.0) / (circles * 300)
			real_acc = max(0.0,real_acc)

		acc_value = math.pow(1.52163, od) * math.pow(real_acc, 24.0) * 2.83
		
		acc_value *= min(1.15, math.pow(circles / 1000.0, 0.3))

		if used_mods.hd:
			acc_value *= 1.08

		if used_mods.fl:
			acc_value *= 1.02

		res.acc_pp = acc_value

		final_multiplier = 1.12

		if used_mods.nf:
			final_multiplier *= 0.90

		if used_mods.so:
			final_multiplier *= 0.95
		res.pp = math.pow(math.pow(aim_value,1.1) + math.pow(speed_value,1.1) + math.pow(acc_value, 1.1), 1.0 / 1.1) * final_multiplier
		return res;

	def pp_calc_acc(aim, speed, b, acc_percent, used_mods = mods(), combo = 0xFFFF, misses = 0,score_version = 1):
		misses = min(b.num_objects,misses)

		max300 = (b.num_objects - misses)

		acc_percent = max(0.0, min(pp_calc1.acc_calc(max300, 0, 0, misses) * 100.0, acc_percent))

		c50 = 0

		c100 = round(-3.0 * ((acc_percent * 0.01 - 1.0) * b.num_objects + misses) * 0.5)

		if c100 > b.num_objects - misses:
			c100 = 0
			c50 = round(-6.0 * ((acc_percent * 0.01 - 1.0) * b.num_objects + misses) * 0.2);

			c50 = min(max300, c50)
		else:
			c100 = min(max300, c100)

		c300 = b.num_objects - c100 - c50 - misses

		return pp_calc1.pp_calc(aim,speed,b,misses,c100,c50,used_mods, combo, score_version,c300)

class calc:
	def mod_str(mod):
		string = ""
		if mod.nf:
			string += "NF"
		if mod.ez:
			string += "EZ"
		if mod.hd:
			string += "HD"
		if mod.hr:
			string += "HR"
		if mod.dt:
			string += "DT"
		if mod.ht:
			string += "HT"
		if mod.nc:
			string += "NC"
		if mod.fl:
			string += "FL"
		if mod.so:
			string += "SO"
		if mod.td:
			string += "TD"
		return string

	class mods:
		def __init__(self):
			self.nomod = 0,
			self.nf = 0
			self.ez = 0
			self.hd = 0
			self.hr = 0
			self.dt = 0
			self.ht = 0
			self.nc = 0
			self.fl = 0
			self.so = 0
			self.td = 0
			self.speed_changing = self.dt | self.ht | self.nc
			self.map_changing = self.hr | self.ez | self.speed_changing
		def update(self):
			self.speed_changing = self.dt | self.ht | self.nc
			self.map_changing = self.hr | self.ez | self.speed_changing
	mod = mods()

	def set_mods(mod, m):
			if m == "NF":
				mod.nf = 1
			if m == "EZ":
				mod.ez = 1
			if m == "HD":
				mod.hd = 1
			if m == "HR":
				mod.hr = 1
			if m == "DT":
				mod.dt = 1
			if m == "HT":
				mod.ht = 1
			if m == "NC":
				mod.nc = 1
			if m == "FL":
				mod.fl = 1
			if m == "SO":
				mod.so = 1
			if m == "TD":
				mod.td = 1


	def pp(l: str, acc: float = 0, misses: int = 0, c100: int = 0, c50: int = 0, mod_s: str = '', combo: int = 0, sv: int = 1):
		try:
			if mod_s != "":
				mod_s = mod_s.upper()
				mod_s = [mod_s[i:i+2] for i in range(0, len(mod_s), 2)]
				for m in mod_s:
					calc.set_mods(calc.mod, m)
					calc.mod.update()
			map = bm.Beatmap(requests.get(l).text.splitlines())
			if combo == 0 or combo > map.max_combo:
				combo = map.max_combo
			map.apply_mods(calc.mod)
			diff = diff_calc.main(map)
			if acc == 0:
				pp = pp_calc1.pp_calc(diff[0], diff[1], diff[3], misses, c100, c50, calc.mod, combo, sv)
			else:
				pp = pp_calc1.pp_calc_acc(diff[0], diff[1], diff[3], acc, calc.mod, combo, misses, sv)
			return round(pp.pp, 2)
		except: return 0
