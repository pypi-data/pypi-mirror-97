# Copyright 2020 Cognite AS
import sys
import warnings

import numpy as np

plot_width = 450
plot_height = 450


def geom_to_arr(geom):
    try:
        xy = getattr(geom, "xy", None)
    except NotImplementedError:
        xy = None

    if xy is not None:
        return np.column_stack(xy)
    if hasattr(geom, "array_interface"):
        data = geom.array_interface()
        return np.array(data["data"]).reshape(data["shape"])[:, :2]
    arr = geom.array_interface_base["data"]

    if (len(arr) % 2) != 0:
        arr = arr[:-1]
    return np.array(arr).reshape(-1, 2)


def geom_to_array(geom):
    if geom.geom_type == "Point":
        return np.array([[geom.x, geom.y]])
    if hasattr(geom, "exterior"):
        if geom.exterior is None:
            xs, ys = np.array([]), np.array([])
        else:
            xs = np.array(geom.exterior.coords.xy[0])
            ys = np.array(geom.exterior.coords.xy[1])
    elif geom.geom_type in ("LineString", "LinearRing"):
        return geom_to_arr(geom)
    elif geom.geom_type == "MultiPoint":
        arrays = []
        for g in geom:
            if g.geom_type == "Point":
                arrays.append(np.array(g.xy).T)
        return np.concatenate(arrays) if arrays else np.array([])
    else:
        arrays = []
        for g in geom:
            arrays.append(geom_to_arr(g))
            arrays.append(np.array([[np.nan, np.nan]]))
        return np.concatenate(arrays[:-1]) if arrays else np.array([])
    return np.column_stack([xs, ys])


def holo_plot_geometry(geom, label=""):
    if "holoviews" in sys.modules:
        import holoviews as hv

        if geom.geom_type == "Point":
            return hv.Points([[geom.x, geom.y]], label=label)
        elif geom.geom_type == "MultiPoint":
            return hv.Points(geom_to_array(geom), label=label)
        elif geom.geom_type in ("LineString", "LinearRing"):
            coordinate = geom_to_array(geom)
            return hv.Path({"x": coordinate[:, 0], "y": coordinate[:, 1]}, ["x", "y"], label=label)
        elif geom.geom_type == "Polygon":
            coordinate = geom_to_array(geom)
            return hv.Polygons([{("x", "y"): coordinate}])
        elif geom.geom_type == "MultiPolygon":
            return hv.Polygons([{("x", "y"): geom_to_array(g)} for g in geom], label=label)
        else:
            plots = None
            for g in geom:
                if plots is None:
                    plots = holo_plot_geometry(g)
                else:
                    plots = plots * holo_plot_geometry(g)
            return plots
    warnings.warn("holoviews not found")
    return None


def plot_geometry(geometry, label="", title="", xlabel="x", ylabel="y"):
    if geometry is not None:
        geometry_plot = holo_plot_geometry(geometry, label=label)
        if geometry_plot is not None:
            geometry_plot.opts(
                padding=0.1,
                width=plot_width,
                height=plot_height,
                axiswise=True,
                show_grid=True,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
            )
        return geometry_plot

    return None


def get_color_map():
    if "matplotlib" in sys.modules:
        from matplotlib import colors as colors

        # Define colormap
        mn = 0
        mx = 5
        s0 = 0.0 / (mx - mn)
        s1 = 1.0 / (mx - mn)
        s2 = 2.0 / (mx - mn)
        s3 = 3.0 / (mx - mn)
        s4 = 4.0 / (mx - mn)
        s5 = 5.0 / (mx - mn)

        cdict = {
            "red": ((s0, 0.0, 0.0), (s1, 1.0, 1.0), (s2, 1.0, 1.0), (s3, 1.0, 1.0), (s4, 0.5, 0.5), (s5, 0.2, 0.2)),
            "green": ((s0, 1.0, 1.0), (s1, 1.0, 1.0), (s2, 0.5, 0.5), (s3, 0.0, 0.0), (s4, 0.0, 0.0), (s5, 0.0, 0.0)),
            "blue": ((s0, 0.0, 0.0), (s1, 0.0, 0.0), (s2, 0.0, 0.0), (s3, 0.0, 0.0), (s4, 0.0, 0.0), (s5, 0.0, 0.0)),
        }

        chi2cmap = colors.LinearSegmentedColormap("chi2_colormap", cdict, 1024)
        chi2cmap.set_bad("w", 1.0)
        return chi2cmap

    warnings.warn("matplotlib not found")
    return None


def plot_grid_point(points_array, label="", title="", xlabel="x", ylabel="y"):
    if "holoviews" in sys.modules and "datashader" in sys.modules:
        import datashader as ds
        import holoviews as hv
        from holoviews.operation.datashader import datashade, rasterize

        if points_array.shape[1] == 2:
            plot_array_orig = hv.Points(points_array, label=label)
            dash_geometry = datashade(plot_array_orig)
            dash_geometry.opts(
                padding=0.1,
                width=plot_width,
                height=plot_height,
                axiswise=True,
                show_grid=True,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
            )
            return dash_geometry
        else:
            chi2cmap = get_color_map()
            plot_array_orig = hv.Points(points_array, vdims=["z"], label=label)
            rast = rasterize.instance(aggregator=ds.min("z"), cmap=chi2cmap, normalization="linear")
            rast_plot = rast(plot_array_orig)
            rast_plot.opts(
                padding=0.1,
                width=plot_width,
                height=plot_height,
                colorbar=True,
                axiswise=True,
                show_grid=True,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
            )
            return rast_plot
    warnings.warn("either holoviews or datashader not found")
    return None
