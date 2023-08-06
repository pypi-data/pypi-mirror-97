from trodesnetwork import socket

from enum import Enum, auto

class CurrentScaling(Enum):
    max10nA = auto()
    max20nA = auto()
    max50nA = auto()
    max100nA = auto()
    max200nA = auto()
    max500nA = auto()
    max1uA = auto()
    max2uA = auto()
    max5uA = auto()
    max10uA = auto()

class GlobalStimulationSettings:
    def setVoltageScale(self, scaleValue):
        self.scaleValue = scaleValue

class StimulationCommand:
    def setBiphasicPulseShape(self, leadingPulseWidth_Samples,
            leadingPulseAmplitude, secondPulseWidth_Samples,
            secondPulseAmplitude, interPhaseDwell_Samples, pulsePeriod_Samples,
            startDelay_Samples):
        self.leadingPulseWidth_Samples = leadingPulseWidth_Samples
        self.leadingPulseAmplitude = leadingPulseAmplitude
        self.secondPulseWidth_Samples = secondPulseWidth_Samples
        self.secondPulseAmplitude = secondPulseAmplitude
        self.interPhaseDwell_Samples = interPhaseDwell_Samples
        self.pulsePeriod_Samples = pulsePeriod_Samples
        self.startDelay_Samples = startDelay_Samples

    def setNumPulsesInTrain(self, numPulsesInTrain):
        self.numPulsesInTrain = numPulsesInTrain

    def setChannels(self, cathodeID, cathodeChannel, anodeID, anodeChannel):
        self.cathodeChannel = cathodeChannel
        self.anodeChannel = anodeChannel
        self.cathodeNtrodeID = cathodeID
        self.anodeNtrodeID = anodeID

    def setGroup(self, group):
        self.group = group

    def setSlot(self, slot):
        self.slot = slot

class TrodesHardware:
    def __init__(self):
        self.service = socket.ServiceConsumer('trodes.hardware')

    def settle_command_triggered(self):
        data = ['tag', 'HRSettle']
        return self.service.request(data)

    def __startstop(self, startstop, slotgroup, number):
        data = [
            'tag',
            'HRStartStopCommand',
            {'startstop': startstop, 'slotgroup': slotgroup, 'number': number}
            ]
        return self.service.request(data)

    def sendStimulationStartSlot(self, slot):
        return self.__startstop('START', 'SLOT', slot)

    def sendStimulationStartGroup(self, group):
        return self.__startstop('START', 'GROUP', group)

    def sendStimulationStopSlot(self, slot):
        return self.__startstop('STOP', 'SLOT', slot)

    def sendStimulationStopGroup(self, group):
        return self.__startstop('STOP', 'GROUP', group)

    def sendStimulationParams(self, params):
        '''
        Takes StimulationCommand params
        '''
        data = [
            'tag',
            'HRSet',
            {
                '_group': params.group,
                'slot': params.slot,
                'cathodeChannel': params.cathodeChannel,
                'anodeChannel': params.anodeChannel,
                'cathodeNtrodeID': params.cathodeNtrodeID,
                'anodeNtrodeID': params.anodeNtrodeID,
                'leadingPulseWidth_Samples': params.leadingPulseWidth_Samples,
                'leadingPulseAmplitude': params.leadingPulseAmplitude,
                'secondPulseWidth_Samples': params.secondPulseWidth_Samples,
                'secondPulseAmplitude': params.secondPulseAmplitude,
                'interPhaseDwell_Samples': params.interPhaseDwell_Samples,
                'pulsePeriod_Samples': params.pulsePeriod_Samples,
                'startDelay_Samples': params.startDelay_Samples,
                'numPulsesInTrain': params.numPulsesInTrain
            }
            ]
        return self.service.request(data)

    def sendClearStimulationParams(self, slot):
        '''
        clear any existing commands in the given slot
        '''
        data = [
            'tag',
            'HRClear',
            { 'number': slot }
            ]
        return self.service.request(data)

    def sendGlobalStimulationSettings(self, settings):
        def getScaleValue(scaleValue):
            if scaleValue == CurrentScaling.max10nA:
                return 'max10nA'
            elif scaleValue == CurrentScaling.max20nA:
                return 'max20nA'
            elif scaleValue == CurrentScaling.max50nA:
                return 'max50nA'
            elif scaleValue == CurrentScaling.max100nA:
                return 'max100nA'
            elif scaleValue == CurrentScaling.max200nA:
                return 'max200nA'
            elif scaleValue == CurrentScaling.max500nA:
                return 'max500nA'
            elif scaleValue == CurrentScaling.max1uA:
                return 'max1uA'
            elif scaleValue == CurrentScaling.max2uA:
                return 'max2uA'
            elif scaleValue == CurrentScaling.max5uA:
                return 'max5uA'
            elif scaleValue == CurrentScaling.max10uA:
                return 'max10uA'
            else:
                raise ValueError("unknown scaleValue enum")

        data = [
            'tag',
            'HRSetGS',
            { 'scaleValue': getScaleValue(settings.scaleValue) }
            ]
        return self.service.request(data)

    def global_stimulation_command(self, resetSequencerCmd,
            killStimulationCmd, clearDSPOffsetRemovalCmd,
            enableStimulation):
        data = [
            'tag',
            'HRSetGC',
            {
                'resetSequencerCmd': resetSequencerCmd,
                'killStimulationCmd': killStimulationCmd,
                'clearDSPOffsetRemovalCmd': clearDSPOffsetRemovalCmd,
                'enableStimulation': enableStimulation,
            }
            ]
        return self.service.request(data)

    def ecu_shortcut_message(self, fn):
        data = [
            'tag',
            'HRSCTrig',
            { 'fn': fn }
            ]
        return self.service.request(data)

class TrodesInfoRequester:
    def __init__(self):
        self.service = socket.ServiceConsumer('trodes.info')

    def __request(self, item):
        data = { 'request': item }
        return self.service.request(data)

    def request_time(self):
        return self.__request('time')[2]['time']

    def request_timerate(self):
        return self.__request('timerate')[2]['timerate']

    def request_config(self):
        return self.__request('config')

class TrodesAnnotationRequester:
    def __init__(self):
        self.service = socket.ServiceConsumer('trodes.annotation')

    def request_annotation(self, timestamp, sender, event):
        data = {
            'timestamp': timestamp,
            'sender': sender,
            'event': event
        }
        return self.service.request(data)

class TrodesAcquisitionRequester:
    def __init__(self):
        self.service = socket.ServiceConsumer('trodes.acquisition.service')

    def __request(self, command, timestamp):
        data = { 'command': command, 'timestamp': timestamp }
        return self.service.request(data)

    def request_play(self):
        return self.__request('play', 0)

    def request_pause(self):
        return self.__request('pause', 0)

    def request_stop(self):
        return self.__request('stop', 0)

    def request_seek(self, timestamp):
        return self.__request('seek', timestamp)

class TrodesEventSubscriber:
    def __init__(self):
        self.subscriber = socket.SourceSubscriber('trodes.events')

    def receive():
        return self.subscriber.receive()

class TrodesAcquisitionSubscriber:
    def __init__(self):
        self.subscriber = socket.SourceSubscriber('trodes.acquisition')

    def receive():
        return self.subscriber.receive()

class TrodesSourceStatusSubscriber:
    def __init__(self):
        self.subscriber = socket.SourceSubscriber('trodes.source.pub')

    def receive():
        return self.subscriber.receive()
