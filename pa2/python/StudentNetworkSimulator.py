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

    def create_checksum_val(self, message):
        char_sum = 0
        for c in message:
            char_sum += ord(c)
        return char_sum

    # This is the constructor.  Don't touch!
    def __init__(self, num_messages, loss, corrupt, avg_delay, trace, seed):
        super(StudentNetworkSimulator,self).__init__(num_messages, loss, corrupt, avg_delay, trace, seed)

    # This routine will be called whenever the upper layer at the sender [A]
    # has a message to send.  It is the job of your protocol to insure that
    # the data in such a message is delivered in-order, and correctly, to
    # the receiving upper layer.
    def a_output(self, message):
        checkSum = self.create_checksum_val(str(message))
        p = Packet(self.SEQNUM, self.SEQNUM, checkSum, str(message))
        if not self.INTRANSIT:
            self.INTRANSIT = True
            print "___patrick____!!!!!"
            self.start_timer(self.A, 100)
            self.to_layer3(self.A, p)
        else:
            #if timeout, resend packet!
            if self.get_time() > 1:
                print "__first"
                print self.get_time()
            if self.get_time() > 10:
                print "__second"
            if self.get_time() > 100:
                print "__third"
            if self.get_time() > 500:
                print "__fourth"
            if self.get_time() > 1000:
                print "__balllls in a_output"
            else:
                # while timer < 1000? wait, then send message again..?
                 print "__cunttttt in a_output"


    # This routine will be called whenever a packet sent from the B-side 
    # (i.e. as a result of a toLayer3() being done by a B-side procedure)
    # arrives at the A-side.  "packet" is the (possibly corrupted) packet
    # sent from the B-side.
    def a_input(self, packet):
        if paket.get_acknum() != self.SEQNUM:
            print "___in the iff statement, line 130___________________________________-"
        else:
            print "___in the else statement, 132______________________________________"


    # This routine will be called when A's timer expires (thus generating a 
    # timer interrupt). You'll probably want to use this routine to control 
    # the retransmission of packets. See startTimer() and stopTimer(), above,
    # for how the timer is started and stopped. 
    def a_timer_interrupt(self):
        print "___IN THE MA FUCKN TIMERRRRR INTERUPTT_______"

    # This routine will be called once, before any of your other A-side 
    # routines are called. It can be used to do any required
    # initialization (e.g. of member variables you add to control the state
    # of entity A).	
    def a_init(self):
        self.SEQNUM = 0
        self.INTRANSIT = False

    # This routine will be called whenever a packet sent from the B-side 
    # (i.e. as a result of a toLayer3() being done by an A-side procedure)
    # arrives at the B-side.  "packet" is the (possibly corrupted) packet
    # sent from the A-side.

    def b_input(self, packet):
        self.INTRANSIT = False
        print "____we out here__________________________________IN BRAVOOOOOOOO"
        print packet.get_seqnum()
        print packet.get_acknum()
        print packet.get_checksum()
        print packet.get_payload()
        checkSum = self.create_checksum_val(str(packet.get_payload()))
        print checkSum
        if checkSum == packet.get_checksum():
            self.to_layer5(self.B, packet.get_payload())
        else:
            print "send the old ack!!"
        # checksum checks if the same sdata was recieved

    # This routine will be called once, before any of your other B-side 
    # routines are called. It can be used to do any required
    # initialization (e.g. of member variables you add to control the state
    # of entity B).
    def b_init(self):
        print "___we in the init in BRAVO _____"
