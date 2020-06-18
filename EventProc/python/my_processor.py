"""Example configuration object for a processor"""

# We need the ldmx configuration package to construct the processor objects
from LDMX.Framework import ldmxcfg

class MyProcessor(ldmxcfg.Producer) :
    """The name is purely conventional to match the C++ class name for clarity

    The line
        super().__init__( name , "ldmx::MyProcessor" )

    Calls the constructor for ldmxcfg.Producer, which is how we have handles
    on this processor. You need to give the actual C++ class name with 
    namespace(s) as the second entry.

    Any other lines define parameters that are accessible in the C++
    configure method. For example, the line
        self.my_parameter = 20

    defines a integer parameter for this class which can be accessed
    in the configure method with
        int my_parameter = parameters.getParameter<int>("my_parameter");

    The lines
        from LDMX.EventProc import include
        include.library()

    Attach the EventProc library to the Process so that the
    processors can be dynamically loaded. If you are in a different
    module, you will need to change 'EventProc' to the name
    of the module you are in.

    Examples
    --------

    Creating the configuration object gives the parameters set
    in __init__.
        myProc = MyProcessor( 'myProc')

    You can also change the parameters after creating this object.
        myProc.my_parameter = 50

    Then you put your processor into the sequence of the process.
        p.sequence.append( myProc )
    """

    def __init__(self, name ):
        super().__init__( name , "ldmx::MyProcessor" )

        from LDMX.EventProc import include
        include.library()

        self.my_parameter = 20