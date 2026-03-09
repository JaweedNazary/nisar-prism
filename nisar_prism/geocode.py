import numpy as np
import warnings
import h5py
from scipy.interpolate import RegularGridInterpolator
from scipy.spatial import cKDTree
from pyproj import Transformer


GEO_GRP = "science/LSAR/RSLC/metadata/geolocationGrid"


def _nearest_index_1d(sorted_vec, value):
    vec = np.asarray(sorted_vec)

    i = np.searchsorted(vec, value)

    if i <= 0:
        return 0
    if i >= vec.size:
        return vec.size - 1

    if abs(value - vec[i-1]) <= abs(vec[i] - value):
        return i-1

    return i


def find_az0_rg0_from_latlon(
    h5_path,
    rslc_path,
    lat,
    lon,
    layer=0,
    newton_iters=8,
    tol_xy=0.5,
):
    """
    Convert geographic coordinates (lat, lon) to RSLC pixel indices.

    Returns
    -------
    az0 : int
        Azimuth index
    rg0 : int
        Range index
    info : dict
        Diagnostic information
    """

    with h5py.File(h5_path, "r") as h5:

        dset = h5[rslc_path]
        H_full, W_full = dset.shape

        freq = rslc_path.split("/")[-2]

        t_full = np.asarray(
            h5["science/LSAR/RSLC/swaths/zeroDopplerTime"]
        )

        r_full = np.asarray(
            h5[f"science/LSAR/RSLC/swaths/{freq}/slantRange"]
        )

        epsg = int(h5[f"{GEO_GRP}/epsg"][()])

        t_geo = np.asarray(h5[f"{GEO_GRP}/zeroDopplerTime"])
        r_geo = np.asarray(h5[f"{GEO_GRP}/slantRange"])

        Xg = np.asarray(h5[f"{GEO_GRP}/coordinateX"])[layer]
        Yg = np.asarray(h5[f"{GEO_GRP}/coordinateY"])[layer]

    transformer = Transformer.from_crs(
        "EPSG:4326",
        f"EPSG:{epsg}",
        always_xy=True,
    )

    x0, y0 = transformer.transform(lon, lat)

    # Check if requested location is outside geolocation grid bounds
    xmin, xmax = np.nanmin(Xg), np.nanmax(Xg)
    ymin, ymax = np.nanmin(Yg), np.nanmax(Yg)

    if not (xmin <= x0 <= xmax and ymin <= y0 <= ymax):
        warnings.warn(
            "Requested lat/lon is outside the RSLC geolocation grid boundary. "
            "The returned pixel will be the closest available location.",
            RuntimeWarning,
        )
        

    X_i = RegularGridInterpolator(
        (t_geo, r_geo),
        Xg,
        bounds_error=False,
        fill_value=np.nan,
    )

    Y_i = RegularGridInterpolator(
        (t_geo, r_geo),
        Yg,
        bounds_error=False,
        fill_value=np.nan,
    )

    mask = np.isfinite(Xg) & np.isfinite(Yg)

    ij = np.argwhere(mask)

    xy = np.column_stack([Xg[mask], Yg[mask]])

    tree = cKDTree(xy)

    _, k = tree.query([x0, y0], k=1)

    it0, ir0 = ij[k]

    t = float(t_geo[it0])
    r = float(r_geo[ir0])

    def f(tr):

        tt, rr = tr

        Xp = float(X_i((tt, rr)))
        Yp = float(Y_i((tt, rr)))

        return np.array([Xp-x0, Yp-y0])

    dt = np.median(np.diff(t_geo))
    dr = np.median(np.diff(r_geo))

    for _ in range(newton_iters):

        e = f((t, r))

        if np.hypot(e[0], e[1]) < tol_xy:
            break

        dEdt = (f((t+dt, r)) - f((t-dt, r))) / (2*dt)
        dEdr = (f((t, r+dr)) - f((t, r-dr))) / (2*dr)

        J = np.column_stack([dEdt, dEdr])

        try:
            delta = np.linalg.solve(J, -e)
        except np.linalg.LinAlgError:
            break

        t += delta[0]
        r += delta[1]

    az0 = _nearest_index_1d(t_full, t)
    rg0 = _nearest_index_1d(r_full, r)

    return az0, rg0, {
        "t": t,
        "r": r,
        "x": x0,
        "y": y0,
        "epsg": epsg,
    }
