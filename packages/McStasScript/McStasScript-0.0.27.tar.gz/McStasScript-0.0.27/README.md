# McStasScript
[McStas](http://www.mcstas.org) API for creating and running McStas instruments from python scripting

Prototype for an API that allow interaction with McStas through an interface like Jupyter Notebooks created under WP5 of PaNOSC.

## Installation
McStasScript does not include the McStas installation, so McStas should be installed separately, link to instructions [here](https://github.com/McStasMcXtrace/McCode/tree/master/INSTALL-McStas).
McStasScript can be installed using pip from a terminal,

    python3 -m pip install McStasScript --upgrade

After installation it is necessary to configure the package so the McStas installation can be found, here we show how the appropriate code for an Ubuntu system as an example. The configuration is saved permanently, and only needs to be updated when McStas or McStasScript is updated. This has to be done from a python terminal or from within a python environment.

    from mcstasscript.interface import functions
    my_configurator = functions.Configurator()
    my_configurator.set_mcrun_path("/usr/bin/")
    my_configurator.set_mcstas_path("/usr/share/mcstas/2.5/")

To get a python terminal, run the command python in a terminal and then copy, paste and execute the lines above one at a time. Exit with ctrl+D.

For the second case, 
1. open a text editor (not MS Word but something like Gedit...),
2. copy and paste the code above,
3. save the file as a Python script, for example, myMcStasScript_config.py
4. In a terminal, run it by typing python myMcStasScript_config.py
    
On a Mac OS X system, the paths to the mcrun executable and mcstas folder are through the application folder:

    my_configurator.set_mcrun_path("/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/bin/")
    my_configurator.set_mcstas_path("/Applications/McStas-2.5.app/Contents/Resources/mcstas/2.5/")
    
    
### Notes on windows installation
McStasScript was tested on Windows 10 installed using this [guide](https://github.com/McStasMcXtrace/McCode/blob/master/INSTALL-McStas/Windows/README.md), it is necessary to include MPI using MSMpiSetup.exe and msmpisdk.msi located in the extras folder.

Open the McStas-shell cmd (shortcut should be available on desktop) and install McStasScript / jupyter notebook with these commands:

    python -m pip install notebook 
    python -m pip install McStasScript --upgrade
    
Using the McStas-shell one can start a jupyter notebook server with this command:

    jupyter notebook

For a standard McStas installation on Windows, the appropriate configuration can be set with these commands in a notebook:

    from mcstasscript.interface import functions
    my_configurator = functions.Configurator()
    my_configurator.set_mcrun_path("\\mcstas-2.6\\bin\\")
    my_configurator.set_mcstas_path("\\mcstas-2.6\\lib\\")
    
Double backslashes are necessary since backslash is the escape character in python strings.

## Instructions for basic use
This section provides a quick way to get started, a more in depth tutorial using Jupyter Notebooks is available in the tutorial folder. The following commands suppose that you are either typing them in a Python environment from a terminal or in a file to be run as the end of the editing by typing a command like, 'python my_file.py' or in a Jupyter notebook

Import the interface 

    from mcstasscript.interface import instr, plotter, functions, reader

Now the package can be used. Start with creating a new instrument, just needs a name

    my_instrument = instr.McStas_instr("my_instrument_file")

Then McStas components can be added, here we add a source and ask for help on the parameters

    my_source = my_instrument.add_component("source", "Source_simple")
    my_source.show_parameters() # Can be used to show available parameters for Source simple
    
The second line prints help on the Source_simple component and current status of our component object. The output is shown here, but without bold, underline and color which is used to show which parameters are required, default or user specified.

     ___ Help Source_simple _____________________________________________________________
    |optional parameter|required parameter|default value|user specified value|
    radius = 0.1 [m] // Radius of circle in (x,y,0) plane where neutrons are 
                        generated. 
    yheight = 0.0 [m] // Height of rectangle in (x,y,0) plane where neutrons are 
                         generated. 
    xwidth = 0.0 [m] // Width of rectangle in (x,y,0) plane where neutrons are 
                        generated. 
    dist = 0.0 [m] // Distance to target along z axis.
    focus_xw = 0.045 [m] // Width of target
    focus_yh = 0.12 [m] // Height of target
    E0 = 0.0 [meV] // Mean energy of neutrons.
    dE = 0.0 [meV] // Energy half spread of neutrons (flat or gaussian sigma).
    lambda0 = 0.0 [AA] // Mean wavelength of neutrons.
    dlambda = 0.0 [AA] // Wavelength half spread of neutrons.
    flux = 1.0 [1/(s*cm**2*st*energy unit)] // flux per energy unit, Angs or meV if 
                                               flux=0, the source emits 1 in 4*PI whole 
                                               space. 
    gauss = 0.0 [1] // Gaussian (1) or Flat (0) energy/wavelength distribution
    target_index = 1 [1] // relative index of component to focus at, e.g. next is 
                            +1 this is used to compute 'dist' automatically. 
    -------------------------------------------------------------------------------------

The parameters of the source can be adjusted directly as attributes of the python object

    my_source.xwidth = 0.12
    my_source.yheight = 0.12
    my_source.lambda0 = 3
    my_source.dlambda = 2.2
    my_source.focus_xw = 0.05
    my_source.focus_yh = 0.05
    
A monitor is added as well to get data out of the simulation (few bins so it is easy to print the results)

    PSD = my_instrument.add_component("PSD", "PSD_monitor", AT=[0,0,1], RELATIVE="source") 
    PSD.xwidth = 0.1
    PSD.yheight = 0.1
    PSD.nx = 5
    PSD.ny = 5
    PSD.filename = "\"PSD.dat\""

This simple simulation can be executed from the 

    data = my_instrument.run_full_instrument(foldername="first_run", increment_folder_name=True)

Results from the monitors would be stored as a list of McStasData objects in the returned data. The counts are stored as numpy arrays. We can read and change the intensity directly and manipulate the data before plotting.

    data[0].Intensity
    
In a python terminal this would display the data directly:

    array([[0.        , 0.        , 0.        , 0.        , 0.        ],
       [0.        , 0.1422463 , 0.19018485, 0.14156196, 0.        ],
       [0.        , 0.18930076, 0.25112956, 0.18897898, 0.        ],
       [0.        , 0.14121589, 0.18952508, 0.14098576, 0.        ],
       [0.        , 0.        , 0.        , 0.        , 0.        ]])
    
Plotting is usually done in a subplot of all monitors recorded.    

    plot = plotter.make_sub_plot(data)

## Use in existing project
If one wish to work on existing projects using McStasScript, there is a reader included that will read a McStas Instrument file and write the corresponding McStasScript python instrument to disk. Here is an example where the PSI_DMC.instr example is converted:

    Reader = reader.McStas_file("PSI_DMC.instr")
    Reader.write_python_file("PSI_DMC_generated.py")

It is highly advised to run a check between the output of the generated file and the original to ensure the process was sucessful.

## Method overview
Here is a quick overview of the available methods of the main classes in the project. Most have more options from keyword arguments that are explained in the manual, but also in python help. To get more information on for example the show_components method of the McStas_instr class, one can use the python help command help(instr.McStas_instr.show_components).

    instr
    └── McStas_instr(str instr_name) # Returns McStas instrument object on initialize
        ├── show_components(str category_name) # Show available components in given category
        ├── component_help(str component_name) # Prints component parameters for given component name   
        ├── add_component(str name, str component_name) # Adds component to instrument and returns object
        ├── add_parameter(str name) # Adds instrument parameter with name
        ├── add_declare_var(str type, str name) # Adds declared variable with type and name
        ├── append_initialize(str string) # Appends a line to initialize (c syntax)
        ├── print_components() # Prints list of components and their location
        ├── write_full_instrument() # Writes instrument to disk with given name + ".instr"
        └── run_full_instrument() # Runs simulation. Options in keyword arguments. Returns list of McStasData
        
    component # returned by add_component
    ├── set_AT(list at_list) # Sets component position (list of x,y,z positions in [m])
    ├── set_ROTATED(list rotated_list) # Sets component rotation (list of x,y,z rotations in [deg])
    ├── set_RELATIVE(str component_name) # Sets relative to other component name
    ├── set_parameters(dict input) # Set parameters using dict input
    ├── set_comment(str string) # Set comment explaining something about the component
    └── print_long() # Prints currently contained information on component
    
    functions
    ├── name_search(str name, list McStasData) # Returns data set with given name from McStasData list
    ├── name_plot_options(str name, list McStasData, kwargs) # Sends kwargs to dataset with given name
    ├── load_data(str foldername) # Loads data from folder with McStas data as McStasData list
    └── Configurator()
        ├── set_mcrun_path(str path) # sets mcrun path
        ├── set_mcstas_path(str path) # sets mcstas path
        └── set_line_length(int length) # sets maximum line length
    
    plotter
    ├── make_plot(list McStasData) # Plots each data set individually
    └── make_sub_plot(list McStasData) # Plots data as subplot
    
    reader
    └──  McStas_file(str filename) # Returns a reader that can extract information from given instr file

    InstrumentReader # returned by McStas_file
    ├── generate_python_file(str filename) # Writes python file with information contaiend in isntrument
    └── add_to_instr(McStas_instr Instr) # Adds information from instrument to McStasScirpt instrument
