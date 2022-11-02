import pygame
import random
import math
pygame.init()


#setup pygame window and introduce global variables like window size, colors

class DrawInformation:
	#class attributes, global body
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	CREAM = 255, 253, 208
	BACKGROUND_COLOR = CREAM

	GRADIENTS = [
		(240,248,255),
		(230,230,250),
		(135,206,250)
	]
	FONT = pygame.font.SysFont('calibri', 23, bold=True)
	LARGE_FONT = pygame.font.SysFont('calibri', 33, bold=True)
	SIDE_PAD = 100  #padding on left and right=50 pixels
	TOP_PAD = 150

#pygame window width, height, and the list we will pass of numbers to be sorted.
	def __init__(self, width, height, lst):
		self.width = width
		self.height = height
#setting up the window
		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("SORTING ALGORITHM VISUALIZER")
		self.set_list(lst)

	def set_list(self,lst):
		#rods
		#width depends on the total number of values in the list
		#height depends on the range of values in the list
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)
		
		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		#reason to divide it by the given calculation is because:
		#the diff of max value and min value is going to tell the number of values in the range.

		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending ):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	controls = draw_info.LARGE_FONT.render("SORTING ALGORITHM VISUALIZER", 1, draw_info.GREEN)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 5))

	title = draw_info.FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 35))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending order | D - Descending order", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 55))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))
	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
	#loop through the entire list
	#enumerate gives the index as well as value in the list
	for i,val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
		color = draw_info.GRADIENTS[i % 3]


		if i in color_positions:
			color = color_positions[i]

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()
#GENERATE STARTING LIST
#randomly generating a list to sort
def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst

def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst
	for i in range(len(lst)-1):
		for j in range(len(lst)-1-i):
			num1 = lst[j]
			num2 = lst[j+1]

			if (num1>num2 and ascending) or (num1<num2 and not ascending):
				lst[j], lst[j+1] = lst[j+1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
				#yield: pause but store the current state of the ftn, and then resume it
				yield True

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i>0 and lst[i-1] > current and ascending
			descending_sort = i>0 and lst[i-1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i-1]
			i = i-1
			lst[i] = current
			draw_list(draw_info, {i:draw_info.GREEN, i-1: draw_info.RED}, True)
			yield True

	return lst


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for ind in range(len(lst)):
        min_index = ind
 
        for jn in range(ind + 1, len(lst)):
            # select the minimum element in every iteration
            if (lst[jn]<lst[min_index] and ascending) or (lst[jn]>lst[min_index] and not ascending):
                min_index = jn
         # swapping the elements to sort the array
        (lst[ind], lst[min_index]) = (lst[min_index], lst[ind])
        draw_list(draw_info, {ind:draw_info.GREEN, min_index: draw_info.RED}, True)
        yield True
    return lst

#main driver code

def main():
	run = True
	#regulates how quickly this loop can run
	clock = pygame.time.Clock()

	#create the starting list
	n = 50
	min_val = 0
	max_val = 100
	lst = generate_starting_list(n, min_val, max_val)

	#instantiating the DrawInformation method: creating the window by providing the width, height and lst
	draw_info = DrawInformation(800, 600, lst)
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None


	while run:
		clock.tick(6)   #max num of time this loop can run in a second

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting=False
		else:
			draw(draw_info, sorting_algo_name, ascending)
		#this will update the display screen
		#draw(draw_info)

		#pygame.display.update()

		for event in pygame.event.get():   #list of all of the events that have occured since last loop9last time this was called)
			#hitting the red x in the top right corner
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			#When R is pressed, list is Reset to original list 
			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info,ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
				ascending = False
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
				ascending = False
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"
				ascending = False
	pygame.quit()	

#these statements make sure that we are running this module by clicking the run button
if __name__ == "__main__":
	main()
