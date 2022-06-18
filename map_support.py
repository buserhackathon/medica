import plotly
import plotly.express as px
import json
import numpy as np
import dbquery


def geoWhere(uf: str, municipio_id: int = None) -> str:
    if municipio_id == '0':
        return f"where uf = '{uf}'"
    else:
        return f"where municipio_id = {municipio_id}"


def getUFs() -> dict:
    return dbquery.getDictResultset("select state, state from municipio order by state")


def getMunicipios(uf: str) -> dict:
    return dbquery.getDictResultset(f"""select * from (
select '0' as id, '(Todos)' as name union
select id, name from municipio
where state = '{uf}'
) a
order by ascii(name), name""")


def getUBSs(uf, municipio_id):
    where = geoWhere(uf, municipio_id)
    df = dbquery.getDataframeResultSet(f"select  id, nom_estab "
                                       f"from ubs {where}")
    gjson = dbquery.getJSONResultset(
        f"select json_build_object('type', 'FeatureCollection','features', json_agg(ST_AsGeoJSON(t.*)::json)) "
        f"from (select id, nom_estab, geom from ubs {where}) "
        "as t(id, nom_estab, geometry)")

    centroid_extent = dbquery.executeSQL(
        f"""select st_x(st_centroid(buffer)) as long,st_y(st_centroid(buffer)) as lat, 
       st_extent(buffer) 
from 
        (select st_buffer(ST_MakePolygon(ST_MakeLine(
 array[st_point(min(st_x(geom)), min(st_y(geom))),
       st_point(max(st_x(geom)), min(st_y(geom))),
       st_point(max(st_x(geom)), max(st_y(geom))),
       st_point(min(st_x(geom)), max(st_y(geom))),
       st_point(min(st_x(geom)), min(st_y(geom)))
       ])), 0.06) as buffer     
           from ubs
           {where}) a
group by buffer
""").first()

    extent = centroid_extent[2]
    if extent[0] is not None:
        values = extent[0].replace(',', ' ').replace('(', ' ').replace(')', ' ').split(' ')
        max_bound = max(abs(float(values[1]) - float(values[3])),
                        abs(float(values[2]) - float(values[4]))) * 111  # km/degree
        zoom = 13.5 - np.log(max_bound)
    else:
        zoom = 13.5

    return df, gjson, {"lat": centroid_extent[1], "lon": centroid_extent[0]}, zoom

def getFigUBSs(uf, municipio_id) -> str:
    area, geo, centroid, zoom = getUBSs(uf, municipio_id)
    fig = px.choropleth_mapbox(area, geojson=geo, color=area.id,
                               locations=area.id, featureidkey="properties.id",
                               center=centroid,
                               hover_name=area.name, hover_data={'id': False},
                               mapbox_style="carto-positron", zoom=zoom)
    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "Institut Cartogràfic i Geològic de Catalunya",
                "source": [
                    f"https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png"
                ]
            }
        ])
    fig.update_layout(coloraxis_showscale=False)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
