from NetworkSimulator import NetworkSimulator
from Queue import Queue
import random
from Event import Event
from Packet import Packet
from message import Message
from EventListImpl import EventListImpl
import random
import math

import time
import atexit
class StudentNetworkSimulator(NetworkSimulator, object):


    """
	* Predefined Constants (static member variables):
     *
     *   int MAXDATASIZE : the maximum size of the Message data and
     *                     Packet payload
     *
     *   int A           : a predefined integer that represents entity A
     *   int B           : a predefined integer that represents entity B
     *
     *
     * Predefined Member Methods:
     *
     *  stopTimer(int entity): 
     *       Stops the timer running at "entity" [A or B]
     *  startTimer(int entity, double increment): 
     *       Starts a timer running at "entity" [A or B], which will expire in
     *       "increment" time units, causing the interrupt handler to be
     *       called.  You should only call this with A.
     *  toLayer3(int callingEntity, Packet p)
     *       Puts the packet "p" into the network from "callingEntity" [A or B]
     *  toLayer5(int entity, String dataSent)
     *       Passes "dataSent" up to layer 5 from "entity" [A or B]
     *  getTime()
     *       Returns the current time in the simulator.  Might be useful for
     *       debugging.
     *  printEventList()
     *       Prints the current event list to stdout.  Might be useful for
     *       debugging, but probably not.
     *
     *
     *  Predefined Classes:
     *
     *  Message: Used to encapsulate a message coming from layer 5
     *    Constructor:
     *      Message(String inputData): 
     *          creates a new Message containing "inputData"
     *    Methods:
     *      boolean setData(String inputData):
     *          sets an existing Message's data to "inputData"
     *          returns true on success, false otherwise
     *      String getData():
     *          returns the data contained in the message
     *  Packet: Used to encapsulate a packet
     *    Constructors:
     *      Packet (Packet p):
     *          creates a new Packet that is a copy of "p"
     *      Packet (int seq, int ack, int check, String newPayload)
     *          creates a new Packet with a sequence field of "seq", an
     *          ack field of "ack", a checksum field of "check", and a
     *          payload of "newPayload"
     *      Packet (int seq, int ack, int check)
     *          chreate a new Packet with a sequence field of "seq", an
     *          ack field of "ack", a checksum field of "check", and
     *          an empty payload
     *    Methods:
     *      boolean setSeqnum(int n)
     *          sets the Packet's sequence field to "n"
     *          returns true on success, false otherwise
     *      boolean setAcknum(int n)
     *          sets the Packet's ack field to "n"
     *          returns true on success, false otherwise
     *      boolean setChecksum(int n)
     *          sets the Packet's checksum to "n"
     *          returns true on success, false otherwise
     *      boolean setPayload(String newPayload)
     *          sets the Packet's payload to "newPayload"
     *          returns true on success, false otherwise
     *      int getSeqnum()
     *          returns the contents of the Packet's sequence field
     *      int getAcknum()
     *          returns the contents of the Packet's ack field
     *      int getChecksum()
     *          returns the checksum of the Packet
     *      int getPayload()
     *          returns the Packet's payload
     *
	"""
    # Add any necessary class/static variables here.  Remember, you cannot use
    # these variables to send messages error free!  They can only hold
    # state information for A or B.
    # Also add any necessary methods (e.g. checksum of a String)
    SEQNUM = 0
    INTRANSIT = False
    MESSAGE = ""
    SEQSENTAPP = 0
    SEQSENTPROTO = 0
    ACKSENT = 0
    NUMLOST = 0
    NUMCORR = 0

