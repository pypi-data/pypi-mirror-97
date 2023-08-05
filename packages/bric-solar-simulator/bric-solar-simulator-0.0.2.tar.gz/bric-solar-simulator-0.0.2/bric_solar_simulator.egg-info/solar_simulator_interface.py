#!/usr/bin/env python
# coding: utf-8

# # GUI Interface
# 
# ## Requirements
# Ensure that `import-ipynb` module is installed
# 
# ## Compiling
# 1. Ensure fbs is installed `pip install fbs`
# 2. Iniate a project `python3 -m fbs startproject`
# 3. Freeze the binary `python3 -m fbs freeze`
# 4. Create an installer `python3 -m fbs installer`
# 
# ## Converting to .py
# To save this file for use as a CLI, convert it to a .py file using `jupyter nbconvert --to python <filename>`

# In[1]:


import os
import sys
import re
import serial

from collections import namedtuple
from functools import partial

# PyQt
from PyQt5 import QtGui

from PyQt5.QtCore import (
    Qt,
    QCoreApplication,
    QTimer,
    QThread
)

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QDoubleSpinBox,
    QButtonGroup,
    QMessageBox
)

# controller
import solar_simulator_controller as ssc


# In[2]:


class Channel():
    class Controls:
        def __init__(
            self,
            intensity  = None,
            enable     = None,
            enable_all = None,
            rng        = None,
            sun_intensity = None,
            set_sun       = None,
            tmr_debounce  = None
        ):
            self.intensity = intensity
            self.enable = enable
            self.enable_all = enable_all
            self.range = rng
            self.sun_intensity = sun_intensity
            self.set_sun = set_sun
            self.tmr_debounce = tmr_debounce
        
    
    
    def __init__( 
        self,              
        channel,
        color,
        intensity  = None,
        enable     = None,
        enable_all = None,
        rng        = None,
        sun_intensity = None,
        set_sun       = None
    ):
        self.__channel = channel
        self.__color = color
        
        # debounce
        tmr_debounce = QTimer()
        tmr_debounce.setInterval( 250 )
        tmr_debounce.setSingleShot( True )
        
        self.controls = self.Controls(
            intensity,
            enable,
            enable_all,
            rng,
            sun_intensity,
            set_sun,
            tmr_debounce
        )
        
        self.intensity = 0
        self.enabled = False
        self.range = 'nominal'
    
        
    @property
    def channel( self ):
        return self.__channel
    
    
    @property 
    def color( self ):
        return self.__color
        
        


Diode = namedtuple( 'Diode', [ 'current', 'voltage', 'current_units', 'voltage_units' ] )


# In[3]:


class SolarSimulatorInterface( QWidget ):
    
    #--- window close ---
    def closeEvent( self, event ):
        self.delete_controller()
        event.accept()
        
    
    #--- destructor ---
    def __del__( self ):
        self.__delete_controller()
        
    
    #--- initializer ---
#     def __init__( self, resources ): # FREEZE
    def __init__( self ):
        super().__init__()
        
        #--- instance variables ---
