from typing import Union, List, Optional, Dict

import pandas as pd
from datetime import datetime
from deprecated import deprecated
from requests.exceptions import HTTPError
from snowflake import connector as snowflake
from snowflake.connector import SnowflakeConnection
from snowflake.connector.pandas_tools import write_pandas
import yaml

from pyrasgo.connection import Connection
from pyrasgo.enums import Granularity, ModelType
from pyrasgo.feature import Feature, FeatureList
from pyrasgo.model import Model
from pyrasgo.member import Member
from pyrasgo.monitoring import track_usage
from pyrasgo import schemas as api


class RasgoConnection(Connection):
    """
    Base connection object to handle interactions with the Rasgo API.

    Defaults to using the production Rasgo instance, which can be overwritten
    by specifying the `RASGO_DOMAIN` environment variable, eg:

    &> RASGO_DOMAIN=custom.rasgoml.com python
    >>> from pyrasgo import RasgoConnection
    >>> rasgo = Connection(api_key='not_a_key')
    >>> rasgo._hostname == 'custom.rasgoml.com'
    True

    """
    from pyrasgo.version import __version__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @track_usage
    def create_model(self, name: str,
                     type: Union[str, ModelType],
                     granularity: Union[str, Granularity]) -> Model:
        """
        Creates model within Rasgo within the account specified by the API key.
        :param name: Model name
        :param model_type: Type of model specified
        :param granularity: Granularity of the data.
        :return: Model object.
        """
        try:
            # If not enum, convert to enum first.
            model_type = type.name
        except AttributeError:
            model_type = ModelType(type)

        try:
            # If not enum, convert to enum first.
            granularity = granularity.name
        except AttributeError:
            granularity = Granularity(granularity)

        # TODO: API should really have _some_ validation for the schema of this post.
        response = self._post("/models", _json={"name": name,
                                                "type": model_type.value,
                                                # TODO: This post should only be `granularity` for future compatibility
                                                #       Coordinate with API development to relax domain specificity
                                                "timeSeriesGranularity": granularity.value})
        return Model(api_object=response.json())

    @track_usage
    def add_feature_to(self, model: Model, feature: Feature):
        model.add_feature(feature)

    @track_usage
    def add_features_to(self, model: Model, features: FeatureList):
        model.add_features(features)

    @track_usage
    def generate_training_data_for(self, model: Model):
        raise NotImplementedError

    @track_usage
    def get_models(self) -> List[Model]:
        """
        Retrieves the list of models from Rasgo within the account specified by the API key.
        """
        response = self._get("/models", {"join": ["features", "author"],
                                         "filter": "isDeleted||$isnull"})
        return [Model(api_object=entry) for entry in response.json()]

    @track_usage
    def get_model(self, model_id) -> Model:
        """
        Retrieves the specified model from Rasgo within the account specified by the API key.
        """
        # TODO: The API should not throw a 500 if it can't find a non-existent model, it should return a 404
        try:
            self._get(f"/models/{model_id}")
        except HTTPError:
            # This assumes they've followed a work flow and had their API key verified (happens on class __init__).
            raise LookupError(f"The model (id={model_id}) could not be found in your Rasgo account.")
        # TODO: The API should not throw a 500 if it can't join against a non-existent model, it should return a 404.
        response = self._get(f"/models/{model_id}", {"join": ["features", "author"]})
        return Model(api_object=response.json())

    @track_usage
    def get_feature(self, feature_id) -> Feature:
        """
        Retrieves the specified feature from Rasgo within the account specified by the API key.
        """
        response = self._get(f"/features/{feature_id}", api_version=1)
        return Feature(api_object=response.json())

    @track_usage
    def get_features(self) -> FeatureList:
        """
        Retrieves the features from Rasgo within account specified by the API key.
        """
        return FeatureList(api_object=self._get("/features", api_version=1).json())

    @track_usage
    def get_features_for(self, model: Model) -> FeatureList:
        raise NotImplementedError()
        # response = self._get("/features",
        #                      params={'join': f""})
        #                    # params={'filter': f"||eq||DateTime"})
        # return FeatureList(response.json())

    @track_usage
    def get_feature_data(self, model_id: int,
                         filters: Optional[Dict[str, str]] = None,
                         limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs the pandas dataframe for the specified model.

        :param model_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        model = self.get_model(model_id)

        conn, creds = self._snowflake_connection(model.get_author())

        table_metadata = model.snowflake_table_metadata(creds)
        query, values = self._make_select_statement(table_metadata, filters, limit)

        result_set = self._run_query(conn, query, values)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_feature_sets(self):
        """
        Retrieves the feature sets from Rasgo within account specified by the API key.
        """
        return self._get("/feature-sets").json()

    @track_usage
    def get_source_tables(self):
        '''
        Retrieves a list of Snowflake tables and views that are queryable as feature sources
        '''
        conn, creds = self._snowflake_connection(self.get_member())
        query = 'SELECT * FROM RASGO_DATA_SOURCE_TABLES'
        result_set = self._run_query(conn, query, None)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_table(self, table_name: str, record_limit: int):
        '''
        Returns top n records from a Snowflake source table to a dataframe
        '''
        conn, creds = self._snowflake_connection(self.get_member())
        if record_limit == -1:
            query = f'SELECT * FROM {table_name}'
        else:
            query = f'SELECT * FROM {table_name} limit {record_limit}'
        result_set = self._run_query(conn, query, None)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_columns(self):
        '''
        Retrieves a list of columns in Snowflake tables and views that are queryable as feature sources
        '''
        conn, creds = self._snowflake_connection(self.get_member())
        query = 'SELECT * FROM RASGO_DATA_SOURCE_COLUMNS'
        result_set = self._run_query(conn, query, None)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_data_sources(self):
        """
        Retrieves the data sources from Rasgo within account specified by the API key.
        """
        return self._get("/data-source").json()

    @track_usage
    def get_dimensionalities(self):
        """
        Retrieves the data sources from Rasgo within account specified by the API key.
        """
        return self._get("/dimensionalities").json()

    @track_usage
    def get_datasource(self, name):
        rows = self.find("data-source", {"name": name})
        if 0 == len(rows):
            return None
        else:
            return rows[0]

    def get_member(self):
        return Member(self.get_user())

    def get_user(self):
        return self._get("/users/me", api_version=1).json()

    @track_usage
    def get_user_id(self):
        """
        Gets the user id for the API key provided, or None if not available.
        NOTE: This is used for monitoring/logging purposes.
        """
        if self._user_id:
            return self._user_id
        else:
            try:
                user = self.get_user()
                self._user_id = user.get('id')
                return self._user_id
            except Exception:
                return None

    @track_usage
    def get_dimensionality(self, name):
        return self._get_item("dimensionalities", {"name": name}, True)

    @track_usage
    def create_column(self, name, data_type, feature_set_id, dimension_id):
        column = api.ColumnCreate(name=name, dataType=data_type,
                                  featureSet=api.FeatureSetBase(id=feature_set_id),
                                  dimensionality=api.Dimensionality(id=dimension_id))
        return self._post("/rcolumns", column.dict(exclude_unset=True)).json()

    @track_usage
    def update_column(self, column_id, name, data_type, feature_set_id, dimension_id):
        column = api.ColumnUpdate(id=column_id, 
                                  name=name, dataType=data_type,
                                  featureSet=api.FeatureSetBase(id=feature_set_id),
                                  dimensionality=api.Dimensionality(id=dimension_id))
        return self._patch(f"rcolumns/{column_id}", column.dict(exclude_unset=True)).json()

    @track_usage
    def create_datasource(self, org_id, name):
        data_source = api.DataSourceCreate(name=name,
                                           abbreviation=name[:10].lower(),
                                           organization=api.Organization(id=org_id))
        return self._post("/data-source", data_source.dict(exclude_unset=True)).json()

    @track_usage
    def create_dimensionality(self, org_id, name, dimension_type, granularity):
        dimensionality = api.DimensionalityCreate(name=name,
                                                  dimension_type=dimension_type,
                                                  granularity=granularity,
                                                  organization=api.Organization(id=org_id))
        return self._post("/dimensionalities", dimensionality.dict(exclude_unset=True)).json()

    @track_usage
    def create_feature(self, org_id: int, featureset_id: int, name: str, code: str, description: str, column_id: int, status: str, tags: List[str]):
        feature = api.FeatureCreate(name=name,
                                    code=code,
                                    description=description,
                                    featureSetId=featureset_id,
                                    columnId=column_id,
                                    organizationId=org_id,
                                    orchestrationStatus=status,
                                    tags=tags)
        return self._post("/features", feature.dict(exclude_unset=True), api_version=1).json()

    @track_usage
    def update_feature(self, feature_id: int, org_id: int, featureset_id: int, name: str, code: str, description: str, column_id: int, status: str, tags: List[str]):
        feature = api.FeatureUpdate(id=feature_id,
                                    name=name,
                                    code=code,
                                    description=description)
        #TODO: We won't be able to update these fields until we create a V1 patch features endpoint
                                    #featureSetId=featureset_id,
                                    #columnId=column_id,
                                    #organizationId=org_id,
                                    #orchestrationStatus=status,
                                    #tags=tags)
        return self._patch(f"features/{feature_id}", feature.dict()).json()

    @track_usage
    def create_feature_set(self, name, datasource_id, table_name, granularity=None):
        feature_set = api.FeatureSetCreate(name=name,
                                           snowflakeTable=table_name,
                                           dataSource=api.DataSourceBase(id=datasource_id),
                                           granularity=granularity)
        return self._post("feature-sets", feature_set.dict()).json()

    @track_usage
    def update_feature_set(self, feature_set_id, name, datasource_id, table_name, granularity=None):
        feature_set = api.FeatureSetUpdate(id=feature_set_id,
                                           name=name,
                                           snowflakeTable=table_name,
                                           dataSource=api.DataSourceBase(id=datasource_id),
                                           granularity=granularity)
        return self._patch(f"feature-sets/{feature_set_id}", feature_set.dict()).json()

    @track_usage
    def publish_feature_set(self, name, datasource_id, table_name, granularity=None):
        '''
        Creates or updates a featureset depending on existence of the defined parameters
        '''
        fs = self._get_item("feature-sets", { "snowflakeTable": table_name})
        if fs:
            feature_set = self.update_feature_set(fs['id'], name, datasource_id, table_name, granularity)
        else:
            feature_set = self.create_feature_set(name, datasource_id, table_name, granularity)
        return feature_set

    def dimensionality_name(self, datatype, granularity):
        return "{} - {}".format(datatype, str(granularity).title())

    @track_usage
    def publish_dimensionality(self, org_id, dimension_type, granularity):
        """
        Creates or returns a dimensionality depending on existence of the defined parameters

        Dimensionality is a named pairing of a datatype and a granularity. Note in some cases the
        granularity is actually a data type.
        """
        if dimension_type is None:
            if granularity.lower() in ['hour', 'day', 'week', 'month', 'quarter', 'year']:
                dimension_type = 'DateTime'
            else:
                dimension_type = "Custom"
        elif dimension_type.lower() == "datetime":
            dimension_type = "DateTime"
        else:
            dimension_type = dimension_type.title()
        dimensionality_name = self.dimensionality_name(dimension_type, granularity)

        # Check for a 'dimensionality' record that corresponds to the the dimensions
        # datatype and granularity.
        dimensionality = self.get_dimensionality(dimensionality_name)
        if dimensionality:
            return dimensionality
        else:
            return self.create_dimensionality(org_id, dimensionality_name, dimension_type, granularity)

    @track_usage
    def get_column(self, name, featureset_id):
        '''
        Returns a column matching a name in the specified featureset
        '''
        items = self._get_items("rcolumns", {"name": name})
        for i in items:
            if featureset_id == i['featureSet']['id']:
                return i
        return None

    @track_usage
    def match_feature(self, code, featureset_id):
        '''
        Returns a feature matching a name in the specified featureset
        '''
        items = self._get_items("features", {"code": code})
        for i in items:
            if featureset_id == i['column']['featureSet']['id']:
                return i
        return None

    @track_usage
    def publish_dimension(self, org_id, featureset_id, name, data_type, dimension_type=None, granularity=None):
        '''
        Creates or updates a dimension depending on existence of the defined parameters
        '''
        dimemnsionality = self.publish_dimensionality(org_id, dimension_type, granularity)
        dimemnsionality_id = dimemnsionality['id']
        dim = self.get_column(name, featureset_id)
        if dim:
            dimension = self.update_column(dim['id'], name, data_type, featureset_id, dimemnsionality_id)
        else:
            dimension = self.create_column(name, data_type, featureset_id, dimemnsionality_id)
        return dimension

    @track_usage
    def publish_feature(self, org_id, featureset_id, name, data_type, code=None, description=None, granularity=None, status=None, tags=None):
        '''
        Creates or updates a feature depending on existence of the defined parameters
        '''
        if code is None:
            code = name
        if description is None:
            description = f"Feature that contains {name} data"
        if status is None:
            status = 'Sandboxed'  
        if granularity is None:
            dimension_id = None
        else:
            dimemnsionality = self.publish_dimensionality(org_id, None, granularity)
            dimension_id = dimemnsionality['id']
        
        ft = self.match_feature(code, featureset_id)
        if ft:
            column = self.update_column(ft['column']['id'], code, data_type, featureset_id, dimension_id)
            feature = self.update_feature(ft['id'], org_id, featureset_id, name, code, description, ft['column']['id'], status, tags)
        else:
            column = self.create_column(code, data_type, featureset_id, dimension_id)
            feature = self.create_feature(org_id, featureset_id, name, code, description, column['id'], status, tags)
        return feature

    @track_usage
    def publish_datasource(self, org_id, ds_name):
        '''
        Creates or returns a datasource depending on of the defined parameters
        '''
        # Check for a 'dimensionality' record that corresponds to the the dimensions
        # datatype and granularity.
        ds = self.get_datasource(ds_name)
        if ds:
            return ds
        else:
            return self.create_datasource(org_id, ds_name)

    def _confirm_df_columns(self, dataframe, dimensions, features):
        df_columns = list(dataframe.columns)
        missing_dims = []
        missing_features = []
        for dim in dimensions:
            if dim not in df_columns:
                missing_dims.append(dim)
        for ft in features:
            if ft not in df_columns:
                missing_features.append(ft)
        if missing_dims or missing_features:
            raise Exception(f"Specified columns do not exist in dataframe: "
                            f"Dimensions({missing_dims}) Features({missing_features})")

    def _generate_featureset_name(self, dimensions, timestamp):
        return f"pandas_by_{'-'.join(dimensions)}_{timestamp}"

    def _snowflakify_name(self, name):
        '''
        param name: string
        return: string
        Converts a string to a snowflake compliant value
        Removes double quotes, replaces dashes with underscores, casts to upper case
        '''
        return name.replace("-", "_").replace('"', '').upper()

    def _snowflakify_list(self, list_in):
        '''
        param list_in: list
        return list_out: list
        Changes a list of columns to Snowflake compliant names
        '''
        list_out = [self._snowflakify_name(n) for n in list_in]
        return list_out

    def _snowflakify_dataframe(self, dataframe: pd.DataFrame):
        '''
        param dataframe: dataframe holding columns
        param column: list of column names that need to change
        Renames all columns in a pandas dataframe to Snowflake compliant names
        '''
        schema = self._schema_for_dataframe(dataframe)
        cols = {}
        for r in schema:
            oldc = r
            newc = self._snowflakify_name(oldc)
            cols[oldc] = newc
        dataframe.rename(columns=cols, inplace=True)

    def _dataframe_to_snowflake(self, dataframe, table_name):
        # TODO: Move this function to a lambda
        # we want to grant a user access to create tables in the schema
        # currently we're doing it in the model_training lambda
        # I can't be done in this method due to role limitations at runtime
        conn, creds = self._snowflake_connection(self.get_member())
        with conn.cursor() as cur:
            # Create the table in Snowflake
            tablesql = self._generate_ddl_from_dataframe(dataframe, table_name)
            cur.execute(tablesql)
        # load data from df to SF table
        write_pandas(conn, dataframe, table_name)

    def _generate_ddl_from_dataframe(self, df, table_name):
        sql_text = pd.io.sql.get_schema(df.reset_index(), table_name)
        sql_text = sql_text.replace('CREATE TABLE', 'CREATE OR REPLACE TABLE')
        sql_text = sql_text.replace('"', '')
        return sql_text

    def _schema_for_dataframe(self, df):
        from pandas.io.json import build_table_schema
        schema_list = build_table_schema(df)
        schema = {}
        for column in schema_list['fields']:
            name = column['name']
            schema[name] = column
        return schema

    @track_usage
    def publish_features_from_df(self, dataframe: pd.DataFrame, dimensions: List[str], features: List[str], granularity: str=None, tags: List[str]=None):
        '''
        Creates a featureset from a pandas dataframe

        :dataframe: Pandas DataFrame containing all columns that will be registered with Rasgo
        :param dimensions: List of columns in df that should be used for joins to other featursets
        :param features: List of columns in df that should be registered as features in Rasgo
        :param granularity: Datetime grain to be added to all features in the df
        :param tags: List of tags to be added to all features in the df
        :return: description of the featureset created
        '''
        # todo: Optionally generate list of feature columns from the dataframe columns, ie - all non-dimensions are features
        # todo: Add option to specify a featureset name + add check that it exists.
        #Type checking
        if type(dimensions) != list:
            raise TypeError('Dimensions must be passed in as a list')
        if type(features) != list:
            raise TypeError('Features must be passed in as a list')
        if tags:
            if type(tags) != list:
                raise TypeError('Tags must be passed in as a list')
        
        member = self.get_member()
        org_id = member.organization_id()
        now = datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H_%M")
        datasource = self.publish_datasource(org_id, 'PANDAS')
        if tags is None:
            tags = list()

        # Convert all strings to work with Snowflake
        dimensions = self._snowflakify_list(dimensions)
        features = self._snowflakify_list(features)
        self._snowflakify_dataframe(dataframe)

        # Confirm each named dimension and feature exists in the dataframe.
        self._confirm_df_columns(dataframe, dimensions, features)

        # Generate featureset name.
        featureset_name = self._generate_featureset_name(dimensions, timestamp)

        # Create a table in Snowflake with the subset of columns we're interested in, name table after featureset.
        all_columns = dimensions + features
        exportable_df = dataframe[all_columns]
        table_name = self._snowflakify_name(featureset_name)
        self._dataframe_to_snowflake(exportable_df, table_name)

        # Add a reference to the FeatureSet
        featureset_name = table_name
        featureset = self.create_feature_set(featureset_name, datasource['id'], table_name, granularity)
        schema = self._schema_for_dataframe(dataframe)

        return_featureset = {}
        return_featureset['id'] = featureset['id']
        return_featureset['name'] = featureset['name']
        return_featureset['granularity'] = featureset['granularity']
        return_featureset['dataSource'] = featureset['dataSource']['name']
        return_featureset['organization'] = featureset['dataSource']['organization']['name']
        return_featureset['snowflakeTable'] = featureset['snowflakeTable']

        # Add references to all the dimensions
        return_dimensions = {}
        for d in dimensions:
            column = schema[d]
            data_type = column['type']
            dimension_name = column['name']
            dimension = self.publish_dimension(org_id, featureset['id'], dimension_name, data_type, None, granularity)
            return_dimensions.update({dimension['id']: {"name": dimension['name']}})
        return_featureset['dimensions'] = return_dimensions

        # Add references to all the features
        return_features = {}
        for f in features:
            column = schema[f]
            data_type = column['type']
            code = column['name']
            feature_name = f"PANDAS_{code}_{timestamp}"
            status = 'Sandboxed'
            tags.append('Pandas')
            feature = self.publish_feature(org_id, featureset['id'], feature_name, data_type, code, None, granularity, status, tags)
            return_features.update({feature['id']:
                                    {"id": feature['id'],
                                    "name": feature['name'],
                                    "column": feature['code']
                                    }})
        return_featureset['features'] = return_features
        return return_featureset

    @track_usage
    def publish_features_from_yml(self, yml_file, orchestrationStatus='Sandboxed'):
        '''
        Creates a featureset from a yml file

        :param yml_file: Rasgo compliant yml file that describes the featureset(s) being created
        :param orchestrationStatus: Sandboxed or Productionized
        :return: description of the featureset created
        '''

        with open(yml_file) as fobj:
            featuresets = yaml.load(fobj, Loader = yaml.SafeLoader)
        for fs in featuresets:
            #publish featureset
            member = self.get_member()
            org_id = member.organization_id()
            datasource = self.publish_datasource(org_id, fs["datasource"])            
            featureset_name = fs.get("name", fs["table"])
            snowflake_table = fs["table"]
            if not snowflake_table:
                raise Exception("A valid table name is required")
            granularity = fs.get('granularity')
            tags = list()
            if fs.get('tags'):
                for t in fs.get('tags'):
                    tags.append(t)
            featureset = self.publish_feature_set(featureset_name, datasource['id'], snowflake_table, granularity)

            return_featureset = {}
            return_featureset['id'] = featureset['id']
            return_featureset['name'] = featureset['name']
            return_featureset['granularity'] = featureset['granularity']
            return_featureset['dataSource'] = featureset['dataSource']['name']
            return_featureset['organization'] = featureset['dataSource']['organization']['name']
            return_featureset['snowflakeTable'] = featureset['snowflakeTable']

            #publish dimensions
            return_dimensions = {}
            for dim in fs['dimensions']:
                name = dim.get('name')
                data_type = dim.get('data_type')
                #allow granularity on a dimension to override the featureset granularity
                dim_granularity = dim.get('granularity', granularity)
                d = self.publish_dimension(org_id, featureset['id'], name, data_type, None, dim_granularity)
                return_dimensions.update({d['id']: {"name": d['name']}})
            return_featureset['dimensions'] = return_dimensions

            #publish features
            return_features = {}
            for feature in fs['features']:
                name = feature['display_name']
                code = feature.get('name', name)
                data_type = feature.get('data_type')
                description = feature.get('description', f"Feature that contains {name} data")
                #apply featureset tags to all features...
                feature_tags = list()
                feature_tags += tags
                #...and add feature-specific tags
                if feature.get('tags'):
                    for t in feature.get('tags'):
                        feature_tags.append(t)
                f = self.publish_feature(org_id, featureset['id'], name, data_type, code, description, granularity, orchestrationStatus, feature_tags)
                return_features.update({f['id']:
                                    {"id": f['id'],
                                    "name": f['name'],
                                    "column": f['code']
                                    }})
            return_featureset['features'] = return_features
        return return_featureset

    @staticmethod
    def _snowflake_connection(member) -> (SnowflakeConnection, dict):
        """
        Constructs connection object for Snowflake data platform
        :param member: credentials for Snowflake data platform

        :return: Connection object to use for query execution
        """
        creds = member.snowflake_creds()
        conn = snowflake.connect(**creds)
        return conn, creds

    @staticmethod
    def _make_select_statement(table_metadata, filters, limit) -> tuple:
        """
        Constructs select * query for table
        """
        query = "SELECT * FROM {database}.{schema}.{table}".format(**table_metadata)
        values = []
        if filters:
            comparisons = []
            for k, v in filters.items():
                if isinstance(v, list):
                    comparisons.append(f"{k} IN ({', '.join(['%s'] * len(v))})")
                    values += v
                else:
                    comparisons.append(f"{k}=%s")
                    values.append(v)
            query += " WHERE " + " and ".join(comparisons)
        if limit:
            query += " LIMIT {}".format(limit)
        return query, values

    @staticmethod
    @track_usage
    def _run_query(conn, query: str, params):
        """
        Execute a query on the [cloud] data platform.

        :param conn: TODO -> abstract the cloud data platform connection
        :param query: String to be executed on the data platform
        :return:
        """
        return conn.cursor().execute(query, params)

    @deprecated("This function has been deprecated, use `get_models` instead.")
    @track_usage
    def get_lists(self) -> List[Model]:
        """
        Deprecated function.  Renamed to `get_models.`
        """
        return self.get_models()

    @deprecated("This function has been deprecated, use `get_model` instead.")
    @track_usage
    def get_feature_list(self, list_id) -> Model:
        """
        Deprecated function.  Renamed to `get_model.`
        """
        return self.get_model(model_id=list_id)
