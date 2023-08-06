from cloudmesh.diagram.diagram import Diagram

from cloudmesh.common.parameter import Parameter
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.shell.command import map_parameters


class DiagramCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_diagram(self, args, arguments):
        """
        ::

          Usage:
                diagram set CLUSTER --hostname=NAMES
                diagram set CLUSTER NAME ATTRIBUTE VALUE
                diagram rack CLUSTER [--output=FORMAT] [-n]
                diagram net CLUSTER [--output=FORMAT] [-n]


          This command produces some default network and rack diagrams for a
          small cluster setup.

          Arguments:
              FILE   a file name
              --output=FORMAT   THe output format, one of svg, png, pdf, gif
                                The default is svg


          Options:
              -f      specify the file
              -n      no preview, just save to file

          Example:

                Installation:
                    pip install cloudmesh-diagram

                Create a rack diagram:
                    cms diagram set d --hostname="red[00-04]"
                    cms diagram set d red01 rack.color blue
                    cms diagram set d red02 net.color red
                    cms diagram rack d
                    cms diagram net d
                    cms diagram net d --output=png -n

        """

        map_parameters(arguments, 'hostname', 'output')
        arguments.view = not arguments["-n"]

        arguments.output = arguments.output or "svg"

        if arguments.set and arguments.hostname:

            hostnames = Parameter.expand(arguments.hostname)
            rack = Diagram(hostnames)
            name = arguments.CLUSTER
            rack.save(name)

        elif arguments.set and arguments.NAME:
            rack = Diagram()
            rack.load(arguments.CLUSTER)
            data = {
                arguments.ATTRIBUTE: arguments.VALUE
            }
            rack.set(arguments.NAME, **data)
            rack.save(arguments.CLUSTER)

        elif arguments.rack:
            diag = f"{arguments.CLUSTER}-rack"
            rack = Diagram()
            rack.load(arguments.CLUSTER)
            rack.render(kind="rack")
            rack.save_diagram(diag)
            rack.saveas(diag, kind="rack", output=arguments.output)
            if arguments.view:
                rack.view(diag, output=arguments.output)

        elif arguments.net:
            diag = f"{arguments.CLUSTER}-net"
            net = Diagram()
            net.load(arguments.CLUSTER)
            net.render(kind="bridge")
            net.save_diagram(diag)
            net.saveas(diag, kind="net", output=arguments.output)
            if arguments.view:
                net.view(diag, output=arguments.output)

        return ""
