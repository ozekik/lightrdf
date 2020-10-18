import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
from matplotlib.ticker import FuncFormatter

# matplotlib.use("Agg")


def format_timedelta(x, pos):
    minutes = int((x % (60 * 60)) // 60)
    seconds = float(x % 60)

    return "{:d}m{:.0f}s".format(minutes, seconds)


formatter = FuncFormatter(format_timedelta)

labels = ["RDFLib 4.2.2", "LightRDF 0.1.1\n(RDFDocument)", "LightRDF 0.1.1\n(Parser)"]
values = ["3:59.56", "0:08.27", "0:08.47"]
values = list(
    map(
        lambda x: datetime.timedelta(
            minutes=int(x.split(":")[0]), seconds=float(x.split(":")[1])
        ),
        values,
    )
)
values = list(map(lambda x: x.seconds, values))

with plt.xkcd():
    fig, ax = plt.subplots()

    ax.set_title("Parsing 1436427 triples (go.owl)", fontsize=14)
    ax.bar(labels, values)
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=30))
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=1))

    fig.tight_layout()
    # plt.show()
    fig.savefig("benchmark1.png")


labels = ["RDFLib 4.2.2", "LightRDF 0.1.1\n(NTTriplesParser)"]
values = ["0:02.47", "0:00.36"]
values = list(
    map(
        lambda x: datetime.timedelta(
            minutes=int(x.split(":")[0]), seconds=float(x.split(":")[1])
        ),
        values,
    )
)
values = list(map(lambda x: x.seconds, values))

with plt.xkcd():
    fig, ax = plt.subplots()

    ax.set_title("Parsing 31050 triples (dbpedia_2016-10.nt)", fontsize=14)
    ax.bar(labels, values)
    ax.yaxis.set_major_formatter(formatter)
    ax.set_ylim(0, 60)
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=10))
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=1))

    fig.tight_layout()
    # plt.show()
    fig.savefig("benchmark2.png")
