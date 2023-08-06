import sys
import typing


class Device:
    ''' Device objects represent an audio output backend like OpenAL or SDL, but might also represent a file output or RAM buffer output. lock() Locks the device so that it's guaranteed, that no samples are read from the streams until :meth: unlock is called. This is useful if you want to do start/stop/pause/resume some sounds at the same time. play(factory, keep=False) Plays a factory. :arg factory: The factory to play. :type factory: Factory :arg keep: See :attr: Handle.keep . :type keep: bool :return: The playback handle with which playback can be controlled with. :rtype: Handle stopAll() Stops all playing and paused sounds. unlock() Unlocks the device after a lock call, see :meth: lock for details.
    '''

    channels = None
    ''' The channel count of the device.'''

    distance_model = None
    ''' The distance model of the device.'''

    doppler_factor = None
    ''' The doppler factor of the device. This factor is a scaling factor for the velocity vectors in doppler calculation. So a value bigger than 1 will exaggerate the effect as it raises the velocity.'''

    format = None
    ''' The native sample format of the device.'''

    listener_location = None
    ''' The listeners's location in 3D space, a 3D tuple of floats.'''

    listener_orientation = None
    ''' The listener's orientation in 3D space as quaternion, a 4 float tuple.'''

    listener_velocity = None
    ''' The listener's velocity in 3D space, a 3D tuple of floats.'''

    rate = None
    ''' The sampling rate of the device in Hz.'''

    speed_of_sound = None
    ''' The speed of sound of the device. The speed of sound in air is typically 343.3 m/s.'''

    volume = None
    ''' The overall volume of the device.'''


class Factory:
    ''' Factory objects are immutable and represent a sound that can be played simultaneously multiple times. They are called factories because they create reader objects internally that are used for playback. file(filename) Creates a factory object of a sound file. :arg filename: Path of the file. :type filename: string :return: The created Factory object. :rtype: Factory sine(frequency, rate=48000) Creates a sine factory which plays a sine wave. :arg frequency: The frequency of the sine wave in Hz. :type frequency: float :arg rate: The sampling rate in Hz. It's recommended to set this value to the playback device's samling rate to avoid resamping. :type rate: int :return: The created Factory object. :rtype: Factory buffer() Buffers a factory into RAM. This saves CPU usage needed for decoding and file access if the underlying factory reads from a file on the harddisk, but it consumes a lot of memory. :return: The created Factory object. :rtype: Factory delay(time) Delays by playing adding silence in front of the other factory's data. :arg time: How many seconds of silence should be added before the factory. :type time: float :return: The created Factory object. :rtype: Factory fadein(start, length) Fades a factory in by raising the volume linearly in the given time interval. :arg start: Time in seconds when the fading should start. :type start: float :arg length: Time in seconds how long the fading should last. :type length: float :return: The created Factory object. :rtype: Factory fadeout(start, length) Fades a factory in by lowering the volume linearly in the given time interval. :arg start: Time in seconds when the fading should start. :type start: float :arg length: Time in seconds how long the fading should last. :type length: float :return: The created Factory object. :rtype: Factory filter(b, a = (1)) Filters a factory with the supplied IIR filter coefficients. Without the second parameter you'll get a FIR filter. If the first value of the a sequence is 0 it will be set to 1 automatically. If the first value of the a sequence is neither 0 nor 1, all filter coefficients will be scaled by this value so that it is 1 in the end, you don't have to scale yourself. :arg b: The nominator filter coefficients. :type b: sequence of float :arg a: The denominator filter coefficients. :type a: sequence of float :return: The created Factory object. :rtype: Factory highpass(frequency, Q=0.5) Creates a second order highpass filter based on the transfer function H(s) = s^2 / (s^2 + s/Q + 1) :arg frequency: The cut off trequency of the highpass. :type frequency: float :arg Q: Q factor of the lowpass. :type Q: float :return: The created Factory object. :rtype: Factory join(factory) Plays two factories in sequence. :arg factory: The factory to play second. :type factory: Factory :return: The created Factory object. :rtype: Factory limit(start, end) Limits a factory within a specific start and end time. :arg start: Start time in seconds. :type start: float :arg end: End time in seconds. :type end: float :return: The created Factory object. :rtype: Factory loop(count) Loops a factory. :arg count: How often the factory should be looped. Negative values mean endlessly. :type count: integer :return: The created Factory object. :rtype: Factory lowpass(frequency, Q=0.5) Creates a second order lowpass filter based on the transfer function H(s) = 1 / (s^2 + s/Q + 1) :arg frequency: The cut off trequency of the lowpass. :type frequency: float :arg Q: Q factor of the lowpass. :type Q: float :return: The created Factory object. :rtype: Factory mix(factory) Mixes two factories. :arg factory: The factory to mix over the other. :type factory: Factory :return: The created Factory object. :rtype: Factory pingpong() Plays a factory forward and then backward. This is like joining a factory with its reverse. :return: The created Factory object. :rtype: Factory pitch(factor) Changes the pitch of a factory with a specific factor. :arg factor: The factor to change the pitch with. :type factor: float :return: The created Factory object. :rtype: Factory reverse() Plays a factory reversed. :return: The created Factory object. :rtype: Factory square(threshold = 0) Makes a square wave out of an audio wave by setting all samples with a amplitude >= threshold to 1, all <= -threshold to -1 and all between to 0. :arg threshold: Threshold value over which an amplitude counts non-zero. :type threshold: float :return: The created Factory object. :rtype: Factory volume(volume) Changes the volume of a factory. :arg volume: The new volume.. :type volume: float :return: The created Factory object. :rtype: Factory
    '''

    pass


