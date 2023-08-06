import abc
import os
import logging
import subprocess

from yaerrrr import models
import tempfile


class AbstractYaerrrrScript(abc.ABC):

    @abc.abstractmethod
    def generate_er(self, context: 'models.YaerrrContext') -> "models.ErDiagram":
        pass

    def run(self, output_file: str):
        context = models.YaerrrContext()
        er = self.generate_er(context)
        self._build_image(er, output_file)

    def _build_image(self, diagram: "models.ErDiagram", output_file: str) -> str:
        fd, dot_name = tempfile.mkstemp(suffix=".dot")

        try:

            with open(dot_name, mode="w", encoding="ascii") as dot_file:
                dot_file.writelines([f"digraph {diagram.er.name} {{"])

                # NODES
                for n in diagram.er.nodes:
                    if isinstance(n, models.Diamond):

                        if len(list(n.fields)) > 0:
                            fields = [f"<tr><td>{f.name}</td><td>{f.datatype}</td></tr>" for f in n.fields]
                            label = f"""\tlabel=<<table border="0" cellborder="1" cellspacing="0"><tr><td colspan="2"><b>{n.name}</b></td></tr>{''.join(fields)}</table>>"""
                        else:
                            label = f"""\tlabel=\"{n.name}\""""
                        dot_file.writelines([
                            f"N_{n.get_id()} [",
                            f"\tshape=diamond,",
                            label,
                            f"]",
                        ])
                    elif isinstance(n, models.Comment):
                        dot_file.writelines([
                            f"N_{n.get_id()} [",
                            f"\tshape=none,",
                            f"""\tlabel={n.description}""",
                            f"]",
                        ])
                    elif isinstance(n, models.Entity):
                        fields = [f"<tr><td>{f.name}</td><td>{f.datatype}</td></tr>" for f in n.fields]
                        dot_file.writelines([
                            f"N_{n.get_id()} [",
                            f"\tshape=none,",
                            f"""\tlabel=<<table border="0" cellborder="1" cellspacing="0"><tr><td colspan="2"><b>{n.name}</b></td></tr>{''.join(fields)}</table>>""",
                            f"]",
                        ])
                    else:
                        raise ValueError(f"Invalid node {type(n)}!")

                # EDGES

                for source, sink, e in diagram.er.edges.data('weight'):
                    if isinstance(e, models.DashedEdge):
                        dot_file.writelines([f"""N_{source.get_id()} -> N_{sink.get_id()} [style="dashed", arrowhead="none", arrowtail="none"]"""])
                    elif isinstance(e, models.ImplementsErEdge):
                        dot_file.writelines([f"""N_{source.get_id()} -> N_{sink.get_id()} [style="solid", arrowhead="none", arrowtail="empty", arrowsize=2]"""])
                    elif isinstance(e, models.RelationshipConnection):
                        if e.position == models.LabelPosition.HEAD:
                            head = e.label
                            tail = ""
                            middle = ""
                        elif e.position == models.LabelPosition.MIDDLE:
                            head = ""
                            tail = ""
                            middle = e.label
                        elif e.position == models.LabelPosition.TAIL:
                            head = ""
                            tail = e.label
                            middle = ""
                        else:
                            raise ValueError(f"Invalid position {e.position}")

                        dot_file.writelines([f"""N_{source.get_id()} -> N_{sink.get_id()} [style="solid", arrowhead="none", arrowtail="none", headlabel="{head}", taillabel="{tail}", label="{middle}"]"""])
                    else:
                        raise ValueError(f"Invalid edge label {type(e)}!")

                dot_file.writelines(["}"])

            extension = os.path.splitext(output_file)[1].lstrip('.')
            cmd = [
                "dot",
                f"-T{extension}",
                f"-o {output_file}",
                f"{dot_name}",
            ]
            logging.info(' '.join(cmd))
            subprocess.run(cmd)

        finally:
            os.close(fd)

        os.unlink(dot_name)

        return output_file


