import numpy as np
import plotly
import plotly.graph_objects as go
from plotly.io import write_image
import random

class PlotlyDynamicPlotter:
    def __init__(self, labels=["x", "y", "z"], title="", aspectratio=None, xrange=None, yrange=None, zrange=None, showSpikes=True, spikeColor="#000000", bgcolor="#fff", fontsize=10):
        self.labels = labels

        axis = dict(showline=True,
                    linewidth=4,
                    title=dict(font=dict(size=20)),
                    showticklabels=False,
                    backgroundcolor=bgcolor)

        layout = go.Layout(scene= dict(
            xaxis_title=labels[0],
            yaxis_title=labels[1],
            zaxis_title=labels[2],
            xaxis=axis,
            yaxis=axis,
            zaxis=axis),
            font=dict(
                size=fontsize)
            )

        self.fig = go.Figure(layout=layout)
        if xrange:
            self.fig.update_layout(scene=dict(
                xaxis=dict(range=xrange, showbackground=True)
            ))
        if yrange:
            self.fig.update_layout(scene=dict(
                yaxis=dict(range=yrange, showbackground=True)
            ))
        if zrange:
            self.fig.update_layout(scene=dict(
                zaxis=dict(range=zrange, showbackground=True)
            ))
        if showSpikes:
            self.fig.update_layout(scene=dict(
                xaxis=dict(spikecolor=spikeColor,
                           spikesides=False,
                           spikethickness=2),
                yaxis=dict(spikecolor=spikeColor,
                           spikesides=False,
                           spikethickness=2),
                zaxis=dict(spikecolor=spikeColor,
                           spikesides=False,
                           spikethickness=2)
            ))
        else:
            self.fig.update_layout(scene=dict(
                xaxis=dict(showspikes=False),
                yaxis=dict(showspikes=False),
                zaxis=dict(showspikes=False)
            ))
        self.fig.update_layout(title=dict(text=title, font=dict(size=35), x=0.5, xanchor="center", y=0.8, yanchor="top"))
        if aspectratio:
            self.fig.update_layout(scene_aspectmode='manual', scene_aspectratio=dict(x=aspectratio[0], y=aspectratio[1], z=aspectratio[2]))

    def plotTrajectory3D(self, trajectory, color="#{:06x}".format(random.randint(0, 0xFFFFFF)).upper(), xc=1, yc=2, zc=3, name="", t=None, showlegend=False, opacity=1, linewidth=2, dash='solid'):
        hinfo = "%{fullData.name}<br><br>" + self.labels[0] + ": %{x}<br>" + self.labels[1] + ": %{y}<br>" + self.labels[2] + ": %{z}<br><br>" + r"tau: %{text}<extra></extra>"

        xs = np.array([x[xc] for x in trajectory]).flatten()
        ys = np.array([x[yc] for x in trajectory]).flatten()
        zs = np.array([x[zc] for x in trajectory]).flatten()

        self.fig.add_scatter3d(x=xs, y=ys, z=zs, mode="lines", line=go.scatter3d.Line(color=color, width=linewidth, dash=dash), name=name,
                               hoverinfo='all', opacity=opacity)
        if t is not None:
            self.fig['data'][-1].update(text=t)

        self.fig['data'][-1].update(hovertemplate=hinfo)

        self.fig['data'][-1].update(showlegend=showlegend)


    def plotHyperboloid(self, l=1, vsize=(-2,2), opacity=0.5, plot_edges=False,  color="rgb(" + str(random.randint(50,100)) + "," + str(random.randint(50,100)) + "," + str(random.randint(50,100)) + ")", drawImpulse=False, showlegend=False, drawCoords=False):
        """
        Generate hyperboloid
        :param l: Cosmological constant
        """
        import plotly.figure_factory as ff #I hope Python is clever!
        from scipy.spatial import Delaunay

        eps = np.sign(l)
        a = np.sqrt(3/np.abs(l))
        u = np.linspace(0, 2 * np.pi, 90)
        v = np.linspace(vsize[0], vsize[1], 90) #TODO: resolution should not be hard-coded

        u, v = np.meshgrid(u, v)

        u = u.flatten()
        v = v.flatten()

        if(eps > 0):
            x = a * np.cosh(v/a) * np.cos(u)
            y = a * np.cosh(v/a) * np.sin(u)
            z = a * np.sinh(v/a)
        else:
            x = a * np.cosh(v/a) * np.cos(u)
            z = a * np.cosh(v/a) * np.sin(u)
            y = a * np.sinh(v/a)

        points2D = np.vstack([u, v]).T

        tri = Delaunay(points2D)
        simplices = tri.simplices

        _tempfig = ff.create_trisurf(x=x, y=y, z=z, simplices=simplices, show_colorbar=False, colormap=color, plot_edges=plot_edges,
                                     aspectratio=dict(x=1, y=1, z=0.8))
        _tempfig['data'][0].update(opacity=opacity)
        _tempfig['data'][0].update(hoverinfo='skip')
        _tempfig['data'][0].update(hoverinfo='skip')
        _tempfig['data'][0].update(name="Hyperboloid")
        _tempfig['data'][0].update(showlegend=showlegend)
        if drawImpulse:
            v = np.linspace(vsize[0], vsize[1], 10)
            z = v[:-1]
            y = v[:-1]
            x = 10 * [-a]
            x2 = 10 * [a]

            _tempfig.add_scatter3d(x=x, y=y, z=z, mode="lines", line=go.scatter3d.Line(color="black", width=4), name="U = infinity", hoverinfo='skip', showlegend=showlegend, opacity=0.4)
            _tempfig.add_scatter3d(x=x2, y=y, z=z, mode="lines", line=go.scatter3d.Line(color="black", width=8), name="U = 0", hoverinfo='skip', showlegend=showlegend, opacity=0.8)

        if drawCoords:
            b = a + 0.005
            bm = a - 0.005
            u = np.linspace(0, 2 * np.pi, 12)
            ud = np.linspace(0, 2 * np.pi, 120)
            v = np.linspace(vsize[0], vsize[1], 12)
            vd = np.linspace(vsize[0], vsize[1], 120)
            #u const
            for u0 in u:
                if (eps > 0):
                    x = b * np.cosh(vd / b) * np.cos(u0)
                    xm = bm * np.cosh(vd / bm) * np.cos(u0)
                    y = b * np.cosh(vd / b) * np.sin(u0)
                    ym = bm * np.cosh(vd / bm) * np.sin(u0)
                    z = b * np.sinh(vd / b)
                    zm = bm * np.sinh(vd / bm)
                else:
                    x = b * np.cosh(vd / b) * np.cos(u0)
                    xm = bm * np.cosh(vd / bm) * np.cos(u0)
                    y = b * np.sinh(vd / b)
                    ym = bm * np.sinh(vd / bm)
                    z = b * np.cosh(vd / b) * np.sin(u0)
                    zm = bm * np.cosh(vd / bm) * np.sin(u0)
                _tempfig.add_scatter3d(x=x, y=y, z=z, mode="lines", line=go.scatter3d.Line(color="black", width=2),
                                       showlegend=False, opacity=1, name="", hoverinfo='skip')
                _tempfig.add_scatter3d(x=xm, y=ym, z=zm, mode="lines", line=go.scatter3d.Line(color="black", width=2),
                                       showlegend=False, opacity=1, name="", hoverinfo='skip')
            #v const
            for v0 in v:
                if (eps > 0):
                    x = b * np.cosh(v0 / b) * np.cos(ud)
                    y = b * np.cosh(v0 / b) * np.sin(ud)
                    z = b * np.sinh(v0 / b) * np.ones_like(ud)
                    xm = bm * np.cosh(v0 / bm) * np.cos(ud)
                    ym = bm * np.cosh(v0 / bm) * np.sin(ud)
                    zm = bm * np.sinh(v0 / bm) * np.ones_like(ud)
                else:
                    x = b * np.cosh(v0 / b) * np.cos(ud)
                    y = b * np.sinh(v0 / b) * np.ones_like(ud)
                    z = b * np.cosh(v0 / b) * np.sin(ud)
                    xm = bm * np.cosh(v0 / bm) * np.cos(ud)
                    ym = bm * np.sinh(v0 / bm) * np.ones_like(ud)
                    zm = bm * np.cosh(v0 / bm) * np.sin(ud)

                _tempfig.add_scatter3d(x=x, y=y, z=z, mode="lines", line=go.scatter3d.Line(color="black", width=2),
                                       showlegend=False, opacity=1, name="", hoverinfo='skip')
                _tempfig.add_scatter3d(x=xm, y=ym, z=zm, mode="lines", line=go.scatter3d.Line(color="black", width=2),
                                       showlegend=False, opacity=1, name="", hoverinfo='skip')

        self.fig.add_traces(_tempfig.data)


    def plotCutAndPasteHyperboloid(self, H, l, vsize=(-2, 2), opacity=0.5, plot_edges=False,  color="rgb(" + str(random.randint(50,100)) + "," + str(random.randint(50,100)) + "," + str(random.randint(50,100)) + ")", drawImpulse=False, showlegend=False):
        from scipy.spatial import Delaunay

        a = np.sqrt(3 / np.abs(l))
        eps = np.sign(l)
        uo = np.linspace(0, 2 * np.pi, 650)
        v = np.linspace(vsize[0], vsize[1], 550)  # TODO: resolution should not be hard-coded

        uo, v = np.meshgrid(uo, v)

        u = uo.flatten()
        v = v.flatten()
        #TODO: OPRAVIT, ZKUST https://stackoverflow.com/questions/25060103/determine-sum-of-numpy-array-while-excluding-certain-values
        if (eps > 0):
            x = a * np.cosh(v / a) * np.cos(u)
            z = a * np.sinh(v / a)
            y = a * np.cosh(v / a) * np.sin(u)

        else:
            x = a * np.cosh(v/a) * np.cos(u)
            z = a * np.cosh(v / a) * np.sin(u)
            y = a * np.sinh(v / a)

        xp = np.array([a if c - b >= 0 else np.nan for a, b, c in zip(x, y, z)]).reshape(uo.shape)
        xm = np.array([a if c - b <= 0 else np.nan for a, b, c in zip(x, y, z)]).reshape(uo.shape)
        yp = np.array([b - 1. / np.sqrt(2) * H if c - b >= 0 else np.nan for a, b, c in zip(x, y, z)]).reshape(uo.shape)
        ym = np.array([b if c - b <= 0 else np.nan for a, b, c in zip(x, y, z)]).reshape(uo.shape)
        zp = np.array([c + 1. / np.sqrt(2) * H if c - b >= 0 else np.nan for a, b, c in zip(x, y, z)]).reshape(uo.shape)
        zm = np.array([c if c - b <= 0 else np.nan for a, b, c in zip(x, y, z)]).reshape(uo.shape)

        _tempfig = go.Figure(data=[
            go.Surface(x=xp, y=yp, z=zp, colorscale=[color, color]),
            go.Surface(x=xm, y=ym, z=zm, colorscale=[color, color])
        ])
        _tempfig['data'][0].update(name="Hyperboloid +")
        _tempfig['data'][1].update(name="Hyperboloid -")
        _tempfig.update_traces(showscale=False, opacity=opacity, hoverinfo='skip', showlegend=showlegend)
        if drawImpulse:
            v = np.linspace(vsize[0], vsize[1], 10)
            z = v[:-1]
            y = v[:-1]
            x = 10 * [-a]
            x2 = 10 * [a]

            _tempfig.add_scatter3d(x=x, y=y, z=z, mode="lines", line=go.scatter3d.Line(color="black", width=4),
                                   name="U- = infinity", hoverinfo='skip', showlegend=showlegend , opacity=0.4)
            _tempfig.add_scatter3d(x=x2, y=y, z=z, mode="lines", line=go.scatter3d.Line(color="black", width=8),
                                   name="U- = 0", hoverinfo='skip', showlegend=showlegend, opacity=0.8)
            _tempfig.add_scatter3d(x=x , y=y - 1. / np.sqrt(2) * H, z=z + 1. / np.sqrt(2) * H, mode="lines", line=go.scatter3d.Line(color="black", width=4),
                                   name="U+ = infinity", hoverinfo='skip', showlegend=showlegend, opacity=0.4)
            _tempfig.add_scatter3d(x=x2, y=y - 1. / np.sqrt(2) * H, z=z + 1. / np.sqrt(2) * H, mode="lines", line=go.scatter3d.Line(color="black", width=8),
                                   name="U+ = 0", hoverinfo='skip', showlegend=showlegend, opacity=0.8)

        self.fig.add_traces(_tempfig.data)


    def plotSurface(self, f, *args, xdomain=[-1, 1], ydomain=[-1, 1], xstep=0.05, ystep=0.05, color="rgb(" + str(random.randint(50,100)) + "," + str(random.randint(50,100)) + "," + str(random.randint(50,100)) + ")", color2=None, complexNull=False, name="Surface", showlegend=False):
        x = np.arange(xdomain[0], xdomain[1], xstep)
        y = np.arange(ydomain[0], ydomain[1], ystep)
        #X, Y = np.meshgrid(x, y)
        z = np.zeros((x.size, y.size))
        for i in range(x.size):
            for j in range(y.size):
                if complexNull:
                    z[i, j] = f(x[i] + 1j * y[j], x[i] - 1j * y[j], args)
                else:
                    z[i, j] = f(x[i], y[j], args)
                if z[i, j] == np.NaN:
                    z[i, j] = 0
        if color2 is None:
            color2 = color
        _tempfig = go.Figure(data=[
            go.Surface(x=x, y=y, z=z, colorscale=[color, color2], name=name, surfacecolor=np.sqrt(np.abs(z)))])
        _tempfig.update_traces(showscale=False, showlegend=showlegend)
        self.fig.add_traces(_tempfig.data)




    def show(self):
        self.fig.show()

    def export_html(self, path, include_plotlyjs=True, include_mathjax=False):
        if include_mathjax:
            include_mathjax = 'cdn'
        self.fig.write_html(path, include_plotlyjs=include_plotlyjs, include_mathjax=include_mathjax)


    #TODO: Do something with default camera
    def export_pdf(self, path, eye=(1.25, 1.25, 1.25), up=(.0, .0, 1.0), orbit=False, title=True):
        """
        This requires Kaleido, install using "pip install -U Kaleido".
        :param path: Path of resulting file
        :param eye: Eye of camera
        :return:
        """
        camera = dict(
            eye=dict(x=eye[0], y=eye[1], z=eye[2]),
            up=dict(x=up[0], y=up[1], z=up[2])
        )
        if orbit:
            self.fig.update_layout(scene = dict(dragmode='orbit'))

        self.fig.update_layout(scene_camera=camera, showlegend=False)
        write_image(self.fig, path, format="pdf", scale=3, engine="kaleido", width=1024, height=1024)
        self.fig.update_layout(scene_camera=dict(eye=dict(x=1.25, y=1.25, z=1.25), up=dict(x=.0,y=.0,z=1.0)), showlegend=True, scene=dict(dragmode='turntable'))