#         image_folder = resources + '/images/' # FREEZE
        image_folder = os.getcwd() + '/images/' 
    
        self.img_redLight    = QtGui.QPixmap( image_folder + 'red-light.png'    ).scaledToHeight( 32 )        
        self.img_greenLight  = QtGui.QPixmap( image_folder + 'green-light.png'  ).scaledToHeight( 32 )
        self.img_yellowLight = QtGui.QPixmap( image_folder + 'yellow-light.png' ).scaledToHeight( 32 )
        
        self.ports  = self.getComPorts()
        self.inst   = None # the instrument
        
        self.channels = []
        self.diode = None
        
        self.spectral_intensities = {
            'red':   1.0,
            'green': 0.1,
            'blue':  0.1,
            'uv':    0.001
        }

        #--- timers ---
        # diode
        self.tmr_diode = QTimer()
        self.tmr_diode.setInterval( 1000 )
        self.tmr_diode.timeout.connect( self.update_diode_ui )
        
        
        #--- init UI ---
        # title font
        self.fnt_title = QtGui.QFont()
        self.fnt_title.setBold( True )
        self.fnt_title.setPointSize( 12 )
        
        # label font
        self.fnt_label = QtGui.QFont()
        self.fnt_label.setBold( True )
        
        self.init_ui()
        self.register_connections()
        
        #--- init variables ---
        
        

    def init_ui( self ):
        #--- main window ---
        self.setGeometry( 100, 100, 400, 600 )
        self.setWindowTitle( 'Solar Simulator Controller' )
        
        lo_main = QVBoxLayout()
        lo_main.addLayout( self.ui_mainToolbar() )
        lo_main.addLayout( self.ui_settings() )
        lo_main.addStretch()
        lo_main.addLayout( self.ui_commands() )
        
        self.setLayout( lo_main )
        
        self.show()
       
    
    def ui_mainToolbar( self ):
        lo_mainToolbar = QHBoxLayout()
        lo_mainToolbar.setAlignment( Qt.AlignTop )
        
        self.ui_mainToolbar_comPorts( lo_mainToolbar )
        self.ui_mainToolbar_connect( lo_mainToolbar )
        
        return lo_mainToolbar
    
    
    def ui_settings( self ):
        lo_settings = QVBoxLayout()
        
        self.ui_settings_led_groups( lo_settings )
        
        return lo_settings
    
    
    def ui_commands( self ):
        lo_commands = QVBoxLayout()
        
        self.ui_commands_diode( lo_commands )
      
        return lo_commands
    
    
    def ui_mainToolbar_comPorts( self, parent ):
        self.cmb_comPort = QComboBox()
        self.update_ports_ui()
        
        lo_comPort = QFormLayout()
        lo_comPort.addRow( 'COM Port', self.cmb_comPort )
        
        parent.addLayout( lo_comPort )
        
    
    def ui_mainToolbar_connect( self, parent ):
        # connect / disconnect
        self.lbl_statusLight = QLabel()
        self.lbl_statusLight.setAlignment( Qt.AlignCenter )
        self.lbl_statusLight.setPixmap( self.img_redLight )
        
        self.lbl_status = QLabel( 'Disconnected' )
        self.btn_connect = QPushButton( 'Connect' )
    
        lo_statusView = QVBoxLayout()
        lo_statusView.addWidget( self.lbl_statusLight )
        lo_statusView.addWidget( self.lbl_status )
        lo_statusView.setAlignment( Qt.AlignHCenter )
        
        lo_status = QHBoxLayout()
        lo_status.addLayout( lo_statusView )
        lo_status.addWidget( self.btn_connect )
        lo_status.setAlignment( Qt.AlignCenter )
        
        parent.addLayout( lo_status )
        
        
    def ui_settings_led_groups( self, parent ):
        lo_led = QVBoxLayout()
        
        self.ui_settings_led_group( 
            lo_led,
            'Group 1',
            {
                'red':   0,
                'green': 1,
                'blue':  2,
                'uv':    6
            } 
        )
        
        lo_led.addSpacing( 35 ) # spacing between groups
        
        self.ui_settings_led_group( 
            lo_led, 
            'Group 2',
            {
                'red':   3,
                'green': 4,
                'blue':  5,
                'uv':    7
            }
        )
        
        parent.addLayout( lo_led )
        
    
    def ui_settings_led_group( self, parent, title, channels ):   
        # title
        lbl_title = QLabel( title )
        lbl_title.setFont( self.fnt_title )
        
    
        # channel controls
        lo_colors = QVBoxLayout()
        for color, ch in channels.items():
            self.ui_settings_channel_control( lo_colors, color, ch )
        
        # main layout
        lo_group = QVBoxLayout()
        lo_group.addWidget( lbl_title )
        
        self.ui_settings_enable_all( lo_group, channels )
        
        lo_group.addLayout( lo_colors )
        
        self.ui_settings_spectrum_group( lo_group, channels ) # am 1.5
        self.ui_settings_range_group( lo_group, channels ) # range
        
        parent.addLayout( lo_group )
        
    
    def ui_settings_channel_control( self, parent, color, channel ):
        lbl_color = QLabel( self.color_to_title( color ) )
        lbl_color.setFont( self.fnt_label )
        
        sb_color = QDoubleSpinBox()
        sb_color.setDecimals( 6 )
        sb_color.setMinimum( 0 )
        sb_color.setMaximum( 100 )
        
        btn_on = QPushButton( 'On' )      
        btn_on.setCheckable( True )

        lo_enable = QHBoxLayout()
        lo_enable.addWidget( btn_on )
        lo_color = QHBoxLayout()
        lo_color.addWidget( lbl_color )
        lo_color.addWidget( sb_color )
        lo_color.addLayout( lo_enable )

        parent.addLayout( lo_color )
        
        # controls
        self.channels.append( Channel(
            channel   = channel,
            color     = color,
            intensity = sb_color,
            enable    = btn_on
        ) )
        
        
    def ui_settings_enable_all( self, parent, group ):
        btn_enable_all = QPushButton( 'All On' )      
        btn_disable_all = QPushButton( 'All Off' )
        
        btg_enable_all = QButtonGroup()
        btg_enable_all.addButton( btn_disable_all, 0 )
        btg_enable_all.addButton( btn_enable_all, 1 )
        
        lo_enable_all = QHBoxLayout()
        lo_enable_all.setAlignment( Qt.AlignRight )
        lo_enable_all.addStretch()
        lo_enable_all.addWidget( btn_disable_all )
        lo_enable_all.addWidget( btn_enable_all )
        
        parent.addLayout( lo_enable_all )
        
        # controls
        for ch in group.values():
            channel = self.get_channel( ch )
            channel.controls.enable_all = btg_enable_all 
        
        
    def ui_settings_spectrum_group( self, parent, group ):
        lbl_title = QLabel( 'Suns' )
        lbl_title.setFont( self.fnt_label )
        
        sb_percent = QDoubleSpinBox()
        sb_percent.setDecimals( 6 )
        sb_percent.setMinimum( 0 )
