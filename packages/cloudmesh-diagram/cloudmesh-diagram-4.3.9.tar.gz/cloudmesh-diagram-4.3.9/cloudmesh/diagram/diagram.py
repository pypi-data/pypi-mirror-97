import json
import subprocess
import textwrap
from collections import OrderedDict

import oyaml as yaml

from cloudmesh.common.util import path_expand
from cloudmesh.common.console import Console


class Diagram(object):
    """
    A class to draw nic rack diagrams

    Example:

        from cloudmesh.diagram.rack import Rack

        rack = Rack(names=arguments.hostnames)

        pprint(rack)

        rack.set("red01", color="blue")
        rack.set("red02", color="green")
        rack.set("red03", textcolor="red")
        rack.set("red04", shape="cloud")
        rack.set("red02", numbered="1")

        name = "mycluster"  # filename for storing the data, no endong for now
        rack.render(name)

        rack.save(name)

        rack.svg(name)
        rack.view(name)


    """
    def __init__(self, names=None, name=None, data=None):
        self.diag = None
        if names is not None:
            self.names = names
            if name is None:
                self.name = names[0]
            else:
                self.name = name
            self.servers = len(names)
            if data is None:
                self.data = OrderedDict()
                counter = 1
                for name in names:
                    self.data[name] = {
                        "net.color": "white",
                        "rack.color": "white",
                        "label": name,
                        "numbered": "",
                        "fontsize": "",
                        "shape": "",
                        "textcolor": "",
                    }
                    counter = counter + 1
            else:
                self.data = data
        else:
            self.names = names
            self.name = name
            self.data = data
            self.servers = 0

    def render(self, kind="rack"):
        if kind == "rack":
            return self.render_rack()
        elif kind == "bridge":
            return self.render_bridge_net()
        else:
            Console.error("Diagram type not supported")

    def render_bridge_net(self):

        manager = self.names[0]
        header = textwrap.dedent("""
        nwdiag {
          # network internet{
          #    address = "xxx.xxx.xxx.xxx"
          #    modem
          #}
          network wifi {
              address = "192.168.50.x"
              # modem

              manager [address = "192.168.50.100"];
              laptop [address = "192.168.50.100"];
              }
          network internal {
              address = "10.0.0.x";
        """).replace("manager", manager)

        servers = {}
        counter = 1
        for name in self.data:
            parameters = []
            for attribute in self.data[name]:
                if attribute == "rack.color":
                    continue
                value = self.data[name][attribute]
                if attribute == "net.color":
                    attribute = "color"
                if value is not None and value != "":
                    parameters.append(
                        f"{attribute}=\"{value}\""
                    )
            parameters.append(f'address = "10.0.0.{counter}"')
            parameters = ", ".join(parameters)
            servers[name] = f'      {name} [ {parameters} ];'
            counter = counter + 1

        workers = []
        for worker in servers:
            server = servers[worker]
            workers.append(server)

        workers = "\n".join(workers)

        footer = textwrap.dedent("""
          }
        }
        """)

        self.diag = header + workers + footer
        return self.diag

    def render_rack(self):

        name = self.names[0]

        header = "rackdiag {" + textwrap.dedent(f"""
              // Change order of rack-number as ascending
              ascending;

              // define height of rack
              {self.servers}U;

              // define description of rack
              description = "{name}";

              // define rack units
        """)

        footer = "\n}"

        servers = []
        counter = 1
        for name in self.data:
            parameters = []
            for attribute in self.data[name]:
                if attribute == "net.color":
                    continue
                value = self.data[name][attribute]
                if attribute == "rack.color":
                    attribute = "color"
                if value is not None and value != "":
                    parameters.append(
                        f"{attribute}=\"{value}\""
                    )
            parameters = ", ".join(parameters)
            servers.append(
                f'{counter}: {name} [ {parameters} ]'
            )
            counter = counter + 1

        servers = "\n".join(servers)

        self.diag = header + servers + footer

        return self.diag

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def set(self, name, **kwargs):
        for attribute in kwargs:
            value = kwargs[attribute]
            self.data[name][attribute] = value

    def set_color(self, name, color):
        self.set(name, color=color)

    def set_label(self, name, label):
        self.set(name, label=label)

    def set_numbering(self, name, numbering):
        self.set(name, numbering=numbering)

    def set_fontsize(self, name, fontsize):
        self.set(name, fontsize=fontsize)

    def set_textcolorl(self, name, textcolorl):
        self.set(name, textcolorl=textcolorl)

    def set_shape(self, name, shape):
        self.set(name, shape=shape)

    def save(self, filename):
        data = {
            "name": self.name,
            "names": self.names,
            "data": self.data
        }

        with open(path_expand(filename), 'w') as f:
            yaml.safe_dump(data, f)

    def load(self, filename):
        with open(path_expand(filename), 'r') as f:
            content = yaml.safe_load(f)
            self.names = content["names"]
            self.data = content["data"]
            self.name = content["name"]
            self.servers = len(self.names)

    def save_diagram(self, name):
        filename = path_expand(name)
        with open(f'{filename}.diag', 'w') as f:
            f.write(self.diag)
            f.write("\n")
            f.flush()

    def svg(self, name, kind="rack"):
        self.saveas(name, kind=kind, output="svg")

    def png(self, name, kind="rack"):
        self.saveas(name, kind=kind, output="png")

    def pdf(self, name, kind="rack"):
        self.saveas(name, kind=kind, output="pdf")

    def gif(self, name, kind="rack"):
        self.saveas(name, kind=kind, output="gif")

    def saveas(self, name, kind="rack", output="svg"):
        filename = path_expand(name)
        self.save_diagram(name)
        if kind == 'rack':
            cmd = ['rackdiag', "-T", output, f"{filename}.diag"]
        elif kind == "net":
            cmd = ['nwdiag', "-T", output, f"{filename}.diag"]
        subprocess.Popen(cmd).wait()

    def view(self, name, output="svg"):
        filename = path_expand(name)
        cmd = ['open', f"{filename}.{output}"]
        subprocess.Popen(cmd)

    def __repr__(self):
        return json.dumps(self.data, indent=4)
