#!/usr/bin/env python
# coding: utf-8

# # Solar Simulator Controller
# For use with a solar simulator controller of **EPFL SB ISIC-GE AECH, Precision LED Driver V1.2**

# ## API
# 
# ### Methods
# **is_enabled( chanel = None ):** Returns the enabled state of a channel.
# 
# **set_channel( channel ):** Sets the active channel.
# 
# **current( channel = None ):** Returns the current of the given or active channel.
# 
# **set_current( amps = 0, channel = None ):** Sets the channel current.
# 
# **set_current_percent( percent, channel = None, reference = 'nominal' ):** Sets the channel current to a percentage of the given reference.
# 
# **set_color_current( color, amps = 0 ):** Sets the current of the given color. 
# 
# **set_color_percent( color, percent = 0, reference = 'nominal' ):** Sets all currents of the given color to a percentage of the reference.
# 
# **is_leader( channel = None ):** REturns whether the given or active channel is in leader mode.
# 
# **leader( channel = None ):** Returns the leader of the given or active channel. [Not Implemented]
# 
# **set_leader( leader = True, channel = None ):** Sets the given or active channel to be in leader or follower mode.
# 
# **zero_all():** Sets all currents to 0.
# 
# **enable( channel = None ):** Enables the given or active channel.
# 
# **enable_all():** Enables all channels.
# 
# **disable( channel = None ):** Disables the given or active channel.
# 
# **disable_all():** Disables all channels.
# 
# **reset():** Sets all currents to 0 and disables all channels.
# 
# 
# ### Properties
# **channel:** Returns the active channel.
# 
# **enabled:** Returns a list of enabled states.
# 
# **diode_voltage:** Returns the diode voltage in Volts.
# 
# **diode_current:** Returns the diode current in Amps.
# 
# **diode_jv:** Returns a dictionary of the diode current and voltage.
# 
# **currents:** Returns an array or currents for each channel.
# 

# ## Channel API
# Represents the properties of a channel.
# Does not interact with hardware.
# 
# ### Methods
# **_set_current( amps ):** Sets the currents of the channel.
# 
# **_set_enabled( enabled = True ):** Sets the enabled state of the channel.
# 
# ### Properties
# **color:** The color key.
# 
# **limit:** Current limits of the channel in Amps.
# 
# **group:** The group index of the channel. Used to group channels in the same wiring scheme.
# 
# **current:** The set current of the channel.
# 
# **enabled:** The enabled state of the channel.

# In[1]:


# standard imports
import time
import logging as log
log.basicConfig( level = log.DEBUG )

from collections import namedtuple

# SCPI imports
import bric_arduino_controllers.arduino_scpi_controller as scpi


# In[2]:


Limit = namedtuple( 'Limit', [ 'max', 'nominal' ] )

class Channel():
    """
    Represents an LED
    """
    
    def __init__( self, color, limit, group ):
        """
        :param color: Name of the channel LED's color.
        :param limit: A Limit object representing the current range of the channel.
        :param group: The wiring group of the LED.
        """
        self.__color = color
        
        if not isinstance( limit, Limit ) :
            raise RuntimeError( 'Invalid limit object.' )
            
        self.__limit = limit
        
        self.__group = group
        self.__current = None
        self.__enabled = False
        
    
    @property
    def color( self ):
        return self.__color
    
    
    @property
    def limit( self ):
        return self.__limit
    
    
    @property
    def group( self ):
        return self.__group
    
    
    @property
    def current( self ):
        return self.__current
    
    
    @property
    def enabled( self ):
        return self.__enabled
    
    
    def _set_current( self, amps ):
        """
        Sets the current value.
        """
        self.__current = amps
        
        
    def _set_enabled( self, enabled = True ):
        """
        Sets the enabled state.
        """
        self.__enabled = enabled
    


# In[3]:


class SolarSimulatorController( scpi.Instrument ):
    """
    Represents a Solar Simulator Controller
    
    Arbitrary SCPI commands can be performed
    treating the hieracrchy of the command as attributes.
    
    To read an property:  inst.p1.p2.p3()
    To call a function:   inst.p1.p2( 'value' )
    To execute a command: inst.p1.p2.p3( '' )
    """
    
    #--- methods ---
    
    def __init__( 
        self, 
        port = None, 
        timeout = 2, 
        baud = 115200,
        
        channels = [
            Channel( 'red',   Limit( nominal = 0.35, max = 0.7 ), 0 ),
            Channel( 'green', Limit( nominal = 0.70, max = 1.0 ), 0 ),
            Channel( 'blue',  Limit( nominal = 0.70, max = 1.0 ), 0 ),
            Channel( 'red',   Limit( nominal = 0.35, max = 0.7 ), 1 ),
            Channel( 'green', Limit( nominal = 0.70, max = 1.0 ), 1 ),
            Channel( 'blue',  Limit( nominal = 0.70, max = 1.0 ), 1 ),
            Channel( 'uv',    Limit( nominal = 1.00, max = 1.7 ), 2 ),
            Channel( 'uv',    Limit( nominal = 1.00, max = 1.7 ), 2 )
        ],
        
        diode = 8
    ):
        """
        Initializes an instance of the controller.
        
        :param port: The port associated to the hardware. [Default: None]
        :param timeout: Communication timeout in seconds. [Default: 2]
        :param baud: The hardware baudrate. [Default: 115200]
        :param leds: An array of LEDs representing each channel.
            [Default: [ r, g, b, r, g, b, uv, uv ] ]
        :param diode: The diode channel. [Default: 8]
        """
        scpi.Instrument.__init__( 
            self, 
            port, 
            read_termination = '\n\r',
            timeout = timeout, 
            baudrate = baud,
            io_attempts = 3
        )
        
        self.__baud = baud
        self.__channels = channels
        self.__diode = diode
        
        
    def connect( self ):
        super().connect()
        self.reset() #turn off all channels, set currents to 0
        
        
    def disconnect( self ):
        # turn off all channels, set to 0 current
        self.reset()
        super().disconnect()
        
        
    def write( self, msg ):
        if ( msg != '*IDN?' ) and ( not msg.startswith( 'ECHO' ) ):
            msg = ':' + msg
        
        super().write( msg )
        
        
    def query( self, msg ):
        """
        Must reimplement due to attemps hiding write function
        """
        if ( msg != '*IDN?' ) and ( not msg.startswith( 'ECHO' ) ):
            msg = ':' + msg
        
        return super().query( msg )
        
        
    @property
    def diode( self ):
        return self.__diode
    
    
    @property
    def channels( self ):
        """
        Returns the channel names
        """
        return self.__channels
    
    
    @property
    def channel( self ):
        """
        Returns the currently active channel
        """    
        resp = self.query( 'CHAN:SELE ?' )
        chan = self.__parse_channel( resp )
        return chan
    
    
    def set_channel( self, channel ):
        """
        Sets the active channel.
        
        :param channel: The channel to set.
        """
        resp = self.query( 'CHAN:SELE {}'.format( channel ) )
        resp = self.__parse_channel( resp )
        if ( resp != channel ):
            # channel did not change
            raise RuntimeError( 'Failed to change channel.' )
        
        
    # No set_voltage due to being current driven device
    @property
    def diode_voltage( self ):
        """
        Returns the voltage of the active channel.
        """
        def volt():
            volt = self.query( 'MEAS:VOLT ?' )
            volt = self.__parse_voltage( volt )
            return volt
        
        return self.__cnr( volt, self.diode )
    
    
    @property
    def diode_current( self ):
        """
        Returns the voltage of the active channel.
        """
        def curr():
            curr = self.query( 'MEAS:CURR ?' )
            curr = self.__parse_current( curr )
            return curr
        
        return self.__cnr( curr, self.diode )
    
    @property
    def diode_jv( self ):
        """
        Returns the diode current and voltage.
        
        :returns: A dictionary with keys 'current' and 'voltage'.
        """
        def djv():    
            volt = self.query( 'MEAS:VOLT ?' )
            volt = self.__parse_voltage( volt )
            
            curr = self.query( 'MEAS:CURR ?' )
            curr = self.__parse_current( curr )
            
            return {
                'current': curr, 
                'voltage': volt
            }
        
        return self.__cnr( djv, self.diode )
    
    
    @property
    def enabled( self ):
        """
        :returns: List of enabled states of channels.
        """
        return [ ch.enabled for ch in self.channels ]
    
    
    def is_enabled( self, channel = None ):
        """
        :param channel: Channel to examine or None for active channel.
            [Default: None]
        :returns: If channel is enabled.
        """
        if channel is None:
            channel = self.channel
            
        return self.channels[ channel ].enabled
    
    
    def current( self, channel = None ):
        """
        Returns the current of the active or given channel.
        
        :param channel: The desired channel or None for the active channel.
            [Defualt: None]
        """
        if channel is None:
            channel = self.channel
            
        ch = self.channels[ channel ]
        return ch.current
        
    
    @property
    def currents( self ):
        """
        Returns an array of currents for each channel.
        """
        channels = len( self.channels )
        currents = [ None ]* channels # init list
        for ch in range( channels ):
            currents[ ch ] = self.current( ch )
            
        return currents
    
    
    def set_current( self, amps, channel = None ):
        """
        Sets the current of the active or given channel.
        
        :raises RuntimeError: If an invalid channel is given.
        """
        if not self.__validate_channel( channel ):
            raise RuntimeError( 'Invalid channel {}'.format( channel ) )
            
        try:
            self.__validate_current( amps, channel )
            
        except RuntimeWarning as err:
            # nominal current exceeded, allow set, but warn
            print( err )
            
        except RuntimeError as err:
            # maximum current exceeded, do not allow set
            raise err
        
        # buffer length of arduino is 16
        # account for 'A' and null terminator
        amp_str = '{:015.15f}'.format( amps )
        amp_str = amp_str[ :14 ]
        
        self.__cnr( 
            lambda: self.query( 
                'SOUR:CURR {}'.format( '{}A'.format( amp_str ) ) 
            ),
            channel 
        )
        
        # update channel
        if channel is None:
            channel = self.channel
            
        self.__channels[ channel ]._set_current( amps )
        
        
    def set_current_percent( self, 
        percent = 0, 
        channel = None, 
        reference = 'nominal' 
    ):
        """
        Set the current of the given or active channel to a percent
        of the nominal or maximum current.
        
        :param percent: The percent to set. [Range: 0 - 1 ]
            [Default: 0]
        :param channel: The channel to use, or None for the active channel.
            [Default: None]
        :param reference: The reference current to use. 
            Values are [ 'nominal', 'max' ].
            [Default: 'nominal']
        """
        if ( percent < 0 ) or ( percent > 1 ):
            # invalid percent
            raise ValueError( 
                'Invalid percent {}. Must be between 0 and 1.'.format( percent ) 
            ) 
        
        if channel is None:
            channel = self.channel
            
        reference = getattr( self.channels[ channel ].limit, reference )
        current = percent* reference
        
        self.set_current( current, channel )
        
        
    def color_channels( self, color = None ):
        """
        Returns the list of channels by color.
        
        :param color: The color to get, or None for all colors. [Default: None]
        :returns: An array of the given color, or a dictionary of all colors if color is None.
        """
        # get all colors
        colors = {};
        for ch in self.channels:
            color = ch.color;
            if color in colors:
                # color already exists
                colors[ color ].append( ch )

            else:
                # new color
                colors[ color ] = [ ch ]
                    
        
        if color is not None:
            # return specified color
            colors = colors[ color ]
                
        return colors
    
    
    def set_color_current( self, color, amps = 0 ):
        """
        Sets the current for channels of the given color.
        
        :param color: The color to set.
        :param amps: The current to set.
        """
        channels = self.color_channels( color )
        for ch in channels:
            self.set_current( amps, ch )
        
    
    
    def set_color_percent( self, color, percent = 0, reference = 'nominal' ):
        """
        Set the current of the channels with the given color to a percent
        of the nominal or maximum current.
        
        :param color: The color to set.
        :param percent: The percent to set. [Range: 0 - 1 ]
            [Default: 0]
        :param reference: The reference current to use. 
            Values are [ 'nominal', 'max' ].
            [Default: 'nominal']
        """
        channels = self.color_channels( color )
        for ch in channels:
            self.set_current_percent( percent, ch, reference )
    
        
    def zero_all( self ):
        """
        Sets all currents to zero.
        """
        for ch in range( len ( self.channels ) ):
            # loop over all channels, set current to 0
            if self.is_leader( ch ):
                self.set_current( 0, ch )
    
    
    def is_leader( self, channel = None ):
        """
        Returns whether the active or given channel is in leader mode.
        
        :param channel: The channel to examine or None for the active channel.
            [Default: None]
        :returns: A boolean representing the leader mode of the channel.
        """
        def is_lead():
            resp = self.query( 'CHAN:MODE ?' )
            if resp.endswith( 'MASTER' ):
                return True

            return False
        
        return self.__cnr( is_lead, channel )
    
    
    def leader( self, channel = None ):
        """
        Returns the leader of the given or active channel.
        
        :param channel: The channel to examine or None for the active channel.
            [Default: None]
        :returns: The channel's leader.
        """
        raise NotImplementedError()
    
    
    def set_leader( self, leader = False, channel = None ):
        """
        Sets the mode and leader of the given or active channel to leader or follower.
        
        :param leader: False, to make a leader, or the channel to follow.
            [Default: False]
        :param channel: The channel to set or None for the active channel.
            [Default: None]
        """
        if leader is False:
            # set as leader
            self.__cnr( 
                lambda: self.query( 'CHAN:MODE MASTER' ),
                channel
            )
        
        else:
            # set as follower
            if ( leader < 0 ) or ( leader > len( self.channels ) ):
                # invalid leader
                raise ValueError( 
                    'Invalid leader channel {}. Available channels are between 0 and {}'.format(
                        leader, len( self.channels )
                    )
                )
            
            def set_lead():
                self.query( 'CHAN:MAST {}'.format( leader ) )
                self.query( 'CHAN:MODE SLAVE' )
                
            self.__cnr( set_lead, channel )
    
    
    def enable( self, channel = None ):
        """
        Enables the active or given channel.
        
        :raises RuntimeError: If an invalid channel is given.
        """
        if not self.__validate_channel( channel ):
            raise RuntimeError( 'Invalid channel {}'.format( channel ) )
        
        self.__cnr(
            lambda: self.query( 'CHAN:ENAB ON' ),
            channel
        )
        
        if channel is None:
            channel = self.channel
            
        self.channels[ channel ]._set_enabled( True )
        
        
    def disable( self, channel = None ):
        """
        Disables the active or given channel.
        
        :raises RuntimeError: If an invalid channel is given.
        """
        if not self.__validate_channel( channel ):
            raise RuntimeError( 'Invalid channel {}'.format( channel ) )
            
        self.__cnr(
            lambda: self.query( 'CHAN:ENAB OFF' ),
            channel
        )
        
        if channel is None:
            channel = self.channel
            
        self.channels[ channel ]._set_enabled( False )
        
        
    def enable_all( self ):
        """
        Enables all channels
        """
        for ch in range( len( self.channels ) ):
            if self.is_leader( ch ):
                self.enable( ch )
            
            
    def disable_all( self ):
        """
        Enables all channels
        """
        for ch in range( len( self.channels ) ):
            if self.is_leader( ch ):
                self.disable( ch )
            
            
            
    def reset( self ):
        """
        Sets all currents to 0, disables all channels, and
        sets all channels to leader mode.
        """
        # set instrument to defualt mode
        self.zero_all() # set all currents to 0
        self.disable_all() # disable all currents
        
        for ch in range( len( self.channels ) ):
            # set all as leader
            self.set_leader( channel = ch )
        
    
    
    #--- private methods ---
    
    def __cnr( self, func, channel ):
        """
        Alias for __change_and_restore
        """
        return self.__change_and_restore( func, channel )
    
        
    def __change_and_restore( self, func, channel ):
        """
        Changes to the given channel, calls the function, 
        then returns to the original channel.
        
        :param func: The function to call on the channel.
        :param channel: The channel to switch to.
        :returns: The return value of the function.
        """
        # select given channel if needed
        o_chan = None
        if channel is not None:
            o_chan = self.channel
            self.set_channel( channel )
        
        try:   
            val = func()
            
        except Exception as err:
            raise err
        
        else:
            return val
        
        finally:
            if o_chan is not None:
                # return to original channel
                self.set_channel( o_chan )
    
    
    def __validate_channel( self, channel = None ):
        """
        Ensure that a valid channel is being given.
        Channels 0 - 7 are for LEDs, channel 8 is the photodiode.
        
        :param channel: The channel to validate, or None for the active channel.
            [Default: None]
        """
        if channel is None:
            channel = self.channel
        
        return ( 
            ( channel >= 0 ) and 
            ( channel < len( self.channels ) ) and
            ( channel != self.diode ) and
            ( self.is_leader( channel ) )
        )
    
    
    def __validate_current( self, current, channel = None ):
        """
        Ensures that the maximum current is not exceeded for a given channel.
        
        :param current: The current to check.
        :param channel: The channel that will be set or None for active channel. 
            [Defualt: None]
            
        :returns: True if the current is safe (i.e. below the max).
        :raises RuntimeWarning: If the current exceeds the nominal.
        :raises RuntimeError: If the current exceeds the maximum.
        """
        if channel is None:
            channel = self.channel
    
        channel = self.channels[ channel ]
        mxc = channel.limit.max
        nom = channel.limit.nominal 
        
        if current > mxc:
            # current exceeds max, raise exception
            raise RuntimeError( 
                'Attempting to set current above maximum allowed ({})'.format( mxc ) 
            )
            
        if current > nom:
            # current exceeds nominal, raise warning
            raise RuntimeWarning(
                'Attempting to set current above nominal ({})'.format( nom )
            )
            
        # safe current
        return True
    
    
    def __parse_channel( self, resp ):
        resp = resp.replace( 'CHAN:SELE ', '' )
        resp = int( resp )
        return resp
    
    
    def __parse_current( self, resp ):
        # response of form nn.nnnnmA
        resp = resp[ :-2 ].replace( 'MEAS:CURR ', '' )
        resp = float( resp )/ 1e3
        return resp
    
    
    def __parse_voltage( self, resp ):
        #response of form nn.nnnnV
        resp = resp[ :-1 ].replace( 'MEAS:VOLT ', '' )
        resp = float( resp )
        return resp
