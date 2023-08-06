import Simple_Process_REPL.core as r
from Simple_Process_REPL.options import define_help_text
import Particle_Board_REPL.particle as P
import regex as re
import logging
import os
import yaml


"""
The purpose of this module is to Serve as a liaison between the
Interpreter/REPL and the device interface layer, which in this case is
defined in particle.py

The Repl module requires two symbol tables, and a dictionary of
defaults, as well as any stateful data the application would like to keep.
In this case it is the _device_ dictionary below.

In many cases particle functions may be used directly in the symbol table.
In other cases where additional functionality,
or data use is needed, the function would be defined here.

The symbol table of these functions is defined and passed to
to the repl core module which is reponsible for similar things
as well as parsing the command line, setting up logging, and
executing the process as desired.
"""

# This is a map which is merged with the application state map.
# Defaults are used by the cli where appropriate.
# device is our particle board, we need it's id, and the
# the path of it's device, ie. /dev/ttyUSB..., The board
# name is boron, photon, whatever. and the last_id just
# in case we need it.

# Particle board interface state
PB = {
    "device": {"id": "", "name": "", "path": "", "last_id": ""},
    "defaults": {
        "config_file": "pbr-config.yaml",
        "loglevel": "info",
        "logfile": "PBR.log",
    },
}

PB |= r.load_defaults("Particle_Board_REPL", "PBR-defaults.yaml")

logger = logging.getLogger()

prefix = """PBR, The Particle_Board_REPL, is an application
Built upon the Simple_Process_REPL. It is intended to make it easy
to interact, program and test Particle.io Boards.
Using the REPL with `PBR -r` is the easiest way to get to know
the features of this application. By default configurations files are
loaded so that basic functionalities are provided for. If a configuration
file is present it will be merged into the defaults. A configuration file
can be created with the `save_config` command.
"""

suffix = ""

define_help_text(prefix, suffix)


def see_images():
    """Ask if the test images are seen, fail if not."""
    yno_msg = r.get_in_config(["dialogs", "images_seen"])
    if not r.ynbox(yno_msg):
        raise Exception("Failure: Test images not Seen.")


def input_serial():
    """
    Function called by test handshake, Asks if images are seen,
    then presents a dialog loop to receive an 8 digit serial number
    to be returned back to the handshake and sent to the device.
    """
    see_images()

    msg = r.get_in_config(["dialogs", "input_serial"])
    while True:
        code, res = r.inputbox(
            msg, title=r.get_in_config(["dialogs", "title"]), height=10, width=50
        )
        if re.match(r"^\d{8}$", res):
            yno_msg = "%s : %s" % (
                r.get_in_config(["dialogs", "serial_is_correct"]),
                res,
            )
            if r.ynbox(yno_msg):
                break
        else:
            r.msgbox(r.get_in_config(["dialogs", "serial_must"]))

    os.system("clear")
    logger.info("Serial Number Entered is: %s" % res)
    return res


def flash_image():
    "Flash the flash image"
    P.flash(r.get_in_config(["images", "flash"]))


def flash_tinker():
    "Flash the tinker image"
    P.flash(r.get_in_config(["images", "tinker"]))


def flash_test():
    "Flash the test image"
    P.flash(r.get_in_config(["images", "test"]))


def product_add():
    """ product device add product id - associate the device wit a product"""
    P.product_add(r.get_in_config(["particle", "product"]), r.get_in_device("id"))


def claim():
    "Claim the device, cloud claim"
    P.claim(r.get_in_device("id"))


def add():
    "Claim the device, device add"
    P.add(r.get_in_device("id"))


def release():
    "Release the claim on a device."
    P.release(r.get_in_device("id"))


def cloud_status():
    "Check to see if the device is connected to the cloud"
    P.cloud_status(r.get_in_device("id"))


def reset_usb():
    "Reset the usb device."
    P.reset_usb(r.get_in_device("id"))


def list_usb_w_timeout():
    "Do a serial list repeatedly for timeout period"
    P.list_usb_w_timeout(r.get_in_config(["waiting", "timeout"]))