##########   soooo should i keep track of ack num and seq sep? and then when adding here add them, not seqnum twice..
### inc app level one for layer 5
### inc pro level for layer 3! should be same if none lost, proto more if some re sent

    def create_checksum_val(self, message):
        char_sum = 0
        for c in message:
            char_sum += ord(c)
        return char_sum

    def print_stats(self):
        print "seqinapp:", self.SEQSENTAPP, " seqsentproto:", self.SEQSENTPROTO, " acksent:", self.ACKSENT, " numlost:", self.NUMLOST, " num corrupt:",self.NUMCORR
        print  "packet loss:", round(((float(self.NUMLOST)) / float(self.SEQSENTPROTO)) * 100, 1), "%"
        print "packet corruption:", round((float(self.NUMCORR) / float(self.SEQSENTPROTO))  * 100, 1), "%"

    # This is the constructor.  Don't touch!
    def __init__(self, num_messages, loss, corrupt, avg_delay, trace, seed):
        super(StudentNetworkSimulator,self).__init__(num_messages, loss, corrupt, avg_delay, trace, seed)
        atexit.register(self.print_stats)

    # This routine will be called whenever the upper layer at the sender [A]
    # has a message to send.  It is the job of your protocol to insure that
    # the data in such a message is delivered in-order, and correctly, to
    # the receiving upper layer.
    def a_output(self, message):
        checkSum = self.create_checksum_val(message.get_data())
        p = Packet(self.SEQNUM, self.SEQNUM, checkSum, message.get_data())
        if not self.INTRANSIT:
            self.INTRANSIT = True
            self.MESSAGE = message.get_data()
            self.to_layer3(self.A, p)
            self.start_timer(self.A, 25)
            self.SEQSENTAPP += 1
            self.SEQSENTPROTO += 1
        # else:
            # do nothing (drop packet)

    # This routine will be called whenever a packet sent from the B-side 
    # (i.e. as a result of a toLayer3() being done by a B-side procedure)
    # arrives at the A-side.  "packet" is the (possibly corrupted) packet
    # sent from the B-side.
    def a_input(self, packet):
        if self.INTRANSIT:
            if packet.get_acknum() != self.SEQNUM or packet.get_checksum() != self.create_checksum_val(packet.get_payload()):
                #self.NUMCORR += 1
                #print "___CORRUPT packet!, send again..____"
                self.a_output(Message(packet.get_payload()))
            else:
                self.SEQNUM = 1 - self.SEQNUM
                self.INTRANSIT = False
                self.stop_timer(self.A)

    # This routine will be called when A's timer expires (thus generating a 
    # timer interrupt). You'll probably want to use this routine to control 
    # the retransmission of packets. See startTimer() and stopTimer(), above,
    # for how the timer is started and stopped. 
    def a_timer_interrupt(self):
        print "____TIMEOUT, send packet again________"
        self.INTRANSIT = False
        self.a_output(Message(self.MESSAGE))
        self.NUMLOST += 1
        self.SEQSENTPROTO += 1

    # This routine will be called once, before any of your other A-side 
    # routines are called. It can be used to do any required
    # initialization (e.g. of member variables you add to control the state
    # of entity A).	
    def a_init(self):
        self.SEQNUM = 0
        self.NUMLOST = 0
        self.INTRANSIT = False

    # This routine will be called whenever a packet sent from the B-side 
    # (i.e. as a result of a toLayer3() being done by an A-side procedure)
    # arrives at the B-side.  "packet" is the (possibly corrupted) packet
    # sent from the A-side.

    def b_input(self, packet):
        checkSum = self.create_checksum_val(packet.get_payload())
        if checkSum == packet.get_checksum():
            self.to_layer5(self.B, packet.get_payload())
            self.to_layer3(self.B, packet)
            self.ACKSENT += 1
        else:
            self.NUMCORR += 1
            print "____CORRUPT_PACKET, send old ack___________"
            self.to_layer3(self.B, Packet(self.SEQNUM, 1 - self.SEQNUM, self.create_checksum_val(self.MESSAGE), self.MESSAGE))
        # checksum checks if the same sdata was recieved

    # This routine will be called once, before any of your other B-side 
    # routines are called. It can be used to do any required
    # initialization (e.g. of member variables you add to control the state
    # of entity B).
    def b_init(self):
        self.ACKSENT = 0
