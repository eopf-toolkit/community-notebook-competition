import folium

from IPython import get_ipython
from IPython.display import Javascript, display, Image

def collapse_outputs(*_args: any, **_kwargs: any) -> None:
    """
    Collapse outputs of all code cells in the current JupyterLab notebook.

    This helper is registered as a post-run hook so that, after each cell
    execution, all code cell outputs are collapsed. It helps keep long
    notebooks compact and easier to navigate.
    """

    display(
        Javascript(
            """
            document
              .querySelectorAll('.jp-CodeCell')
              .forEach(cell => {
                const btn = cell.querySelector('.jp-OutputCollapser');
                if (btn) { btn.click(); }
              });
            """
        )
    )


    ipython = get_ipython()
    if ipython is not None:
        ipython.events.register("post_run_cell", collapse_outputs)

import geopandas as gpd
from shapely.validation import make_valid


def fix_invalid_geometries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Fix invalid geometries in a GeoDataFrame using ``shapely.make_valid``.

    Checks the validity of each geometry in the input
    GeoDataFrame and applies ``make_valid``
    It returns a copy of the GeoDataFrame with corrected geometries.

    Args:
    gdf : geopandas.GeoDataFrame
        GeoDataFrame whose geometry column may contain invalid geometries.

    Returns:
    geopandas.GeoDataFrame
        A new GeoDataFrame where invalid geometries have been repaired.
    """
    gdf_fixed = gdf.copy()

    invalid_mask = ~gdf_fixed.geometry.is_valid

    if invalid_mask.any():
        gdf_fixed.loc[invalid_mask, "geometry"] = (
            gdf_fixed.loc[invalid_mask, "geometry"].apply(make_valid)
        )

    return gdf_fixed

import geopandas as gpd
import folium 

def reset_panthera_onca_map(
    panthera_onca_gdf_simple: gpd.GeoDataFrame,
    opacity: float = 0.6,
    explore_kwargs: dict | None = None,
) -> folium.Map:
    """
    Create a fresh interactive map of the Panthera onca habitat.

    Args:
        panthera_onca_gdf_simple: gpd.GeoDataFrame
            Simplified habitat GeoDataFrame
        opacity: float, default 0.6
            Habitat layer opacity
        explore_kwargs: dict, optional
            Additional kwargs passed directly to gpd.explore()

    Returns:
        folium.Map with panthera onca geometry
    """
    default_kwargs = {
        "color": "orange",
        "tooltip": False,
        "legend": True,
        "style_kwds": {
            "fillOpacity": opacity,
            "opacity": opacity,
        },
    }

    if explore_kwargs:
        explore_kwargs["style_kwds"] = explore_kwargs.get("style_kwds", {})
        explore_kwargs["style_kwds"].update({
            "fillOpacity": opacity,
            "opacity": opacity,
        })
        default_kwargs.update(explore_kwargs)

    return panthera_onca_gdf_simple.explore(**default_kwargs)

import xarray as xr
from rich.console import Console
from rich.tree import Tree

console = Console()

def emoji_legend_tree():
    legend = Tree("📖 Emoji Legend")
    legend.add("📂 Root / Container")
    legend.add("🟩 Group[ (Internal Zarr hierarchy)")
    legend.add("🟦 DataArray (The actual pixel data)")
    legend.add("🟧 Metadata (Attributes/STAC tags)")
    console.print(legend)


def rich_dtree_recursive(
    node: xr.DataTree, 
    name: str = "root", 
    highlight_paths: list[str] | None = None, 
    parent_path: str = "", 
    highlight_emoji: str = "⭐"):
    """
    Recursively build a Rich Tree of a hierarchical dataset.

    Args:
        node: The current node object with `children`, `ds.data_vars`, and `attrs`.
        name: Name of the current node.
        highlight_paths: List of full paths to highlight.
        parent_path: Path of the parent node.
        highlight_emoji: Emoji to indicate highlighted nodes.

    Returns:
        rich.tree.Tree object representing this node and its children.
    """
    if highlight_paths is None:
        highlight_paths = []

    full_path = f"{parent_path}/{name}" if parent_path else name

    base_emoji = "📂" if parent_path == "" else "🟩"

    is_highlighted = any(p.startswith(full_path) for p in highlight_paths)
    is_root = parent_path == ""

    emoji = f"{base_emoji}{highlight_emoji}" if is_highlighted else base_emoji

    label = f"{emoji} {name} (groups: {len(node.children)}, variables: {len(node.ds.data_vars)}, attrs: {len(node.attrs)})"
    tree = Tree(label)

    if is_root or is_highlighted:
        for metadata in node.attrs:
            tree.add(f"🟧 {metadata}")
        for array in node.ds.data_vars:
            tree.add(f"🟦 {array}")

    highlighted_children = {}
    normal_children = {}
    for child_name, child_node in node.children.items():
        child_full_path = f"{full_path}/{child_name}"
        if any(p.startswith(child_full_path) for p in highlight_paths):
            highlighted_children[child_name] = child_node
        else:
            normal_children[child_name] = child_node

    for child_name, child_node in highlighted_children.items():
        tree.add(
            rich_dtree_recursive(
                child_node,
                child_name,
                highlight_paths,
                parent_path=full_path,
                highlight_emoji=highlight_emoji
            )
        )

    for child_name, child_node in normal_children.items():
        child_label = f"🟩 {child_name} (groups: {len(child_node.children)}, variables: {len(child_node.ds.data_vars)}, attrs: {len(child_node.attrs)})"
        tree.add(Tree(child_label))

    return tree

import pandas as pd

CHUNKS_FOR_10_KM = {"x": 1098, "y": 1098}

DEFAULT_OPEN_KWARGS_DTREE_DICT = {
    "chunks": CHUNKS_FOR_10_KM, 
    "op_mode": "native",
    "chunks": "auto", 
}

def _build_open_kwargs_dtree_dict(item: pd.Series):
    open_kwargs = item["xarray:open_datatree_kwargs"]
    open_kwargs_dict = ast.literal_eval(open_kwargs_str) if isinstance(open_kwargs, str) else open_kwargs
    return {**DEFAULT_OPEN_KWARGS_DTREE_DICT, **open_kwargs_dict}