def get_usb_and_id():
    """
    Retrieve and set the USB device, the board name,  and the device id.
    Uses 'particle serial list' in a timeout loop. This is required
    for most things. Wait and handshake, use the usb device,
    and the id is needed by many things.
    """
    # PB['usb_device'], PB['device_id'] = P.get_usb_and_id()
    path, name, id = P.get_w_timeout(r.get_in_config(["waiting", "timeout"]))

    r.set({"device": {"path": path, "name": name, "id": id}})
    r.show()


def wait_for_plist():
    """Wait for particle serial list to succeed with timeout, doesn't
    really work."""
    # we don't care about the results, just to wait.
    P.get_w_timeout(r.get_in_config(["waiting", "timeout"]))


def archive_log():
    "Move the current logfile to one named after the current device."
    r.archive_log("%s.log" % r.get_in_device("id"))


def particle_help():
    """A function to provide additional Application specific help."""
    print(
        """\n\n Particle Process help:\n
Particle help can be accessed directly at any time with the 'particle-help'
command.\n
When working with a Particle.io board, the first step is to 'get'
the id and device. There are many commands here which need the usb device
or the device id.  With that, the basic commands for the process we have
been intending would be;

'start, setup, claim, testit, flash, and archive_log'.

Note that 'start', 'setup', and 'testit', are user defined commands which are
actually lists of other commands. These are defined in the configuration
file.  Help lists the source for these commands.
'start' is actually; 'dialog-start get wait identify'

The 'continue to next' and 'device failed' dialog windows are built in to
the interactive loop. Any additional prompts, such as 'dialog-start' or
'dialog-test' can be added to the process  with their commands.
and prompt texts are defined in the configuration, which can be
seen with 'showin config'.

When a process is deemed good, the autoexec can be set to it, and that
will be what runs automatically, in the process loop, or as a oneshot,
if no commands are given on the cli.\n\n """
    )


symbols = [
    ["dfu", P.dfu_mode, "Put the device in dfu mode."],
    ["listen", P.listen, "Put the device in listening mode."],
    ["list", P.list_usb, "List the particle boards connected to USB."],
    ["reset", reset_usb, "Reset the usb device"],
    ["identify", P.identify, "listen and identify"],
    ["inspect", P.inspect, "Inspect the device"],
    ["login", P.login, "Login to the particle cloud."],
    ["logout", P.logout, "Logout of the particle cloud."],
    ["update", P.update, "dfu/Update device, dfu then update"],
    ["setup-done", P.set_setup_bit, "Set the Setup bit."],
    ["add", add, "Add/claim device"],
    ["product-add", product_add, "Add device to a product"],
    ["claim", claim, "Cloud claim the device"],
    ["release", P.release, "Release claim on device"],
    ["flash", flash_image, "dfu/Flash the configured image"],
    ["tinker", flash_tinker, "dfu/Flash tinker onto device"],
    ["flash-test", flash_test, "Flash the test, only, the handshake is up to you."],
    ["_doctor", P.doctor, "run particle doctor"],
    ["cloud-status", cloud_status, "Get the cloud status of the current device"],
    ["get", get_usb_and_id, "Get the USB device and the device id."],
    ["archive-log", archive_log, "Archive the log to the the device id."],
    ["input-serial", input_serial, "Dialog to receive an 8 digit serial number."],
    ["particle-help", particle_help, "Additional Application layer help."],
]


# Name, function, number of args, help string
# Commands we want in the repl which can take arguments.
# look in rcore.py for examples.
specials = [
    [
        "_flash",
        P.flash,
        1,
        "Flash the specified image; _flash boron-system-part1@2.0.1.bin",
    ]
]


# get the default parser for the application and add to it if desired.
parser = None
# parser = r.get_parser()
# parser.add_argument("-f", "--foo", action="store_true", help="set foo")


def init():
    """
    Call into the interpreter/repl with our stuff,
    This starts everything up.
    """
    r.init(symbols, specials, parser)
