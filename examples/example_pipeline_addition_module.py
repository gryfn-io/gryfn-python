# Example python script boilerplate to execute as part of a module.

if __name__ == '__main__':
    # Import cli from gryfn module. Critical in order to work with the
    # GUI. The only argument that must be supplied is the gpro location
    # you want to run your script on.
    from gryfn import cli
    import numpy

    # Add custom arguments to get additional data into your script
    # during module execution
    # In order for the GUI to pick up that you want to give it a file,
    # please use the cli.FileString argument for the type, and the
    # UI will open a file browser for your pleasure.
    cli.arguments.add_argument("--plots", type=cli.FileString, help='location of plots file to use with data')
    cli.arguments.add_argument("--number", type=float, default=1.0, help="a number")

    # Call cli.parse_args() to parse the base arguments + your extensions. This must be called,
    # regardless of whether you add additional arguments to the script.
    args = cli.parse_args()

    # args.gpro will already be represented by the GPro class.
    # No need to instantiate a GPro. This cli will provide it
    # for you.

    #######################
    # The rest of the script is pure userland. This can look
    # however you want it to. Feel free to bake the entire
    # processing script into one python file, or, for better
    # maintainability, consider creating re-usable modules
    # that will generalize your interactions with the data.

    # Get your custom script arguments
    plot_file = args.plots

    # Import whatever libraries and modules you need to process your data
    from analysis_library import process_data
    process_data(args.gpro, plot_file)

