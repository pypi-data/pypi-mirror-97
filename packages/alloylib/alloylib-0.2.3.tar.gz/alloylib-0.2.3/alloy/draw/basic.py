# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

import numpy as np 
import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

import matplotlib.pyplot as plt


def draw_point_on_img(canvas, pt_, color):
    """ Given a 2D array canvas, color a pixel according to the x,y position.

    parameters:
    -----------
    canvas: numpy.array
        A n x m x c array, where c is the dimensions of color
    pt: tuple of ints
        The (x,y) position to draw on

    returns
    -------
    Bool
        Whether it was drew on successfully.

    """
    
    pt = (int(pt_[0]),int(pt_[1]))

    if pt[0] < np.size(canvas, 1) and pt[0] >= 0 and pt[1] < np.size(canvas, 0) and pt[1] >= 0:
        canvas[pt[1], pt[0],:] = color
        return True
    return False

class CheckableQueue(queue.Queue): # or OrderedSetQueue
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue

def draw_circle_on_img(canvas, center_, radius=2,color=[0,255,255]):
    """Draw a circle with given radius and color on the canvas with (x,y) center
    """

    center = (int(center_[0]),int(center_[1]))


    search_queue = CheckableQueue()
    search_queue.put(center)
    visited_list = []
    while not search_queue.empty():
        #get the current element
        cur_ele = search_queue.get()
        #add to visited list
        visited_list.append(cur_ele)
        #draw the dot
        canvas[cur_ele[1],cur_ele[0],:] = color
        #loop through possible neighbors
        for (dx,dy) in [(-1, 0),(1, 0),(0,-1),(0,1)]:
            neighbor_loc = (cur_ele[0] + dx, cur_ele[1] + dy)
            #check the distance to make sure the distance is still less than desired
            nei_dist = np.sqrt(np.square(neighbor_loc[0] - center[0]) + np.square(neighbor_loc[1] - center[1]))
            if nei_dist <= radius and not search_queue.__contains__(neighbor_loc) and not neighbor_loc in visited_list:
                if neighbor_loc[0] < np.size(canvas, 1) and neighbor_loc[0] >= 0 and neighbor_loc[1] < np.size(canvas, 0) and neighbor_loc[1] >= 0:
                    search_queue.put(neighbor_loc)



def draw_rectangle_on_img(canvas, pt1, pt2, color=[0,0,0]):
    """
    Draw rectangle where pt1 is on the upper left and pt2 is the bottom right
    """

    for y in range(pt2[1], pt1[1]):
        for x in range(pt1[0], pt2[0]):
            draw_point_on_img(canvas, x, y, color)


def draw_line_on_img(canvas, start_pt_, end_pt_, color=[0,1,0]):
    """
    Given two points, this algorithm will plot that line
    modified from 
    http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
    """

    start_pt = (int(start_pt_[0]),int(start_pt_[1]))
    end_pt = (int(end_pt_[0]),int(end_pt_[1]))


    delta_x = end_pt[0] - start_pt[0]
    delta_y = end_pt[1] - start_pt[1]

    #check whether to swap it
    steep_flag = np.abs(delta_y) > np.abs(delta_x)
    if steep_flag:
        #swap x, y
        start_pt = (start_pt[1], start_pt[0])
        end_pt = (end_pt[1], end_pt[0])

    swap_flag = False
    if start_pt[0] > end_pt[0]:
        #swap starting and ending point
        tmp = start_pt
        start_pt = end_pt
        end_pt = tmp

    #recalculate the delta
    delta_x = end_pt[0] - start_pt[0]
    delta_y = end_pt[1] - start_pt[1]

    err = int(delta_x / 2.0)
    ystep = 1 if start_pt[1] < end_pt[1] else -1

    y = start_pt[1]
    for x in range(start_pt[0], end_pt[0] + 1):
        #plot point
        if steep_flag:
            draw_point_on_img(canvas, (y, x), color)
        else:
            draw_point_on_img(canvas, (x, y), color)
        #calculate the new error
        err -= np.abs(delta_y)
        if err < 0:
            y += ystep
            err += delta_x
    return


def display_canvas(canvas, origin='upper'):

    #plt.ion()
    plt.imshow(canvas, origin=origin)
    plt.draw()

    # plt.imshow(canvas, origin=origin)
    # plt.show()

# img = np.ones([900,900,3], dtype=np.uint8)
# img = img * 255
# import yaml
# with open('gridworld_8_8.yaml','r') as data:
# #with open('NSH_A.yaml','r') as data:
#     info = yaml.load(data)
#     #convert into dict for easy process
#     info_dict = {}
#     for node in info['nodes']:
#         info_dict[node['id']] = node

#     width = 10
#     mod = 10
#     x_offset = 0
#     y_offset = 0
#     for node in info['nodes']:
#         infl_x = node['_x'] * mod + width + x_offset
#         infl_y = node['_y'] * mod + width + y_offset
#         start_pt = (infl_x, infl_y)        
#         for con in node['connections']:
#             end_node = info_dict[con]
#             end_pt = (end_node['_x']*mod + width + x_offset, end_node['_y'] * mod + width  + y_offset)
            
#             #draw ticker line instead
#             if (end_pt[0] - start_pt[0]) == 0:
#                 #vertical line 
#                 pt1 = (end_pt[0] - width/2, start_pt[1] if start_pt[1] > end_pt[1] else end_pt[1] )
#                 pt2 = (end_pt[0] + width/2, start_pt[1] if start_pt[1] < end_pt[1] else end_pt[1] )

#                 draw_rectangle_on_img(img, pt1, pt2)
#             else:
#                 #horizontal line
#                 pt1 = (start_pt[0] if start_pt[0] < end_pt[0] else end_pt[0] , end_pt[1] + width/2)
#                 pt2 = (start_pt[0] if start_pt[0] > end_pt[0] else end_pt[0] , end_pt[1] - width/2)
#                 draw_rectangle_on_img(img, pt1, pt2)     
#             #draw_line_on_img(img, start_pt, end_pt)           

#         #draw_circle_on_img(img,infl_x,infl_y,5)
#     #print(info)

