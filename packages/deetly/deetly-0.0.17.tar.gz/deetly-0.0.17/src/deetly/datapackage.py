"""Datapackage class.

The class contains methods for building and publishing a datapackage.
"""
import datetime
import io
import json
import os
from typing import Any, Dict, List

import pandas as pd
import plotly.io as pio

import deetly.validator
import deetly.utils
from deetly.error import DatapackageError

from enum import Enum


DEFAULT_DEETLY_API = "https://us-central1-mesiqi-238408.cloudfunctions.net/deetlyAPI" 
#DEFAULT_DEETLY_API = "https://api.deetly.com/deetlyAPI"
#DEFAULT_DEETLY_API = "http://localhost:8080" 

class Datapackage:
    """Datapackage resource.

    Attributes:
        id: The id of the datapackage.
        name: The name of the datapackage.
    """

    def __init__(self, metadata: Dict) -> None:
        """Constructor."""
        self.resources = []
        self.views: List = []
        self.metadata: Dict = self._create_datapackage(dict(metadata))

    def _create_datapackage(self, metadata: Dict, schema: str = None) -> Dict:
        """Create datapackage from metadata."""
        now = datetime.datetime.today().isoformat()
        metadata["issued"] = metadata.get("created", now)
        metadata["modified"] = now
        metadata["title"] = metadata.get("title", metadata.get("name", None))
        
        if schema == "dcat": 
            deetly.validator.validate_datapackage_dcat2(metadata)
        else:
            deetly.validator.validate_datapackage_minimal(metadata)
     
        return metadata

    def __repr__(self):
        return json.dumps(self.toJSON())  


    @property
    def id(self) -> str:
        """Datapackage id."""
        _id = self.metadata.get("id", deetly.utils.get_id_from_metadata(self.metadata))
        self.metadata["id"] = _id
        return _id

    
    @property
    def slug(self) -> str:
        """Datapackage slug."""
        _slug = self.metadata.get("slug", deetly.utils.get_slug_from_metadata(self.metadata))
        self.metadata["slug"] = _slug
        return _slug

    @property
    def title(self) -> str:
        """Datapackage title."""
        return self.metadata.get("title", None)


    @property
    def name(self) -> str:
        """Datapackage name."""
        return self.metadata.get("name", None)


    def plot(
        self,
        spec_type: str,
        spec: Dict,
        name: str,
        description: str,
        resources: str or List = [],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Adds a plot/figure/view to the package.

        Creates a dict containg layout, data and metadata

        Args:
            spec_type: For example 'ploty', 'vega' or other type.
            spec: The JSON spec for the view.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        view = {
            "name": name,
            "description": description,
            "specType": spec_type,
            "spec": spec,
            "resources": resources,
        }

        for key, value in kwargs.items():
            view[key] = value

        self.views.append(view)

    def add(self, type: str, content: Any, name: str, description: str = "") -> None:
        """Adds a view view to the package.

        Args:
            content: The view content.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            type: The type of view
        """ 

        if type == 'plotly':
            return self.plotly(content, name, description)

        if type == 'altair':
            return self.altair(content, name, description)
        
        if type == 'link':
            return self.link(content, name, description)

        if type == 'text':
            return self.markdown(content, name, description)

        if type == 'deck':
            return self.deck(content, name, description)

        if type == 'pydeck':
            return self.pydeck(content, name, description)

        if type == 'barlist':
            return self.barlist(content, name, description)

        if type == 'markdown':
            return self.markdown(content, name, description)
        
        if type == 'table':
            return self.table(content, name, description)

        if type == 'vega':
            return self.vega(content, name, description)

        if type == 'pdf':
            return self.pdf(content, name, description)

        if type == 'forcegraph':
            return self.forcegraph(content, name, description)

        if type == 'cytoscape':
            return self.cytoscape(content, name, description)

        if type == 'upload':
            return self.upload(content, name, description)

        if type == 'echart':
            return self.echart(content, name, description)

        print("No viewer available for " + name)

    def echart(self, fig: object, name: str, description: str = "", layout: Dict = {}) -> None:
        """Adds a EChart view to the package.

        Creates a dict containg layout, data and metadata

        Args:
            fig: The echart figure.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        try:
            # check if figure is json option
            spec = {"option": json.loads(json.dumps(fig))}
        except Exception:
            # otherwise assume figure is echart graph
            option = fig.dump_options_with_quotes()
            option = option.replace('\n', '') 
            spec = {"option": json.loads(option)}
        

        self.plot("echart", spec, name, description)


    def plotly(self, fig: Dict, name: str, description: str = "") -> None:
        """Adds a plotly view to the package.

        Creates a dict containg layout, data and metadata

        Args:
            fig: The Plotly figure.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("plotly", pio.to_json(fig), name, description)

    def altair(
        self, fig: Any, name: str, description: str = "", *args: Any, **kwargs: Any
    ) -> None:
        """Adds a Altair view to the package.

        Creates a dict containg layout, data and metadata

        Args:
            fig: The Altair figure.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        self.plot("vega", fig.to_dict(), name, description, *args, **kwargs)

    def vega(
        self, fig: Any, name: str, description: str = "", *args: Any, **kwargs: Any
    ) -> None:
        """Adds a Vega view to the package.

        Creates a dict containg layout, data and metadata

        Args:
            fig: The Vega chart.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        self.plot("vega", fig.to_dict(), name, description, *args, **kwargs)

    def deck(
        self, fig: Any, name: str, description: str = "", *args: Any, **kwargs: Any
    ) -> None:
        """Adds a Deck view to the package.

        Creates a deck.gl view

        Args:
            fig: The Deck chart.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        self.plot("deck", fig, name, description, *args, **kwargs)

    def pydeck(
        self, fig: Any, name: str, description: str = "", *args: Any, **kwargs: Any
    ) -> None:
        """Adds a PyDeck view to the package.

        Creates a dpydeck view

        Args:
            fig: The pydeck chart.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
            args: optional additional argument list.
            kwargs: optional keyworded, argument list.
        """

        self.plot("deck", json.loads(fig.to_json()), name, description, *args, **kwargs)

    def barlist(self, fig: Any, name: str, description: str = "") -> None:
        """Adds a Barlist view to the package.

        Creates barlist view

        Args:
            fig: The specification.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("barlist", fig, name, description)

    def forcegraph(self, fig: Any, name: str, description: str = "") -> None:
        """Adds a ForceGraph view to the package.

        Creates forcegraph view

        Args:
            fig: The specification.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("forcegraph", fig, name, description)

    def cytoscape(self, fig: Any, name: str, description: str = "") -> None:
        """Adds a Cytoscape graph view to the package.

        Creates cytoscape view

        Args:
            fig: The specification.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("cytoscape", fig, name, description)

    def graphviz(self, fig: Any, name: str, description: str = "", *args: Any,
        **kwargs: Any) -> None:
        """Adds a Graphviz graph view to the package.

        Creates graphviz view

        Args:
            fig: The specification.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        fig = {"data": fig}

        self.plot("graphviz", fig, name, description)

    def pdf(
        self, resource: str or object, name: str = "", description: str = ""
    ) -> None:
        """Adds a PDF view to the package.

        Creates pdf view

        Args:
            resource: Name of the resource.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("pdf", {}, name if name else resource, description, resource)

    def table(self, resource: str, name: str = "", description: str = "") -> None:
        """Adds a table view to the package.

        Creates table view

        Args:
            resource: Name of the resource.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        self.plot("table", {}, name if name else resource, description, resource)

    def markdown(self, markdown: str, name: str, description: str = "") -> None:
        """Adds a Markdown view to the package.

        Creates markdown view

        Args:
            fig: The specification.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        spec = {"markdown": markdown}

        self.plot("markdown", spec, name, description)


    def text(self, text: str, name: str = None, description: str = "") -> None:
        """Adds a text/markdown view to the package.

        Creates text/markdown view

        Args:
            fig: The specification.
            name: View name.
            description: Description of the view. Can be plain text or Markdown.
        """

        spec = {"markdown": text}

        if name == None:
            name = text

        self.plot("markdown", spec, name, description)

    def df(self, df: pd.DataFrame, name: str, description: str = "") -> None:
        """Add a pandas dataframe to the package.

        Saves pandas dataframe to gzip'ed csv file.

        Args:
            df: The pandas dataframe
            name: The name of the datasett
            description: Description of the data. Can be plain text or Markdown

        Raises:
            TypeError: The first parameter (df) must be of type pandas.Dataframe().
        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"The first parameter df must be of type pandas.Dataframe()"
            )

        fields = []
        for name, dtype in zip(df.columns, df.dtypes):

            if str(dtype) == "object":
                dtype = "string"
            if str(dtype) == "int64":
                dtype = "number"
            if str(dtype) == "float64":
                dtype = "number"
            if str(dtype) == "bool":
                dtype = "boolean"
            if str(dtype) == "datetime64":
                dtype = "string"
            if str(dtype) == "timedelta[ns]":
                dtype = "string"
            if str(dtype) == "category":
                dtype = "string"
            else:
                dtype = "string"
            fields.append({"name": name, "type": dtype})

        output = io.StringIO()
        df.to_csv(output, index=False)
        data = output.getvalue()
        output.close()

        name = name.replace(" ", "_")

        resource = {
            "name": name,
            "description": description,
            "path": f"/resources/{name}.csv.gz",
            "format": "csv",
            "dsv_separator": ",",
            "mediatype": "text/csv",
            "schema": {"fields": fields},
            "data": data,
        }
        self.resources.append(resource)

    def url(
        self,
        url: str,
        name: str,
        description: str = "",
        format: str = "pdf",
        mediatype: str = "application/pdf",
        resourcetype: str = "url",
    ) -> None:
        """Add a url to the package.

        Args:
            url: Full path
            name: The name of file
            description: Description of the data. Can be plain text or Markdown

        Raises:
            TypeError: The first parameter (url) must be of type str.
        """

        if not isinstance(url, str):
            raise TypeError(f"The first parameter url must be of type str")

        name = name.replace(" ", "_")

        resource = {
            "name": name,
            "description": description,
            "path": url,
            "format": format,
            "mediatype": mediatype,
            "type": resource,
        }
        self.resources.append(resource)

    def link(self, url: str, name: str, description: str = "") -> None:
        """Add a link to the package as a resource

        Args:
            url: The URL of the link
            name: Name 
            description: Description of the data. Can be plain text or Markdown
        """

        (
            resource_name,
            resource_extension,
        ) = deetly.utils.get_name_and_extension_from_url(url)

        link = {
            "name": name,
            "description": description if description else name,
            "path": url,
            "format": resource_extension.replace(".",""),
            "mediatype": deetly.utils.get_media_type(resource_extension),
            "type": "link",
        }

        self.resources.append(link)

    def upload(self, url: str, name: str = "", description: str = "") -> None:
        """Upload a file and add the file as downloadable dataresource to the package.

        Args:
            url: The URL of the file
            name: Name 
            description: Description of the file. Can be plain text or Markdown
        """

        (
            resource_name,
            resource_extension,
        ) = deetly.utils.get_name_and_extension_from_url(url)

        name = name.replace(" ", "_")

        resource = {
            "name": name,
            "description": description if description else name,
            "url": url,
            "format": resource_extension,
            "mediatype": deetly.utils.get_media_type(resource_extension),
            "data": None,
        }

        self.resources.append(resource)

    def _upload_resources(self, space: str, token: str, api: str) -> List:
        resources = []

        # upload resources
        for resource in self.resources:
            try: 
                if resource.get("data", None) is not None:
                    public_url = deetly.utils.upload_file(
                        space,
                        token,
                        self.id,
                        f'resources/{resource["name"]}',
                        resource["mediatype"],
                        resource["data"],
                        api
                    )
                else:
                    public_url = deetly.utils.upload_from_url(
                        space,
                        token,
                        self.id,
                        f'resources/{resource["name"]}',
                        resource["mediatype"],
                        resource["path"],
                        api
                    )

                _resource = {}
                for key, value in resource.items():
                    if key not in ["data"]:
                        _resource[key] = value

                _resource["description"] = resource.get("description", "")
                _resource["url"] = json.loads(public_url).get(
                    "path", resource.get("path", "")
                )
                _resource["type"] = resource.get("type", "dataset")
                resources.append(_resource)
            except:
                name = _resource["name"]
                print(f"Error uploading {name}")
        return resources

    def _get_content(self) -> List:
        content = []
        for view in self.views:
            for key, value in view.items():
                if key == "name":
                    content.append(
                        {
                            "type": "view",
                            "name": value,
                            "description": view.get("description", ""),
                        }
                    )

        return content

    def toJSON(self):
        self.metadata["id"] = self.id
        self.metadata["slug"] = self.slug
        self.metadata["views"] = self.views
        self.metadata["resources"] = self.resources
        return self.metadata

    def publish(self, space: str = None, token: str = None, api: str = None) -> None:
        """Publishes the package to storage and the metadata to elastic seach.

        Args:
            space: The id of the space to publish to.
                Defaults to environment variable [DEETLY_SPACE]
            token: The users token.
                Defaults to environment variable [DEETLY_TOKEN]
            api: The url of the API.
                Defaults to environment variable [DEETLY_API]
        """

        if api is None:
            try:
                api = os.environ["DEETLY_API"]
            except:
                api = DEFAULT_DEETLY_API
                pass

        if space is None:
            try:
                space = os.environ["DEETLY_SPACE"]
            except:
                space = self.metadata.get('space', None)

        if space is None:
            msg = "Space id not provided. Publishing to the 'public' space."
            #print(msg)                

        if token is None:
            try: 
                token = os.environ["DEETLY_TOKEN"]
            except:
                if (space is None):
                    space = 'public'
                    token = 'public'

        if token is None:
            msg = """Your token must be provided either as parameter (token=...)
                    or set with environment variable: DEETLY_TOKEN
            """
            print(msg)
            raise DatapackageError(msg)

        self.metadata["id"] = self.id
        self.metadata["views"] = self.views

        self.metadata["resources"] = self._upload_resources(space, token, api)
        self.metadata["content"] = self._get_content()

        datapackage = json.dumps(self.metadata)

        datapackage_url = None
        try: 
            # upload datapackage
            response = deetly.utils.upload_file(
                space, token, self.id, "datapackage.json", "application/json", datapackage, api
            )
            name = self.metadata.get("name", self.id)  
            print(f"Publishing story {name} to the {space} space...") 

            datapackage_url = json.loads(response).get("url", None)
            if datapackage_url is not None:
                print(f"Published at: https://public.deetly.com/{space}/{self.id}", "\n")
                #print(f"Metadata: {datapackage_url}", "\n")
            else:
                print('Error publishing datapackage')
        except:
            print('Error publishing datapackage')
    
        if datapackage_url is not None:    
            if len(self.metadata["resources"]) > 0:
                print(f"Resources:", "\n")
                for resource in self.metadata["resources"]:
                    print(resource["url"], "\n")

            # extract metadata for elastic search
            metadata = {}
            for key, value in self.metadata.items():
                if key not in ["views"]:
                    metadata[key] = value

            metadata["url"] = datapackage_url
            metadata["space"] = space

            # update elastic search
            try: 
                res = json.loads(deetly.utils.index_document(token, space, metadata, api))
                body = res.get("body", None)
                if not body:
                    print(f"Error updating metadata index: {res}", "\n")

                result = body.get("result", None)

                if not result:
                    print("\n", f"Error updating metadata index: {res}")
            except:
                print(f"Error updating metadata index: {res}", "\n")

 
