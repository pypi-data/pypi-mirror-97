#!/usr/bin/env python3

helpstr = (
    """The TSQ zce tool expects DAC spectrum as an imput spectrum. It does not\
    verify the validity of the imput. Thus it is up to the sw user to evaluate\
    that the given figure is sane.

    Acquiring DAC spectrum:
        For acquiring DAC spectrum you first need to find the correct number\
    of the DAC[1] (digital-to-analog converter) involved. You do this by\
    opening the Tune Window view in The Xcalibur Tune and then reading the\
    DAC which is connected to the collision offset.[2] Then you need to call\
    the .dac command[3] with proper vaules. The syntax is .dac #DAC, from, to,\
    step, m/z.[3] If your desired ion has m/z 133.7 in ESI+, the command\
    should look for example like ".dac 9,-8,6,.1,133.7".[4] Do not forget to\
    turn off the collision gas during .dac acquisition. When .dac command is\
    running, you can start the acquisition into file.  After some time you\
    will acquire smooth curve. After end of the acquisition you can go back to\
    the normal scan mode by calling the .dac command without arguments.[3]

    Limitations:
      * The program does not perform any sanity check, be careful and know\
    what you're doing
      * The program expects to get an TSQ DAC as an imput and expects, that\
    minimal value of that concrete DAC is -196.
      * You tell me.

    Notes:
    [1] DAC = digital-to-analog converter
    [2] on all TSQ7000 which I've seen the proper value is 9
    [3] for full reference do not hesitate to check the DAC.TXT in original sw\
    (Xcalibur/system/xsq/msi/DAC.TXT)
    [4] Dont be shocked to see wierd numbers on X-axis of Prof view after\
    submitting the command. As m/z is not expected to be negative, the whole\
    spectrum is shifted so that the minimal value of the selected DAC is 0. As\
    our specific DAC has the minimal value of -196, it means the shift of the\
    whole spectrum by +196.""")
