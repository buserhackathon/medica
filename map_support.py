import plotly
import plotly.express as px
import json
import numpy as np
import dbquery

mapbox_access_token = 'pk.eyJ1IjoiYXNzaXNtYXVybyIsImEiOiJja3RvcGt2eTgwZXc5Mm9taGd6MTltZ2o2In0.FJ2GqIssNuJxeYh0ewTpLw'


def geoWhere(municipio_id: int = None) -> str:
        return f"where municipio_id = {municipio_id}"


def getUFs() -> dict:
    #TODO: adicionar DISTINCT
    return dbquery.getDictResultset("select state, state from municipio order by state")


def getMunicipios(uf: str) -> dict:
    # TODO: substituir concat por ||
    return dbquery.getDictResultset(f"""
select concat('i',cast(id as varchar)) as id, name from municipio
where state = '{uf}'
order by capital desc, name""")


def getUBSs(uf, municipio_id):
    # Se o município não corresponde à UF obtém a cidade correta, a capital
    uf_municipio_id = dbquery.getValueFromDb(f"select state from municipio where id = {municipio_id}")
    if uf_municipio_id != uf:
        municipio_id = dbquery.getValueFromDb(f"select id from municipio where state = '{uf}' and capital = 1")
    # ...
    where = geoWhere(municipio_id)
    df = dbquery.getDataframeResultSet(
        f"select  id, nom_estab || '<br>' || dsc_endereco || '<br>' || dsc_bairro as endereco "
        f"from ubs {where}")

    gjson = dbquery.getJSONResultset(
        f"select json_build_object('type', 'FeatureCollection','features', json_agg(ST_AsGeoJSON(t.*)::json)) "
        f"from (select id, "
        f"st_buffer(geom,0.0003) as geometry "
        f"from ubs {where}) "
        f"as t(id, geometry)")
    #
    # df_mun = dbquery.getDataframeResultSet(f"select  id, name as nom_estab "
    #                                    f"from municipio where state = 'AC' limit 1")
    #
    # gjson_mun = dbquery.getJSONResultset(
    #     f"select json_build_object('type', 'FeatureCollection','features', json_agg(ST_AsGeoJSON(t.*)::json)) "
    #     f"from (select id, name as nom_estab, geom as geometry from municipio where state = 'AC' limit 1) "
    #     "as t(id, nom_estab, geometry)")

    centroid_extent = dbquery.executeSQL(
        f"""select st_x(m.centroide_area_urbana) as long,st_y(m.centroide_area_urbana) as lat, 
       st_extent(m.geom) 
from municipio m
where id = {municipio_id}
group by m.centroide_area_urbana
""")[0]

    extent = centroid_extent[2]
    if extent is not None:
        values = extent.replace(',', ' ').replace('(', ' ').replace(')', ' ').split(' ')
        max_bound = max(abs(float(values[1]) - float(values[3])),
                        abs(float(values[2]) - float(values[4]))) * 111  # km/degree
        zoom = 19.5 - np.log(max_bound)
    else:
        zoom = 13.5

    return df, gjson, {"lat": centroid_extent[1], "lon": centroid_extent[0]}, zoom


def getFigUBSs(uf, municipio_id) -> str:
    ubss, geo, centroid, zoom = getUBSs(uf, int(municipio_id.replace('i', '')))
    fig = px.choropleth_mapbox(ubss, geojson=geo, color=ubss.id,
                               locations=ubss.id, featureidkey="properties.id",
                               center=centroid,
                               hover_name=ubss.endereco, hover_data={'id': False},
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
