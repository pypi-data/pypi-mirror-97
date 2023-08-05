""" **Description**

        A log instance formats and writes log entries using the loguru package
        with a specified level and stream.  Log entries contain an ISO-8601
        datetime and level.  Dynamic stream redirection and level specification
        are supported.

        Singleton.

        Thread safe.

    **Example**

        ::

            from diamondback import Log
            import io
            import numpy
            import sys


            try :

                # Default - Log level is 'INFO'.

                # Set Log level to 'INFO'.

                Log.level( 'INFO' )

                # Write an 'INFO' entry.

                Log.write( 'INFO', 'Hello World.' )

                # Set Log stream to sys.stdout, and write an 'INFO' entry.

                Log.stream( sys.stdout )

                Log.write( 'INFO', 'Valid = {}'.format( True ) )

                # Set Log stream to a memory stream, write an 'INFO' entry, and read and reset the stream.

                stream = io.StringIO( )

                Log.stream( stream )

                x = numpy.random.rand( 2, 2 )

                Log.write( 'INFO', 'X = {}'.format( x ) )

                value = stream.getvalue( )

                _, _ = stream.truncate( 0 ), stream.seek( 0 )

                # Set Log stream to a file and write a 'WARNING' entry.

                with open( 'log.000.txt', 'w' ) as fout :

                    Log.stream( fout )

                    x = numpy.random.rand( 2, 2 )

                    Log.write( 'WARNING', 'X = {}'.format( x ) )

            except Exception as ex :

                # Write an 'ERROR' entry on Exception.

                Log.write( 'ERROR', ex )

    **License**

        `BSD-3C. <https://github.com/larryturner/diamondback/blob/master/license>`_

        Copyright (c) 2018, Larry Turner, Schneider Electric.  All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-03-22.

    **Definition**

"""

from loguru import logger
from threading import RLock
import numpy
import os
import sys
import typing


class Log( object ) :

    """ Log service.
    """

    numpy.set_printoptions( formatter = { 'float' : '{: .6f}'.format } )

    logger.remove( 0 )

    _identity = logger.add( sys.stdout, level = 'TRACE', format = '{time:YYYY-MM-DDTHH:mm:ss.SSZ} {level} {message}' )

    _level = logger.level( 'INFO' )

    _rlock = RLock( )

    @classmethod
    def level( cls, level : str ) -> None :

        """ Level.

            Arguments :

                level - Level in ( 'CRITICAL', 'ERROR', 'WARNING', 'SUCCESS', 'INFO', 'DEBUG', 'TRACE' ) ( str ).
        """

        with ( Log._rlock ) :

            try :

                Log._level = logger.level( level.upper( ) )

            except :

                raise ValueError( 'Level = {}'.format( level ) )

    @classmethod
    def stream( cls, stream : any ) -> None :

        """ Stream.

            Arguments :

                stream - Stream ( sys.stderr, sys.stdout, open( < path >, 'w' or 'a' ) ).
        """

        with ( Log._rlock ) :

            if ( ( not stream ) or ( not hasattr( stream, 'write' ) ) ) :

                raise ValueError( 'Stream = {}'.format( stream ) )

            logger.remove( Log._identity )

            Log._identity = logger.add( stream, level = 'TRACE', format = '{time:YYYY-MM-DDTHH:mm:ss.SSZ} {level} {message}' )


    @classmethod
    def write( cls, level : str, entry : typing.Union[ Exception, str ] ) -> None :

        """ Formats and writes log entries using the loguru package with a
            specified level and stream.  Log entries contain an ISO-8601
            datetime and level.

            Arguments :

                level - Level in ( 'CRITICAL', 'ERROR', 'WARNING', 'SUCCESS', 'INFO', 'DEBUG', 'TRACE' ) ( str ).

                entry - Entry ( Exception, str ).
        """

        with ( Log._rlock ) :

            try :

                level = logger.level( level.upper( ) )

            except :

                raise ValueError( 'Level = {}'.format( level ) )

            if ( level.no >= Log._level.no ) :

                try :

                    if ( isinstance( entry, Exception ) ) :

                        entry = 'Exception = {} Description = {}'.format( type( entry ).__name__, str( entry ) )

                        info = sys.exc_info( )[ -1 ]

                        while ( info ) :

                            entry += ' @ File = {} Line = {}'.format( info.tb_frame.f_code.co_filename.split( os.sep )[ -1 ], info.tb_lineno )

                            info = info.tb_next

                    logger.log( level.name, entry )

                except :

                    pass
