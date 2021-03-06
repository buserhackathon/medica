-- public."BR_Localidades_2010_v1" definition

-- Drop table

-- DROP TABLE public."BR_Localidades_2010_v1";

CREATE TABLE public."BR_Localidades_2010_v1" (
	id serial4 NOT NULL,
	geom public.geometry(point, 4674) NULL,
	cd_geocodi varchar(20) NULL,
	tipo varchar(10) NULL,
	cd_geocodb varchar(20) NULL,
	nm_bairro varchar(60) NULL,
	cd_geocods varchar(20) NULL,
	nm_subdist varchar(60) NULL,
	cd_geocodd varchar(20) NULL,
	nm_distrit varchar(60) NULL,
	cd_geocodm varchar(20) NULL,
	nm_municip varchar(60) NULL,
	nm_micro varchar(100) NULL,
	nm_meso varchar(100) NULL,
	nm_uf varchar(60) NULL,
	cd_nivel varchar(1) NULL,
	cd_categor varchar(5) NULL,
	nm_categor varchar(50) NULL,
	nm_localid varchar(60) NULL,
	long numeric NULL,
	lat numeric NULL,
	alt numeric NULL,
	gmrotation numeric NULL,
	CONSTRAINT "BR_Localidades_2010_v1_pkey" PRIMARY KEY (id)
);
CREATE INDEX "sidx_BR_Localidades_2010_v1_geom" ON public."BR_Localidades_2010_v1" USING gist (geom);


-- public.adp_deficiencia_fisica_idoso definition

-- Drop table

-- DROP TABLE public.adp_deficiencia_fisica_idoso;

CREATE TABLE public.adp_deficiencia_fisica_idoso (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	descricao varchar NOT NULL,
	ranking varchar NULL
);


-- public.capitais_csv definition

-- Drop table

-- DROP TABLE public.capitais_csv;

CREATE TABLE public.capitais_csv (
	capital varchar(50) NULL,
	uf varchar(50) NULL
);


-- public.equipamento definition

-- Drop table

-- DROP TABLE public.equipamento;

CREATE TABLE public.equipamento (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	descricao varchar NOT NULL,
	ranking varchar NULL
);


-- public.estrutura_fisica_ambiencia definition

-- Drop table

-- DROP TABLE public.estrutura_fisica_ambiencia;

CREATE TABLE public.estrutura_fisica_ambiencia (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	descricao varchar NOT NULL,
	ranking varchar NULL
);


-- public.medicamento definition

-- Drop table

-- DROP TABLE public.medicamento;

CREATE TABLE public.medicamento (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	descricao varchar NOT NULL,
	ranking varchar NULL
);


-- public.municipio definition

-- Drop table

-- DROP TABLE public.municipio;

CREATE TABLE public.municipio (
	id int8 NOT NULL,
	geom public.geometry(multipolygon, 4326) NULL,
	"_uid_" numeric NULL,
	geocod varchar(254) NULL,
	"name" varchar(60) NULL,
	state varchar(2) NULL,
	capital int4 NULL DEFAULT 0,
	centroide_area_urbana public.geometry(point, 4326) NULL,
	CONSTRAINT municipio_corr_pkey PRIMARY KEY (id)
);
CREATE INDEX sidx_municipio_corr_geom ON public.municipio USING gist (geom);


-- public.ubs definition

-- Drop table

-- DROP TABLE public.ubs;

CREATE TABLE public.ubs (
	vlr_latitude float4 NULL,
	vlr_longitude float4 NULL,
	cod_munic int4 NULL,
	cod_cnes int4 NULL,
	nom_estab varchar NULL,
	dsc_endereco varchar NULL,
	dsc_bairro varchar NULL,
	dsc_cidade varchar NULL,
	dsc_telefone varchar NULL,
	estr_fis_id int4 NULL,
	adp_def_idoso_id int4 NULL,
	equipamento_id int4 NULL,
	medicamento_id int4 NULL,
	geom public.geometry(point, 4326) NULL,
	municipio_id int4 NULL,
	id int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,
	uf varchar(2) NULL,
	CONSTRAINT ubs_pk PRIMARY KEY (id)
);


-- public.ubs_csv definition

-- Drop table

-- DROP TABLE public.ubs_csv;

CREATE TABLE public.ubs_csv (
	vlr_latitude float4 NULL,
	vlr_longitude float4 NULL,
	cod_munic int4 NULL,
	cod_cnes int4 NULL,
	nom_estab varchar NULL,
	dsc_endereco varchar NULL,
	dsc_bairro varchar NULL,
	dsc_cidade varchar NULL,
	dsc_telefone varchar NULL,
	dsc_estrut_fisic_ambiencia varchar NULL,
	dsc_adap_defic_fisic_idosos varchar NULL,
	dsc_equipamentos varchar NULL,
	dsc_medicamentos varchar NULL,
	estr_fis_id int4 NULL,
	adp_def_idosos_id int4 NULL,
	equipamentos_id int4 NULL,
	medicamentos_id int4 NULL
);