class Handle:
    ''' Handle objects are playback handles that can be used to control playback of a sound. If a sound is played back multiple times then there are as many handles. pause() Pauses playback. :return: Whether the action succeeded. :rtype: bool resume() Resumes playback. :return: Whether the action succeeded. :rtype: bool stop() Stops playback. :return: Whether the action succeeded. :rtype: bool
    '''

    attenuation = None
    ''' This factor is used for distance based attenuation of the source.'''

    cone_angle_inner = None
    ''' The opening angle of the inner cone of the source. If the cone values of a source are set there are two (audible) cones with the apex at the :attr: location of the source and with infinite height, heading in the direction of the source's :attr: orientation . In the inner cone the volume is normal. Outside the outer cone the volume will be :attr: cone_volume_outer and in the area between the volume will be interpolated linearly.'''

    cone_angle_outer = None
    ''' The opening angle of the outer cone of the source.'''

    cone_volume_outer = None
    ''' The volume outside the outer cone of the source.'''

    distance_maximum = None
    ''' The maximum distance of the source. If the listener is further away the source volume will be 0.'''

    distance_reference = None
    ''' The reference distance of the source. At this distance the volume will be exactly :attr: volume .'''

    keep = None
    ''' Whether the sound should be kept paused in the device when its end is reached. This can be used to seek the sound to some position and start playback again.'''

    location = None
    ''' The source's location in 3D space, a 3D tuple of floats.'''

    loop_count = None
    ''' The (remaining) loop count of the sound. A negative value indicates infinity.'''

    orientation = None
    ''' The source's orientation in 3D space as quaternion, a 4 float tuple.'''

    pitch = None
    ''' The pitch of the sound.'''

    position = None
    ''' The playback position of the sound in seconds.'''

    relative = None
    ''' Whether the source's location, velocity and orientation is relative or absolute to the listener.'''

    status = None
    ''' Whether the sound is playing, paused or stopped (=invalid).'''

    velocity = None
    ''' The source's velocity in 3D space, a 3D tuple of floats.'''

    volume = None
    ''' The volume of the sound.'''

    volume_maximum = None
    ''' The maximum volume of the source.'''

    volume_minimum = None
    ''' The minimum volume of the source.'''


class error:
    pass


AUD_DEVICE_JACK = None
''' constant value 3
'''

AUD_DEVICE_NULL = None
''' constant value 0
'''

AUD_DEVICE_OPENAL = None
''' constant value 1
'''

AUD_DEVICE_SDL = None
''' constant value 2
'''

AUD_DISTANCE_MODEL_EXPONENT = None
''' constant value 5
'''

AUD_DISTANCE_MODEL_EXPONENT_CLAMPED = None
''' constant value 6
'''

AUD_DISTANCE_MODEL_INVALID = None
''' constant value 0
'''

AUD_DISTANCE_MODEL_INVERSE = None
''' constant value 1
'''

AUD_DISTANCE_MODEL_INVERSE_CLAMPED = None
''' constant value 2
'''

AUD_DISTANCE_MODEL_LINEAR = None
''' constant value 3
'''

AUD_DISTANCE_MODEL_LINEAR_CLAMPED = None
''' constant value 4
'''

AUD_FORMAT_FLOAT32 = None
''' constant value 36
'''

AUD_FORMAT_FLOAT64 = None
''' constant value 40
'''

AUD_FORMAT_INVALID = None
''' constant value 0
'''

AUD_FORMAT_S16 = None
''' constant value 18
'''

AUD_FORMAT_S24 = None
''' constant value 19
'''

AUD_FORMAT_S32 = None
''' constant value 20
'''

AUD_FORMAT_U8 = None
''' constant value 1
'''

AUD_STATUS_INVALID = None
''' constant value 0
'''

AUD_STATUS_PAUSED = None
''' constant value 2
'''

AUD_STATUS_PLAYING = None
''' constant value 1
'''

AUD_STATUS_STOPPED = None
''' constant value 3
'''
