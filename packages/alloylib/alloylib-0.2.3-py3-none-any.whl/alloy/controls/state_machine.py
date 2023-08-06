# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

import time
class StateMachine(object):

    def __init__(self, persistent=False, start_state='start_state'):

        self._state_list = {
            'start_state': self._start_state,
            'terminal_state': self._terminal_state
        }
        self.inital_start_state_name = start_state
        self._curr_state_name = self.inital_start_state_name
        self._persistent_flag = persistent
        #run state definition in the end
        self._state_definitions()
        self._initialization()
        self._terminate_flag = False
        self._last_state_change_time_stamp = time.time()
        print("hello")

    def terminated(self):
        return self._terminate_flag

    def _state_definitions(self):
        pass

    def _start_state(self, **kwargs):
        return self._curr_state_name

    def _terminal_state(self, **kwargs):
        self._terminate_flag = True
        return self._curr_state_name

    def _initialization(self):
        self._terminate_flag = False
        self._last_state_change_time_stamp = time.time()

    def _restart(self):
        self._curr_state_name = self.inital_start_state_name
        self._initialization()

    def step(self, **kwargs):

        last_state_name = self._curr_state_name
        #get the current state
        curr_state = self._state_list[self._curr_state_name]
        #run the current state with the given arguments
        next_state_name = curr_state(**kwargs)
        #save the next state name
        self._curr_state_name = next_state_name
        if last_state_name != next_state_name:
            self._last_state_change_time_stamp = time.time()


    def get_time_since_last_state_change(self):
        return time.time() - self._last_state_change_time_stamp

    ## while we can have state machine runs internally,
    ## won't we want it to be effected by the outside environment?
    def run(self, start_state=''):
        if start_state != '':
            self._current_state_name = start_state

        #initialize the state machine to the original configuration
        #if the initialize flag is set
        if not self._persistent_flag:    
            self._restart()

        while(not self.terminated()):
            last_state_name = self._curr_state_name
            self.step()
            print("last state:{}, next state:{}".format(last_state_name, self._curr_state_name))
   
class TimerStateMachine(StateMachine):

    def _state_definitions(self):
        self._state_list['t1'] = self._state_t1
        self._state_list['t2'] = self._state_t2
        self._state_list['t3'] = self._state_t3

    def _start_state(self, **kwargs):
        return 't1'

    def _state_t1(self, **kwargs):
        return 't2'

    def _state_t2(self, **kwargs):
        return 't3'

    def _state_t3(self, **kwargs):
        return 'terminal_state'

class CounterStateMachine(StateMachine):

    def _start_state(self, **kwargs):
        
        if kwargs['counter'] < 5:
            return 'start_state'
        else:
            return 'terminal_state'



def main():
    csm = CounterStateMachine()
    index = 0

    while(not csm.terminated()):
        index += 1
        print(index)
        csm.step(counter=index)
    print('complete')
    print(index)

    tsm = TimerStateMachine()
    tsm.run()


if __name__ == '__main__':
    main()
