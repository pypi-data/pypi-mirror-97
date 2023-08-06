import copy
import pretty_midi
__copyright__    = 'Copyright (C) 2020 CyberWindBell Project'
__version__      = '0.0.2'
__license__      = 'MIT'
__author__       = 'cwbp'
__author_email__ = 'cwbp@cwbp.com'
__url__          = 'http://github.com/cwbp/mdpw'

__all__ = ['mdpw']

_n = 'n'
_s = 's'
_c = 'c'

_i_type = 0
_i_pitch = 1
_i_duration = 2
_i_velocity = 3
_i_inst = 4
_i_start = 5
_i_notetype = 6

_on = "on"
_off = "off"
_delta = 0.0001

#def _deep_copy(data):

def add_start(data, start, defv):
        d = data
        if d[_i_type] == _n:
            for ii in range(1,len(defv)):
                #print(ii, d, defv)
                if len(d) <= ii:
                    d.append(defv[ii])
                else:
                    defv[ii] = d[ii]
            if len(d) <= _i_start:
                d.append(start)
            else:
                d[_i_start] = float(start)
            #print("duration:", float(d[_i_duration]))
            return float(d[_i_duration])
        if d[_i_type] == _c:
            ld = 0.0
            for ii in range(1, len(d)):
                dd = copy.copy(d[ii])
                d[ii] = dd
                td = add_start(dd, start, defv)
                if ld < td:
                    ld = td
            return ld
        if d[_i_type] == _s:
            ld = 0.0
            for ii in range(1, len(d)):
                dd = copy.copy(d[ii])
                d[ii] = dd
                td = add_start(dd, start, defv)
                start += td
                ld += td
            return ld
        return 0.0
def insert_event(ret, event):
    #print("event:", event, ret)
    if not event[_i_inst] in ret:
        ret[event[_i_inst]] = [event]
        return
    data = ret[event[_i_inst]]
    for i in range(len(data)):
        if data[i][_i_start] > event[_i_start] or (data[i][_i_start] == event[_i_start] and
            ( event[_i_notetype] == _on or data[i][_i_start] ==_off)):
                data.insert(i, event)
                return
    data.append(event)
def split_by_inst(data, ret):
    for d in data:
        if d[_i_type]== _s or  d[_i_type]== _c:
            split_by_inst(d[1:], ret) 
        else:
            dd = copy.copy(d)
            dd.append(_on)
            insert_event(ret, dd) #noteon
            #print("d:",d)
            #d[_i_start] += d[_i_duration]-_delta
            #d.append(_off)
            #insert_event(ret, d) #noteoff
def remove_noteoff(track_data):
    pass
def compile(data, tempo):
    ldata = copy.deepcopy(data)
    d = add_start(ldata, 0.0, ['n', 64, 1, 64,1])
    #print(ldata, tempo, d)
    ret = {}
    split_by_inst(ldata, ret)
    #print(ret)
    mfile =  pretty_midi.PrettyMIDI()
    for inst in ret:
        i = inst if inst < 129 else 0
        track = pretty_midi.Instrument(program=i, is_drum=(inst==129))
        for n in ret[inst]:
                st = n[_i_start]*60/tempo
                dt = n[_i_duration]*60/tempo-_delta
                track.notes.append(pretty_midi.Note(
                    pitch = n[_i_pitch], velocity=n[_i_velocity], start = st, end = st+dt
                ))
        mfile.instruments.append(track)
    return mfile