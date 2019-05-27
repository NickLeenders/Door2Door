# -*- coding: utf-8 -*-



#taking loading due to braking as 0.75=0/75g

g = 9.80665
acc_g = 0.75
brake_g = 0.75




def wheel_loading(a,b,c,mass,brake_g,acc_g):
    w = mass * g
    #moments = weight * c + y * b - x * a
    y_load_b = ( w * (a - (brake_g * c)))/(b+a)
    x_load_b = w - y_load_b
    y_load_a = ( w * (a + (brake_g * x)))/(b+a)
    x_load_a = w - y_load_a
    load_dict = {"front_load_min": x_load_a , "front_load_max": x_load_b, "back_load_min": x_load_b, "back_load_max": x_load_a}
    #acceleration g
    return(load_dict)
    


    

