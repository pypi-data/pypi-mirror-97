# coding: utf-8
"""
    assetic.layertools  (layertools.py)
    Base file that any gis package needs to inherit from to allow
    integration with Assetic systems
"""
from __future__ import absolute_import

import logging

from assetic import (
    FunctionalLocationRepresentation,
    AssetToolsCompleteAssetRepresentation
)
from assetic.tools import FunctionalLocationTools
from assetic.tools.shared.xml_config_reader import XMLConfigReader
from .config_base import ConfigBase
from .messager_base import MessagerBase

try:
    import pythonaddins
except ImportError:
    # ArcGIS Pro doesn't have this library
    pass
from typing import List, Any
import assetic

from .calculation_tools import CalculationTools
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class LayerToolsBase:
    # define error codes for the asset creation
    results = {
        "success": 0,
        "error": 1,
        "skip": 2,
        "partial": 3,
    }

    def __init__(self, config):

        self._is_valid_config = True
        self.config = config  # type: ConfigBase

        self._layerconfig = self._get_layerconfig(config.layerconfig)

        self._assetconfig = self._layerconfig.assetconfig
        self.asseticsdk = self.config.asseticsdk

        # instantiate assetic.AssetTools
        self.assettools = assetic.AssetTools(self.asseticsdk.client)

        # get logfile name to help user find it
        self.logfilename = ""
        for h in self.asseticsdk.logger.handlers:
            try:
                self.logfilename = h.baseFilename
            except:
                pass

        self.fltools = FunctionalLocationTools(self.asseticsdk.client)
        self.gis_tools = assetic.tools.GISTools(self._layerconfig, self.asseticsdk.client)

        self._calc_tools = self._get_calc_tools()

        self._bulk_threshold = 250
        if self._layerconfig.bulk_threshold:
            self._bulk_threshold = self._layerconfig.bulk_threshold

        self.messager = self.config.messager  # type: MessagerBase
        self.logger = self.messager.logger

        self.xmlconf = self.config.layerconfig  # type: XMLConfigReader

        self.apihelper = assetic.APIHelper(self.asseticsdk.client)

    @property
    def layerconfig(self):
        """
        Asset Layer Configuration
        Cache the XML content so that we don't continually reload it as we
        access it in _get_cat_config
        :return:
        """
        return self._layerconfig

    @property
    def bulk_threshold(self):
        """Gets the minimum threshold before bulk operation applied.
        :return: The integer to set for minimum threshold
        :rtype: int
        """
        return self._bulk_threshold

    @bulk_threshold.setter
    def bulk_threshold(self, value):
        """Sets the minimum threshold before bulk operation applied.
        :param value: The integer to set for minimum threshold
        :type: int
        """
        self._bulk_threshold = value

    def _get_layerconfig(self, layerconfig):
        if layerconfig is None:
            if not self.config.layerconfig:
                msg = "Assetic package missing layer configuration"
                if self.config.asseticsdk:
                    self.config.asseticsdk.logger.error(msg)
                else:
                    logger = logging.getLogger(__name__)
                    logger.error(msg)
                self._is_valid_config = False
                return
            _layerconfig = self.config.layerconfig
        else:
            _layerconfig = layerconfig

        return _layerconfig

    def _get_calc_tools(self):
        if self._layerconfig.calculations_plugin:
            try:
                global_namespace = {
                    "__file__": __file__,
                    "__name__": "custom",
                }
                exec(compile(open(self._layerconfig.calculations_plugin,
                                  "rb").read(),
                             self._layerconfig.calculations_plugin,
                             'exec'), global_namespace)
            except Exception as ex:
                self.asseticsdk.logger.error(str(ex))
                _calc_tools = CalculationTools()
            else:
                try:
                    _calc_tools = global_namespace["FieldCalculations"]()
                except Exception as ex:
                    self.asseticsdk.logger.error(str(ex))
                    _calc_tools = CalculationTools()
        else:
            _calc_tools = CalculationTools()

        return _calc_tools

    def _configuration_missing(self):
        """
        Convenience method that checks if a configuration file
        exists and the configuration can be successfully extracted.

        Also contains centralised log messages.
        """

        if self._is_valid_config is False:
            msg = ("Invalid or missing configuration file, "
                   "asset creation aborted.")
            self.logger.error(msg)
            self.messager.new_message(msg)

        return not self._is_valid_config

    @abc.abstractmethod
    def get_rows(self, lyr, fields, query=None):
        pass

    @abc.abstractmethod
    def get_geom_geojson(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_geom_wkt(self, *args, **kwargs):
        """
        Get the well known text for a geometry in 4326 projection
        :param outsrid: The projection EPSG code to export WKT as (integer)
        :param geometry: The input geometry
        :returns: wkt string of geometry in the specified projection
        """
        pass

    @abc.abstractmethod
    def create_funclocs_from_layer(self, lyr, query=None):
        # type: (Any, str) -> (int, int)
        """
        Iterates over the rows in a passed in layer (narrowed down by
        optional query) and creates functional locations defined in
        the data.

        Returns the number of successful and failed functional
        locations.

        :param lyr: passed in arcgis layerfile
        :param query: query to select certain attributes
        :return: number created, number failed
        """
        pass

    @abc.abstractmethod
    def update_funclocs_from_layer(self, lyr, query=None):
        # type: (Any, str) -> (int, int)
        """
        Iterates over the rows in a passed in layer (narrowed down by
        optional query) and updates functional locations defined in
        the data.

        Returns the number of successful and failed updates of functional
        locations.

        :param lyr: passed in arcgis layerfile
        :param query: query to select certain attributes
        :return: number created, number failed
        """
        pass

    def _new_asset(self, row, lyr_config, fields, *args, **kwargs):
        """
        Create a new asset for the given search result row

        :param row: a layer search result row, to create the asset for
        :param lyr_config: configuration object for asset field mapping
        :param fields: list of attribute fields
        :returns: Boolean True if success, else False
        """

        # Add calculated output fields to field list so that they are
        # considered valid
        all_calc_output_fields = lyr_config["all_calc_output_fields"]

        if all_calc_output_fields:
            fields = list(set(all_calc_output_fields + fields))

        complete_asset_obj = self.get_asset_obj_for_row(row, lyr_config, fields)

        # alias core fields for readability
        corefields = lyr_config["corefields"]

        # verify it actually needs to be created
        if "id" in corefields and corefields["id"] in fields:
            if not complete_asset_obj.asset_representation.id:
                # guid field exists in ArcMap and is empty
                newasset = True
            else:
                # guid id populated, must be existing asset
                # return early with passed error code
                newasset = False
        else:
            # guid not used, what about asset id?
            if "asset_id" in corefields and corefields["asset_id"] in fields:
                # asset id field exists in Arcmap
                if not complete_asset_obj.asset_representation.asset_id:
                    # asset id is null, must be new asset
                    newasset = True
                else:
                    # test assetic for the asset id.
                    # Perhaps user is not using guid
                    # and is manually assigning asset id.
                    chk = self.assettools.get_asset(
                        complete_asset_obj.asset_representation.asset_id)
                    if not chk:
                        newasset = True
                    else:
                        # asset id already exists.  Not a new asset
                        newasset = False
            else:
                # there is no field in ArcMap representing either GUID or
                # Asset ID, so can't proceed.
                self.asseticsdk.logger.error(
                    "Asset not created because there is no configuration "
                    "setting for <id> or <asset_id> or the field is not in "
                    "the layer")

                return self.results["error"]

        if not newasset:
            self.asseticsdk.logger.warning(
                "Did not attempt to create asset because it already has the following "
                "values: Asset ID={0},Asset GUID={1}".format(
                    complete_asset_obj.asset_representation.asset_id
                    , complete_asset_obj.asset_representation.id))

            return self.results["skip"]

        # set status
        complete_asset_obj.asset_representation.status = \
            lyr_config["creation_status"]

        # Create new asset
        asset_repr = self.assettools.create_complete_asset(complete_asset_obj)

        if asset_repr is None:
            # this occurs when the asset creation has failed
            # components/dimensions - no attempt was made to create
            self.messager.new_message("Asset Not Created - Check log")

            return self.results['error']

        # apply asset guid and/or assetid
        if "id" in corefields:
            row[corefields["id"]] = asset_repr.asset_representation.id
        if "asset_id" in corefields:
            row[corefields["asset_id"]] = asset_repr.asset_representation.asset_id

        # apply component id
        for component_dim_obj in asset_repr.components:
            for component_config in lyr_config["components"]:
                component_type = None
                if "component_type" in component_config["attributes"]:
                    component_type = component_config["attributes"][
                        "component_type"]
                elif "component_type" in component_config["defaults"]:
                    component_type = component_config["defaults"][
                        "component_type"]

                # Apply the component GUID to the feature
                if ("id" in component_config["attributes"]) and (component_type
                                                                 == component_dim_obj.component_representation.component_type):
                    row[component_config["attributes"]["id"]] = \
                        component_dim_obj.component_representation.id

                # Apply the component friendly id to the feature
                if "name" in component_config["attributes"] and \
                        component_type \
                        == component_dim_obj.component_representation \
                        .component_type:
                    row[component_config["attributes"]["name"]] = \
                        component_dim_obj.component_representation.name

        # apply FL ids to feature
        if asset_repr.functional_location_representation:
            fl_resp = asset_repr.functional_location_representation
            fl_conf = lyr_config["functionallocation"]
            # apply guid if there is a field for it
            if "id" in fl_conf and fl_conf["id"] in row:
                row[fl_conf["id"]] = fl_resp.id
            # apply friendly id if there is a field for it
            if "functional_location_id" in fl_conf and \
                    fl_conf["functional_location_id"] in row:
                row[fl_conf["functional_location_id"]] = \
                    fl_resp.functional_location_id

        # Now check config and update Assetic with spatial data and/or address
        addr = None
        geojson = None
        if len(lyr_config["addressfields"]) > 0 \
                or len(lyr_config["addressdefaults"]) > 0:
            # get address details
            addr = assetic.CustomAddress()
            # get address fields from the attribute fields of the feature
            for k, v in six.iteritems(lyr_config["addressfields"]):
                if k in addr.to_dict() and v in fields:
                    setattr(addr, k, row[v])
            # get address defaults
            for k, v in six.iteritems(lyr_config["addressdefaults"]):
                if k in addr.to_dict():
                    setattr(addr, k, v)

        if all([lyr_config["upload_feature"], "SHAPE@" in row, "SHAPE@XY" in row]):
            geometry = row['SHAPE@']
            centroid = row['SHAPE@XY']
            geojson = self.get_geom_geojson(4326, geometry, centroid)

        if addr or geojson:
            chk = self.assettools.set_asset_address_spatial(
                asset_repr.asset_representation.id, geojson, addr)
            if chk > 0:
                e = ("Error attempting creation of complete asset - "
                     "asset creation successful but failed during creation "
                     "of spatial data. See log.")
                self.asseticsdk.logger.error(e)

                return self.results['partial']

        if asset_repr.error_code in [2, 4, 16]:
            # component (2), or dimension (4) or Fl (16) error
            return self.results['partial']

        return self.results['success']

    @abc.abstractmethod
    def create_assets(self, lyr, query=None):
        pass

    @abc.abstractmethod
    def update_assets(self, lyr, query=None):
        pass

    def bulk_update_rows(self, rows, lyr, lyr_config):
        """
        Initiate bulk update of assets and components etc via Data Exchange
        :param rows: list of dictionaries, each row is a record from GIS
        :param lyr: the GIS layer being processed
        :param lyr_config: The configuration settings for the layer from
        the XML file
        :return: valid rows - the rows for where the asset actually exists
        """
        if len(lyr_config["all_calc_output_fields"]) > 0:
            # there are calculated fields to manage
            for row in rows:
                for calculation in lyr_config["calculations"]:
                    calc_val = self._calc_tools.run_calc(
                        calculation["calculation_tool"],
                        calculation["input_fields"]
                        , row, lyr_config["layer"])
                    if calc_val:
                        row[calculation["output_field"]] = calc_val

        lyr_name = lyr.name
        message = 'Commencing Data Exchange bulk update initiation'
        self.messager.new_message(message, "Assetic Integration")

        # Bulk update assets will return valid rows, invalid rows are asset id
        # not found or disposed assets
        chk, valid_rows = self.gis_tools.bulk_update_assets(rows, lyr_name)
        if chk != 0:
            message = "Error encountered bulk updating assets"
            self.messager.new_message(message, "Assetic Integration")
        if len(valid_rows) == 0:
            self.messager.new_message("No valid assets for update"
                                      , "Assetic Integration")
        self.gis_tools.bulk_update_components(valid_rows, lyr_name)
        self.gis_tools.bulk_update_addresses(valid_rows, lyr_name)
        self.gis_tools.bulk_update_networkmeasures(valid_rows, lyr_name)
        self.gis_tools.bulk_update_asset_fl_assoc(valid_rows, lyr_name)
        if lyr_config["upload_feature"]:
            self.bulk_update_spatial(valid_rows, lyr, lyr_config)

        message = 'Completed initiating Data Exchange updates, updates may ' \
                  'still be in progress. Check Data Exchange History page'
        self.messager.new_message(message, "Assetic Integration")
        return chk, valid_rows

    def bulk_update_spatial(self, rows, lyr, lyr_config):
        # type: (list, str, dict) -> int
        """
        For the given rows use dataExchange to bulk upload spatial
        :param rows: a list of rows from layer
        :param lyr: the layer being processed
        :param lyr_config: the XML config for the layer
        :return: 0=success, else error
        """
        # get some info about the layer
        desc = arcpy.Describe(lyr)
        shape_type = desc.shapeType

        # will need to project to EPSG4326 for output
        tosr = arcpy.SpatialReference(4326)

        spatial_rows = list()
        # loop through rows and get WKT
        for row in rows:
            if "SHAPE@" in row:
                row_dict = dict()
                polygonwkt = ""
                linewkt = ""
                if "asset_id" in lyr_config["corefields"]:
                    asset_id = row[lyr_config["corefields"]["asset_id"]]
                elif "id" in lyr_config["corefields"]:
                    asset_guid = row[lyr_config["corefields"]["asset_id"]]
                    asset = self.assettools.get_asset(asset_guid)
                    if asset != None:
                        asset_id = asset["AssetId"]
                    else:
                        msg = "Asset with ID [{0}] not found".format(
                            asset_guid)
                        self.logger.warning(msg)
                        continue
                else:
                    self.logger.warning(
                        "No asset ID field for spatial upload.  No upload "
                        "performed")
                    return 1

                # get geometry and process
                geometry = row['SHAPE@']
                new_geom = geometry.projectAs(tosr)
                if shape_type == "Polygon":
                    polygonwkt = new_geom.WKT
                elif shape_type == "Polyline":
                    linewkt = new_geom.WKT

                # define the point for all feature types
                pt_geometry = arcpy.PointGeometry(geometry.centroid
                                                  , geometry.spatialReference)
                pointwkt = pt_geometry.projectAs(tosr).WKT

                row_dict["Asset ID"] = asset_id
                row_dict["Point"] = pointwkt
                row_dict["Polygon"] = polygonwkt
                row_dict["Line"] = linewkt
                spatial_rows.append(row_dict)
            else:
                # missing spatial data
                self.logger.warning(
                    "Missing spatial data in bulk upload, no bulk update "
                    "performed")
                return 1

        if len(spatial_rows) > 0:
            self.gis_tools.bulk_update_spatial(spatial_rows)
        return 0

    @abc.abstractmethod
    def individually_update_rows(self, rows, lyr_config, fields, dialog):
        # type: (List[dict], dict, List[str], Any) -> None
        """
        Iterates over the rows of the layerfile and updates each asset
        using API calls.

        :param rows: <List[dict]> a list of dicts where keys are the
        column names and values are cell contents
        :param lyr_config: <dict> dict defining the relationship
        between xml nodes and the layer's column values
        :param fields: <List[str]> a list of column names from the layer
        :param dialog: <Unsure> arcpy dialog object that allows arcpy
        messages to be pushed to console
        :return:
        """

        lyrname = lyr_config['layer']

        total = len(rows)

        # initialise counters for the log messages
        num_pass = 0
        num_fail = 0

        for i, row in enumerate(rows):
            success = self._update_asset(row, lyr_config, fields)

            if self.commontools.is_desktop:
                if self.config.force_use_arcpy_addmessage:
                    # Using the progressor
                    arcpy.SetProgressorLabel(
                        "Updating Assets for layer {0}.\nProcessing "
                        "feature {1} of {2}".format(
                            lyrname, i + 1, total))
                    arcpy.SetProgressorPosition()
                else:
                    dialog.description = \
                        "Updating Assets for layer {0}." \
                        "\nProcessing feature {1} of {2}".format(
                            lyrname, i + 1, total)
                    dialog.progress = (i + 1 / total) * 100
            else:
                msg = "Updating Assets for layer {0}." \
                      "\nProcessing feature {1} of {2}".format(
                    lyrname, i + 1, total)
                self.commontools.new_message(msg)
                self.logger.info(msg)

            if success:
                num_pass = num_pass + 1
            else:
                num_fail = num_fail + 1

        message = "Finished {0} Asset Update, {1} assets updated".format(
            lyrname, str(num_pass))

        if num_fail > 0:
            message = "{0}, {1} assets not updated. (Check log file '{2}')" \
                      "".format(message, str(num_fail), self.logfilename)

        self.commontools.new_message(message, "Assetic Integration")

    def _attach_functionallocation(self, asset_repr, row, lyr_config):
        # type: (AssetToolsCompleteAssetRepresentation, dict, dict) -> int
        """
        Retrieves the functional location information relating to the asset
        from the row and attaches it to the asset representation

        :param asset_repr: <AssetToolsCompleteAssetRepresentation>
        :param row: <dict> arcpy row
        :param lyr_config: <dic> customer defined config values
        :return: None - object modified in place
        """

        flfields = lyr_config['functionallocation']

        flid = None
        flname = None
        fltype = None
        if "functional_location_id" in flfields and \
                flfields['functional_location_id'] in row:
            flid = row[flfields['functional_location_id']]
        if "functional_location_name" in flfields and \
                flfields['functional_location_name'] in row:
            flname = row[flfields['functional_location_name']]
        if "functional_location_type" in flfields and \
                flfields['functional_location_type'] in row:
            fltype = row[flfields['functional_location_type']]

        if flname not in ['', None] and fltype not in ['', None]:
            # User has specified name and type indicating a requirement to
            # create the FL if not exist.
            # First check if FL already exists
            flrepr = self.fltools.get_functional_location_by_name_and_type(
                flname, fltype)

            if flrepr is None:
                # e.g. the FL doesn't exist
                f = FunctionalLocationRepresentation()

                fltypeid = self.fltools.get_functional_location_type_id(fltype)

                f.functional_location_id = flid
                f.functional_location_type = fltype
                f.functional_location_name = flname
                f.functional_location_type_id = fltypeid

                flrepr = self.fltools.create_functional_location(f)
                if flrepr is None:
                    # e.g. an error occurred while creating
                    return 1

        elif flid not in ['', None]:
            flrepr = self.fltools.get_functional_location_by_id(flid)

        else:
            # No config for FL.  not an error though.
            return 0

        asset_repr.functional_location_representation = flrepr

        return 0

    def retrieve_asset_id(self, asset_representation):
        chk = self.assettools.get_asset(
            asset_representation.asset_id)

        if chk:
            # set the guid, need it later if doing spatial load
            asset_representation.id = chk["Id"]

    def _update_components(self, complete_asset_obj):
        # type: (AssetToolsCompleteAssetRepresentation) -> None
        """
        Iterate over components retrieved for asset and update any changes.

        :param complete_asset_obj: <AssetToolsCompleteAssetRepresentation>
        :return: None
        """

        # have components, assume network measure needed, also assume we
        # don't have Id's for the components which are needed for update
        current_complete_asset = self.assettools.get_complete_asset(
            complete_asset_obj.asset_representation.id, []
            , ["components", "dimensions"])

        # get an asset ID to use for messaging if error
        asset_id = complete_asset_obj.asset_representation.asset_id
        if not asset_id:
            asset_id = complete_asset_obj.asset_representation.id

        for component in reversed(complete_asset_obj.components):
            # get the id from the current record, matching on
            # component type
            new_comp = component.component_representation
            for current_comp_rep in current_complete_asset.components:
                current_comp = current_comp_rep.component_representation
                if current_comp.component_type == new_comp.component_type \
                        or current_comp.id == new_comp.id:
                    # set the id and name in case they are undefined
                    new_comp.id = current_comp.id
                    new_comp.name = current_comp.name

                    # Look for dimensions and set dimension Id
                    for dimension in component.dimensions:
                        count_matches = 0
                        for current_dim in current_comp_rep.dimensions:
                            # match on id or (nm type and record
                            # type and shape name)
                            if not dimension.id and \
                                    dimension.network_measure_type == \
                                    current_dim.network_measure_type and \
                                    dimension.record_type == \
                                    current_dim.record_type and \
                                    dimension.shape_name == \
                                    current_dim.shape_name:
                                # set dimension id and component id
                                dimension.id = current_dim.id
                                dimension.component_id = new_comp.id
                                count_matches += 1
                        if not dimension.id or count_matches > 1:
                            # couldn't find unique id. remove
                            component.dimensions.remove(dimension)
                            self.asseticsdk.logger.warning(
                                "Unable to update dimension for "
                                "component {0} because new existing and "
                                "distinct dimension record was "
                                "found".format(
                                    new_comp.name))
            if not new_comp.id:
                # couldn't find component - remove
                complete_asset_obj.components.remove(component)
                self.logger.warning(
                    "Unable to update component for asset '{0}' becuase "
                    "no existing or unique component of type '{1}' and "
                    "name '{2}' was found".format(
                        asset_id
                        , new_comp.component_type, new_comp.label
                    ))

    def upload_features(self, row, complete_asset_obj, lyr_config, fields):
        # type: (dict, AssetToolsCompleteAssetRepresentation, dict, List[str]) -> bool
        """
        Uploads the address and point data against the asset defined
        in the complete_asset_obj.

        :param row: row representing a layer row
        :param complete_asset_obj: object representing asset with attached
        components, dimensions, functiona location, etc.
        :param lyr_config: customer-defined configuration found in xml file
        :param fields:
        """

        # get address details
        addr = assetic.CustomAddress()
        # get address fields the attribute fields of the feature
        for k, v in six.iteritems(
                lyr_config["addressfields"]):
            if k in addr.to_dict() and v in fields:
                setattr(addr, k, row[v])
        # get address defaults
        for k, v in six.iteritems(
                lyr_config["addressdefaults"]):
            if k in addr.to_dict():
                setattr(addr, k, v)
        if 'SHAPE@' in row and 'SHAPE@XY' in row:
            geometry = row['SHAPE@']
            centroid = row['SHAPE@XY']
            geojson = self.get_geom_geojson(4326, geometry, centroid)
        else:
            geojson = None
        chk = self.assettools.set_asset_address_spatial(
            complete_asset_obj.asset_representation.id, geojson, addr)
        if chk > 0:
            self.messager.new_message(
                "Error Updating Asset Address/Location:{0}, Asset GUID={1}"
                "".format(
                    complete_asset_obj.asset_representation.asset_id
                    , complete_asset_obj.asset_representation.id))
            return False

        return True

    def _update_asset(self, row, lyr_config, fields):
        # type: (dict, dict, list) -> bool
        """
        Update an existing asset for the given arcmap row

        :param row: a layer search result row, to create the asset for
        :param lyr_config: configuration object for asset field mapping
        :param fields: list of attribute fields
        :returns: Boolean True if success, else False
        """
        # Add calculated output fields to field list so that they are
        # considered valid
        all_calc_output_fields = lyr_config["all_calc_output_fields"]
        if all_calc_output_fields:
            fields = list(set(all_calc_output_fields + fields))

        # retrieve all of the asset info from the row and attach
        complete_asset_obj = self.get_asset_obj_for_row(row, lyr_config, fields)

        if complete_asset_obj.asset_representation.id is None:
            if complete_asset_obj.asset_representation.asset_id:
                chk = self.assettools.get_asset(
                    complete_asset_obj.asset_representation.asset_id)

                if chk:
                    # set the guid, need it later if doing spatial load
                    complete_asset_obj.asset_representation.id = chk["Id"]

        # if still no ID, return false and exit
        if complete_asset_obj.asset_representation.id is None:
            self.asseticsdk.logger.warning(
                "Asset not updated because it is undefined or not in Assetic. "
                "Asset ID={0}".format(
                    complete_asset_obj.asset_representation.asset_id))
            return False

        # attach functional location representation to the asset using
        # row info (creates funcloc if it doesn't exist)
        errcode = self._attach_functionallocation(complete_asset_obj, row, lyr_config)

        if errcode > 0:
            return False

        if len(complete_asset_obj.components) > 0:
            self._update_components(complete_asset_obj)

        # update the asset attributes
        chk = self.assettools.update_complete_asset(complete_asset_obj)

        if chk > 0:
            self.messager.new_message(
                "Error Updating Asset:{0}, Asset GUID={1}".format(
                    complete_asset_obj.asset_representation.asset_id
                    , complete_asset_obj.asset_representation.id))
            return False

        if lyr_config["upload_feature"]:
            chk = self.upload_features(row, complete_asset_obj, lyr_config, fields)

            if not chk:
                return False

        return True

    def get_asset_obj_for_row(self, row, lyr_config, fields):
        """
        Prepare a complete asset for the given search result row using data
        from within the row

        :param row: a layer search result row, to create the asset for
        :param lyr_config: configuration object for asset field mapping
        :param fields: list of attribute fields in the layer
        :returns: assetic.AssetToolsCompleteAssetRepresentation() or None
        """
        # instantiate the complete asset representation to return
        complete_asset_obj = AssetToolsCompleteAssetRepresentation()

        # create an instance of the complex asset object
        asset = assetic.models.ComplexAssetRepresentation()

        # set status (mandatory field)
        # asset.status = "Active"

        asset.asset_category = lyr_config["asset_category"]

        # apply field calculations first
        for calculation in lyr_config["calculations"]:
            calc_val = self._calc_tools.run_calc(
                calculation["calculation_tool"], calculation["input_fields"]
                , row, lyr_config["layer"])
            if calc_val:
                row[calculation["output_field"]] = calc_val
        # set core field values from arcmap fields
        for xml, lyrcol in six.iteritems(lyr_config["corefields"]):
            chk_xml = xml in asset.to_dict().keys()
            chk_lyr = lyrcol in fields
            chk_lyr_none = row[lyrcol] is not None
            chk_str_null = str(row[lyrcol]).strip() != ""
            if all([chk_xml, chk_lyr, chk_lyr_none, chk_str_null]):
                setattr(asset, xml, row[lyrcol])

        # set core field values from defaults
        for xml, lyrcol in six.iteritems(lyr_config["coredefaults"]):
            if xml in asset.to_dict() and str(lyrcol).strip() != "":
                setattr(asset, xml, lyrcol)

        attributes = {}
        # set attributes values from arcmap fields
        if "attributefields" in lyr_config:
            for xml, lyrcol in six.iteritems(lyr_config["attributefields"]):
                if lyrcol in fields and row[lyrcol] is not None and \
                        str(row[lyrcol]).strip() != "":
                    attributes[xml] = row[lyrcol]
        # set attribute values from defaults
        for xml, lyrcol in six.iteritems(lyr_config["attributedefaults"]):
            if str(lyrcol).strip() != "":
                attributes[xml] = lyrcol
        # add the attributes to the asset and the asset to the complete object
        asset.attributes = attributes
        complete_asset_obj.asset_representation = asset

        # create component representations
        for component in lyr_config["components"]:
            comp_tool_rep = assetic.AssetToolsComponentRepresentation()
            comp_tool_rep.component_representation = \
                assetic.ComponentRepresentation()
            for xml, lyrcol in six.iteritems(component["attributes"]):
                if lyrcol in fields and row[lyrcol] is not None and \
                        str(row[lyrcol]).strip() != "":
                    setattr(comp_tool_rep.component_representation, xml
                            , row[lyrcol])
            for xml, lyrcol in six.iteritems(component["defaults"]):
                if xml in comp_tool_rep.component_representation.to_dict():
                    setattr(comp_tool_rep.component_representation, xml, lyrcol)

            # add dimensions to component
            if component["dimensions"] and len(component["dimensions"]) > 0:
                # create an array for the dimensions to be added
                # to the component
                dimlist = list()
                for dimension in component["dimensions"]:
                    # Create an instance of the dimension and set minimum fields
                    dim = assetic.ComponentDimensionRepresentation()
                    for xml, lyrcol in six.iteritems(dimension["attributes"]):

                        # only set attribute on dimension repr. if column defined
                        # in xml and is not None or ''
                        if (lyrcol in fields) and (row[lyrcol] is not None) and \
                                (str(row[lyrcol]).strip() != ""):
                            setattr(dim, xml, row[lyrcol])
                    for xml, lyrcol in six.iteritems(dimension["defaults"]):
                        if xml in dim.to_dict():
                            setattr(dim, xml, lyrcol)

                    # if comp_tool_rep.component_representation.dimension_unit is None:
                    # try to set the componenent's dimension to the thing
                    # todo - is it correct defining dimension unit within the
                    # comp_tool_rep.component_representation.dimension_unit = dim.dimension_unit
                    # comp_tool_rep.component_representation.network_measure_type = dim.network_measure_type

                    dimlist.append(dim)

                # Add the dimension array to the component
                comp_tool_rep.dimensions = dimlist

            # add the component array
            complete_asset_obj.components.append(comp_tool_rep)

        # add functional location to representation
        self._attach_functionallocation(complete_asset_obj, row, lyr_config)

        return complete_asset_obj

    def set_asset_address_spatial(self, assetid, lyr_config, geojson,
                                  addr=None):
        """
        Set the address and/or spatial definition for an asset
        :param assetid: The asset GUID (TODO support friendly ID)
        :param lyr_config: The settings defined for the layer
        :param geojson: The geoJson representation of the feature
        :param addr: Address representation.  Optional.
        assetic.CustomAddress
        :returns: 0=no error, >0 = error
        """
        if (addr is not None) and \
                not isinstance(addr, assetic.CustomAddress):
            msg = "Format of address incorrect,expecting " \
                  "assetic.CustomAddress"
            self.asseticsdk.logger.debug(msg)
            return 1
        else:
            addr = assetic.CustomAddress()

        # get guid
        assetguid = self.xmlconf.get_layer_asset_guid(assetid, lyr_config)
        if assetguid is None:
            msg = "Unable to obtain asset GUID for assetid={0}".format(assetid)
            self.asseticsdk.logger.error(msg)
            return 1
        chk = self.assettools.set_asset_address_spatial(assetguid, geojson,
                                                        addr)
        return 0

    def decommission_asset(self, assetid, lyr_config, comment=None):
        """
        Set the status of an asset to decommisioned
        :param assetid: The asset GUID (TODO support friendly ID)
        :param lyr_config: config details for layer
        :param comment: A comment to accompany the decommision
        :returns: 0=no error, >0 = error
        """

        return 1

    @staticmethod
    def find_funcloc(flreprs, **attrs):
        """
        Attempt to find a functional location matching the passed in
        attributes.
        :param flreprs:
        :param attrs:
        :return:
        """

        for fl in flreprs:
            matchs = []
            for attr, attrval in attrs.items():
                matchs.append(fl.__getattribute__(attr) == attrval)

            if all(matchs):
                return fl

        return None

    @staticmethod
    def _get_fl_attrvals(row, attrs, defattrs):
        # type: (dict, dict, dict) -> dict
        """
        Creates a dictionary of attributes from row values
        to attach to a functional location representation.
        :param row: row representation

        :param attrs: dict defining relationship between odata
        value and the layer column name
        :param defattrs: dict defining relationship between odata
        value and the default value
        :return: dict containing attributes
        """

        attrvals = {}

        for cloud, lyrcol in six.iteritems(attrs):
            val = row[lyrcol]

            if val in ['', None]:
                # don't want blank values causing potential errors
                continue

            attrvals[cloud] = val

        attrvals.update(defattrs)

        return attrvals

    def _create_fl_from_row(self, row, fl_fields, fltype, attrs, def_attrs):
        # type: (dict, dict, str, dict, dict) -> FunctionalLocationRepresentation
        """
        Retrieves information from a cursor row and attempts to create
        a functional location from the data.

        :param row: arcgis layer row, converted to a dictionary
        :param fl_fields: dict that defines relationship between functional
        location fields and the layer column names
        :param fltype: valid FL cloud type
        :param attrs: FL attributes, in form of {oData val: layer column}
        :param def_attrs: FL default attributes, in form of {oData val:
        default val}
        :return:
        """

        # instantiate representation
        new_flepr = FunctionalLocationRepresentation()

        if "functional_location_id" in fl_fields and \
                fl_fields['functional_location_id'] in row:
            # set the user friendly FL ID.  It is not required if auto-id on
            new_flepr.functional_location_id = row[fl_fields[
                'functional_location_id']]

        new_flepr.functional_location_name = row[fl_fields[
            'functional_location_name']]

        try:
            fltype_id = self.fltools.get_functional_location_type_id(fltype)
        except KeyError:
            msg = ("Failed to find Functional Location Type Id for FL "
                   "{0}, which is an invalid FL Type.".format(fltype))
            self.fltools.logger.error(msg)
            return None

        new_flepr.functional_location_type = fltype
        new_flepr.functional_location_type_id = fltype_id
        attr_vals = self._get_fl_attrvals(row, attrs, def_attrs)
        new_flepr.attributes = attr_vals
        flrepr = self.fltools.create_functional_location(new_flepr)

        return flrepr

    @staticmethod
    def _retrieve_fl_attrs_from_row(row, attrs, def_attrs):
        """
        Attach new attributes relating to functional locations in to the layer attributes
        :param row:
        :param attrs:
        :param def_attrs:
        :return:
        """
        attrvals = {}
        for od, lyrcol in six.iteritems(attrs):
            attrvals[od] = row[lyrcol]

        attrvals.update(def_attrs)

        return attrvals

    def is_new_asset(self, xmlcorefields, lyrfields, assetobj):
        """
        A method to determine, given a row of a table and the field
        definitions, if the row needs to be created.
        :param xmlcorefields:
        :param lyrfields:
        :param assetobj:
        """

        # verify it actually needs to be created
        if ("id" in xmlcorefields) and (xmlcorefields["id"] in lyrfields):
            if assetobj.asset_representation.id is None:
                # guid field exists in ArcMap and is empty
                newasset = True
            else:
                # guid id populated, must be existing asset
                # return early with passed error code
                newasset = False
        else:
            # guid not used, what about asset id?
            if ("asset_id" in xmlcorefields) and (xmlcorefields["asset_id"] in lyrfields):
                # asset id field exists in Arcmap
                if assetobj.asset_representation.asset_id is None:
                    # asset id is null, must be new asset
                    newasset = True
                else:
                    # test assetic for the asset id.
                    # Perhaps user is not using guid
                    # and is manually assigning asset id.
                    chk = self.assettools.get_asset(
                        assetobj.asset_representation.asset_id)
                    if chk is None:
                        newasset = True
                    else:
                        # asset id already exists.  Not a new asset
                        newasset = False
            else:
                # there is no field in integration representing either GUID or
                # Asset ID, so can't proceed.
                self.logger.error(
                    "Asset not created because there is no configuration "
                    "setting for <id> or <asset_id> or the field is not in "
                    "the layer")

                # set newasset to None so it can be handled by integration
                newasset = None

        if newasset is False:
            self.logger.warning(
                "Did not attempt to create asset because it already has the "
                "following values: Asset ID={0},Asset GUID={1}".format(
                    assetobj.asset_representation.asset_id,
                    assetobj.asset_representation.id))

        return newasset

    @staticmethod
    def set_assetic_spatial_attributes(row, lyr_config, lyrfields):
        # Now check config and update Assetic with spatial data and/or address
        addr = None
        geojson = None
        if len(lyr_config["addressfields"]) > 0 \
                or len(lyr_config["addressdefaults"]) > 0:
            # get address details
            addr = assetic.CustomAddress()
            # get address fields from the attribute fields of the feature
            for k, v in six.iteritems(lyr_config["addressfields"]):
                if k in addr.to_dict() and v in lyrfields:
                    setattr(addr, k, row[v])

            # get address defaults
            for k, v in six.iteritems(lyr_config["addressdefaults"]):
                if k in addr.to_dict():
                    setattr(addr, k, v)

        if lyr_config["upload_feature"] and "geom_geojson" in row:
            geojson = row["geom_geojson"]

        return addr, geojson