#         sb_percent.setMaximum( 10 )
        
        btn_set = QPushButton( 'Set' )
        
        lo_sun = QHBoxLayout()
        lo_sun.addWidget( lbl_title )
        lo_sun.addWidget( sb_percent )
        lo_sun.addWidget( btn_set )
        
        parent.addLayout( lo_sun )
        
        # controls
        for ch in group.values():
            channel = self.get_channel( ch )
            channel.controls.sun_intensity = sb_percent
            channel.controls.set_sun = btn_set
        
    
    def ui_settings_range_group( self, parent, group ):
        lbl_range = QLabel( 'Range' )
        lbl_range.setFont( self.fnt_label )
        
        btn_range_nominal = QPushButton( 'Nominal' )
        btn_range_nominal.setCheckable( True )
        btn_range_nominal.setChecked( True )
        
        btn_range_max = QPushButton( 'Max' )
        btn_range_max.setCheckable( True )
        
        btg_range = QButtonGroup()
        btg_range.addButton( btn_range_nominal )
        btg_range.addButton( btn_range_max )
        
        lo_range = QHBoxLayout()
        lo_range.addWidget( lbl_range )
        lo_range.addWidget( btn_range_nominal )
        lo_range.addWidget( btn_range_max )
        
        parent.addLayout( lo_range )
        
        # controls
        for ch in group.values():
            channel = self.get_channel( ch )
            channel.controls.range = btg_range 
    
    
    def ui_commands_diode( self, parent ):
        lbl_title = QLabel( 'Diode' )
        lbl_title.setFont( self.fnt_title )
        
        # current
        lbl_current_title = QLabel( 'Current' )
        lbl_current_title.setFont( self.fnt_label )
        
        lbl_current = QLabel( 'N\A' )
        lbl_current_units = QLabel( '' )
        
        lo_current = QHBoxLayout()
        lo_current.addWidget( lbl_current_title )
        lo_current.addWidget( lbl_current )
        lo_current.addWidget(lbl_current_units )
        
        # voltage
        lbl_voltage_title = QLabel( 'Voltage' )
        lbl_voltage_title.setFont( self.fnt_label )
        
        lbl_voltage = QLabel( 'N\A' )
        lbl_voltage_units = QLabel( '' )
        
        lo_voltage = QHBoxLayout()
        lo_voltage.addWidget( lbl_voltage_title )
        lo_voltage.addWidget( lbl_voltage )
        lo_voltage.addWidget(lbl_voltage_units )
        
        lo_diode = QHBoxLayout()
        lo_diode.addWidget( lbl_title )
        lo_diode.addLayout( lo_current )
        lo_diode.addLayout( lo_voltage )
        
        self.diode = Diode(
            current = lbl_current,
            voltage = lbl_voltage,
            current_units = lbl_current_units,
            voltage_units = lbl_voltage_units
        )
        
        
        parent.addLayout( lo_diode )
        
    #--- ui functionality ---
    
    def register_connections( self ):
        
        def handle_intensity_change( channel ):
            tmr_debounce = channel.controls.tmr_debounce
            
            tmr_debounce.stop()
            try:
                tmr_debounce.timeout.disconnect()
                
            except:
                pass
                
            tmr_debounce.timeout.connect(
                lambda: self.set_channel_intensity( channel )
            )
            
            tmr_debounce.start()
            
            
        def handle_enable_all( channel, enable = True ):
            btn = channel.controls.enable
            enabled = btn.isChecked()
            
            if enable != enabled:
                # change state of button
                btn.click()
        
        
        self.cmb_comPort.currentTextChanged.connect( self.change_port )
        self.btn_connect.clicked.connect( self.toggle_connect )   
        
        # channel functionality
        for channel in self.channels:           
            channel.controls.intensity.valueChanged.connect(
                # must use closure to freeze channel
                partial( handle_intensity_change, channel )
            )

            # enable
            channel.controls.enable.clicked.connect(
                # must use closure to freeze channel
                partial( self.enable_channel, channel )
            )
            
            # disable all control
            channel.controls.enable_all.button( 0 ).clicked.connect(                
                # must use closure to freeze channel
                partial( handle_enable_all, channel, False )
            )
            
            # enable all control
            channel.controls.enable_all.button( 1 ).clicked.connect(
                # must use closure to freeze channel
                partial( handle_enable_all, channel, True )
            )
            
            for range_btn in channel.controls.range.buttons():
                range_btn.clicked.connect(
                    # must use closure to freeze group
                    partial( self.set_range, channel, range_btn.text().lower() )
                )
            
            channel.controls.set_sun.clicked.connect(
                # must use closure to freeze group
                partial( self.set_sun, channel )
            )
            
        
        
    
    #--- slot functions ---
    
    def change_port( self ):
        """
        Changes port and disconnects from current port if required
        """
        # disconnect and delete controller
        self.delete_controller()
          
        # update port
        self.update_port()
        
        
    def update_ports( self ):
        """
        Check available COMs, and update UI list
        """
        self.ports = self.getComPorts()
        self.update_ports_ui()
        
        
    def toggle_connect( self ):
        """
        Toggles connection between selected com port
        """
        self.tmr_diode.stop()
        
        # show waiting for communication
        self.lbl_status.setText( 'Waiting...' )
        self.lbl_statusLight.setPixmap( self.img_yellowLight )
        self.repaint()
        
        # create laser controller if doesn't already exist, connect
        if self.inst is None:
            try:
                self.inst = ssc.SolarSimulatorController( self.port )
                self.inst.connect()
                
            except Exception as err:
                self.update_connected_ui( False )
                
                warning = QMessageBox()
                warning.setWindowTitle( 'Solar Simulator Controller Error' )
                warning.setText( 'Could not connect\n{}'.format( err ) )
                warning.exec()
            
        else:
            self.delete_controller()
        
        # update ui
        self.update_diode_ui()
        
        if self.inst is not None:
            self.update_connected_ui( self.inst.connected )
            
            if self.inst.connected:
                self.tmr_diode.start()
            
        else:
            self.update_connected_ui( False )
            
            
    def set_channel_intensity( self, channel ):
        if not self.is_connected():
            return
        
        value = channel.controls.intensity.value()/ 100
        reference = channel.range
        self.inst.set_current_percent( value, channel.channel, reference )
    
    
    def enable_channel( self, channel ):
        if not self.is_connected():
            return 
        
        ch = channel.channel
        if channel.controls.enable.isChecked():
            self.inst.enable( ch )
            
        else:
            self.inst.disable( ch )
            
    
    def set_range( self, channel, rng ):
        if not self.is_connected():
            return
        
        channel.range = rng
        self.set_channel_intensity( channel )
    
    
    def set_sun( self, channel ):
        if not self.is_connected():
            return
        
        intensity = channel.controls.sun_intensity.value()* 100
        ratio = self.spectral_intensities[ channel.color ]
        
        channel.controls.intensity.setValue( intensity* ratio )
        

        
    #--- helper functions ---
    
    
    def getComPorts( self ):
        """ (from https://stackoverflow.com/a/14224477/2961550)
        Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith( 'win' ):
            ports = [ 'COM%s' % (i + 1) for i in range( 256 ) ]
            
        elif sys.platform.startswith( 'linux' ) or sys.platform.startswith( 'cygwin' ):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob( '/dev/tty[A-Za-z]*' )
            
        elif sys.platform.startswith( 'darwin' ):
            ports = glob.glob( '/dev/tty.*' )
            
        else:
            raise EnvironmentError( 'Unsupported platform' )

        result = []
        for port in ports:
            try:
                s = serial.Serial( port )
                s.close()
                result.append( port )
                
            except ( OSError, serial.SerialException ):
                pass
            
        return result    

    
    def delete_controller( self ):
        if self.inst is not None:
            self.inst.disconnect()
            del self.inst
            self.inst = None
            
            
    def parse_com_port( self, name ):
        pattern = "(\w+)\s*(\(\s*\w*\s*\))?"
        matches = re.match( pattern, name )
        if matches:
            name = matches.group( 1 )
            if name == 'No COM ports available...':
                return None
            else:
                return name
        else:
            return None
        
        
    def update_port( self ):
        self.port = self.cmb_comPort.currentText()
        
        
    def update_ports_ui( self ):
        self.cmb_comPort.clear()
        
        if len( self.ports ):
            self.cmb_comPort.addItems( self.ports )
            
        else:
            self.cmb_comPort.addItem( 'No COM ports available...' )
            
    
    def update_connected_ui( self, connected ):
        if connected == True:
            statusText = 'Connected'
            statusLight = self.img_greenLight
            btnText = 'Disconnect'
            
        elif connected == False:
            statusText = 'Disconnected'
            statusLight = self.img_redLight
            btnText = 'Connect'
            
        else:
            statusText = 'Error'
            statusLight = self.img_yellowLight
            btnText = 'Connect'
        
        self.lbl_status.setText( statusText )
        self.lbl_statusLight.setPixmap( statusLight )
        self.btn_connect.setText( btnText )
        
        
    def update_enable_button_ui( self, btg ):
        checked_id = btg.checkedId()
        
        for btn in btg.buttons():
            enabled = ( btg.id( btn ) == checked_id )
            self.set_enabled_stylesheet( btn, enabled )
        
    
    def update_diode_ui( self ):
        if ( self.inst is None ) or ( not self.inst.connected ):
            self.diode.current.setText( 'N/A' )
            self.diode.voltage.setText( 'N/A' )
            self.diode.current_units.setText( '' )
            self.diode.voltage_units.setText( '' )
            
            return
        
        jv = self.inst.diode_jv
        jv = self.diode_to_str( jv )
        
        self.diode.current.setText( jv[ 'current' ] )
        self.diode.voltage.setText( jv[ 'voltage' ] )
        self.diode.current_units.setText( jv[ 'current_unit' ] )
        self.diode.voltage_units.setText( jv[ 'voltage_unit' ] )
        
        
    def get_channel( self, ch ):
        """
        Get Channel class by channel id.
        """
        for channel in self.channels:
            if channel.channel == ch:
                return channel
            
        raise RuntimeError( 'Channel {} does not exist.'.format( ch ) )
    
    
    def color_to_title( self, color ):
        if color == 'uv':
            return 'UV'
        
        return color[ 0 ].upper() + color[ 1: ].lower()
        
        
    def diode_to_str( self, jv ):
        ranges = {
            -9: 'n',
            -6: 'u',
            -3: 'm',
             0: ''
        }
        
        strs = {}
        for measurement, val in jv.items():
            if measurement == 'current':
                unit = 'A'
            
            elif measurement == 'voltage':
                unit = 'V'
                
            else:
                raise ValueError( 'Invalid unit for Diode JV {}.'.format( measurement ) )
            
            greatest = None
            for index, prefix in ranges.items():
                magnitude = 10** index
                
                if abs( val ) >= magnitude:
                    if ( greatest is None ) or ( index > greatest ):
                        # show 3 significant digits
                        val_str = str( val/ magnitude )
                        val_str = val_str[ :3 ] if ( val_str[ 3 ] == '.' ) else val_str[ :4 ]
                        unit_str = prefix + unit
                        
                        greatest = index
    
            if greatest is None:
                raise ValueError( 'Invalid Diode JV range {}'.format( val ) )    
                
            strs[ measurement ] = val_str
            strs[ measurement + '_unit' ] = unit_str
        
        return strs
    
    
    def is_connected( self ):
        return ( self.inst is not None ) and ( self.inst.connected )


# In[ ]:


# FREEZE
app = QCoreApplication.instance()
if app is None:
    app = QApplication( sys.argv )
    
main_window = SolarSimulatorInterface()
sys.exit( app.exec_() )


# In[ ]:


# FREEZE
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '1')


# In[ ]:




