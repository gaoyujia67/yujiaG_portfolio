from itertools import repeat
import requests
import time
import datetime


class lighting:
    '''
    this is a class to use api to control light strip
    where self.values is a list of numbers between 0 and 255 
    controling the color of lights, 
    each four numbers for rgb and white color of a light.
    '''

    def __init__(self):
        '''
        set the url of api and initial color of lights
        '''
        self.lights_num=300
        api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiamlhd2VpaHVAdW1pY2guZWR1In0.VjotHXi79TN0-8kAewWfPlO9NOYEaszabyEyIzZu-U0"
        device_name = "ELM"
        self.url = f"https://si568.umsi.run/change?key={api_key}&device={device_name}"
        self.shuturl = f"https://si568.umsi.run/off?key={api_key}&device={device_name}"
        self.initial_value=[0,0,0,0]
        self.values=self.initial_value*self.lights_num


    def push_api(self):
        '''
        Converts self.values from list of numbers to string format
        and sends it to the API.
        '''
        values=', '.join(map(str, self.values))
        requests.post(self.url, json={'values': values})


    def shut_off(self):
        '''Turn off the whole light strip.'''
        requests.post(self.shuturl)


    def all_change(self, value):
        """
        Changes the color of all light nodes to the same specified color.

        Parameters:
        - value (list of int): A list of integers representing the color to set (e.g., RGB and brightness).
        """
        if not (isinstance(value, list) and len(value) == 4 and all(isinstance(x, int) for x in value)):
            raise ValueError('value is not a list of 4 int')
        if not all(0 <= num <= 255 for num in value):
            raise ValueError('some number is not between 0 and 255')
        self.values=value*(self.lights_num)
        self.push_api()
        

    def change_every_other(self, value1, value2):
        """
        Alternates the color of every other light node between two specified colors.

        Parameters:
        - value1 (list of int): The first color value to alternate.
        - value2 (list of int): The second color value to alternate.
        """
        if not (isinstance(value1, list) and len(value1) == 4 and all(isinstance(x, int) for x in value1)):
            raise ValueError('value1 is not a list of 4 int')
        if not all(0 <= num <= 255 for num in value1):
            raise ValueError('some number in value1 is not between 0 and 255')
        if not (isinstance(value2, list) and len(value2) == 4 and all(isinstance(x, int) for x in value2)):
            raise ValueError('value2 is not a list of 4 int')
        if not all(0 <= num <= 255 for num in value2):
            raise ValueError('some number in value2 is not between 0 and 255')
        value=value1+value2
        self.values=value*int(self.lights_num/2)
        self.push_api()
    

    def general_pattern(self, values):
        """
        Lights the strip in a given color sequence. The sequence is repeated to cover the entire length of the light strip.

        Parameters:
        - values (list of int): A list of integers representing the sequence of colors.
        """
        if not (isinstance(values, list) and all(isinstance(x, int) for x in values)):
            raise ValueError('values is not a list of int')
        if not all(0 <= num <= 255 for num in values):
            raise ValueError('some number in values is not between 0 and 255')
        if len(values)%4!=0:
            raise ValueError('lenght of values is not a multiple of 4')
        lights=len(values)/4
        if lights>self.lights_num:
            raise ValueError('The number of lights is not enough to display the pattern.')
        repeat=int(self.lights_num/lights)+1
        self.values=(values*repeat)[:self.lights_num*4]
        self.push_api()


    def fade_every_other(self):
        """
        Reduces the brightness of every other light node by a third to create a fading effect.
        """
        for i in range(self.lights_num):
            if i % 2 == 0: 
                for j in range(4):
                    index=4*i+j
                    self.values[index]=int(self.values[index]/3)
        self.push_api()
            

    def change_every_other_loop(self, value1, value2, second=10):
        '''Autometically alter the color of adjacent light nodes.
        Default altering period is 10 seconds.
        '''
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=second)
        while end_time > datetime.datetime.now():
            self.change_every_other(value1, value2)
            time.sleep(1)
            self.change_every_other(value2, value1)
            time.sleep(1)
        self.shut_off()
        

    def grow(self, value):
        """
        Gradually illuminate all light nodes starting from one end of the light strip.

        Parameters:
        - value (list of int): color of the light nodes.
        """
        repeat = 1
        while repeat <= self.lights_num + 1:
            self.values[0:4*repeat] = value*repeat
            self.push_api()
            repeat += 5
            time.sleep(0.01)
        time.sleep(2)
        self.shut_off()
    
    def chase(self, value):
        '''
        Simulates a sequence of 4 light nodes chasing each other along a light stripe.

        Parameters:
        - value (list of int): color of the light nodes
        '''
        repeat = 4
        for i in range(0, self.lights_num):
            self.values[0:4*i*repeat] = self.initial_value*i*repeat
            self.values[i*4:4*(i+1)*repeat] = value*repeat
            self.push_api()
            time.sleep(0.01)
        time.sleep(2)
        self.shut_off()


    def breath(self, fade=True, second=1.4):
        """
        Creates a 'breathing' effect where the brightness of the lights increases and decreases.

        Parameters:
        - fade (bool): If True, the lights will fade out. If False, they will fade in.
        - second (float): The duration of one breath cycle in seconds.
        """
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=second)
        sleep_time=second/6
        while end_time > datetime.datetime.now():
            if fade:
                for i in range(4):
                    time.sleep(sleep_time)
                    self.values = [int(x/1.1) for x in self.values]
                    self.push_api()
            else:
                for i in range(4):
                    time.sleep(sleep_time)
                    self.values = [int(x*1.1) for x in self.values]
                    self.push_api()
            
            
if __name__ == "__main__":
    lit=lighting()
    rainbow_pattern=[255, 0, 0, 0, 255, 165, 0, 0, \
        255, 255, 0, 0, 0, 128, 0, 0, \
        0, 100, 100, 0, 0, 0, 255, 0, 148, 0, 211, 0]
    
    # Change the color of all light nodes
    lit.all_change([150, 0, 0, 100])
    time.sleep(5)  # Light last for 5 seconds
    lit.shut_off()
    
    # Alter the color of every other light nodes
    lit.change_every_other_loop([251, 236, 93, 100], [0, 117, 228, 0])

    # A rainbow sequence
    lit.general_pattern(rainbow_pattern)

    # Fade the color density of every other light nodes after lightening all of them
    lit.all_change([150, 0, 0, 100])
    lit.fade_every_other()
    time.sleep(3)  # Light last for 3 seconds
    lit.shut_off()

    # Light grow
    lit.grow([150, 0, 0, 100])

    # Light chase
    lit.chase([150, 0, 0, 100])

    # Light breathe
    flag=True
    while(1):
        lit.breath(flag, 0.6)
        flag=not flag
        lit.breath(flag, 0.6)
        flag=not flag
    lit.breath('a')
    time.sleep(3)
    lit.shut_off()
    
    
