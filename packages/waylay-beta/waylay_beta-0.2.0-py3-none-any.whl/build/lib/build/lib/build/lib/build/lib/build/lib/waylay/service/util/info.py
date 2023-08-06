"""Python SDK Documentation tooling."""

from typing import Optional, Dict, Union, List

import pandas as pd
import numpy as np

from waylay.service import WaylayServiceContext


def format_links_html(links: Optional[Dict[str, Dict[str, str]]]) -> str:
    """Format link information to an html string."""
    if not links:
        return ''
    link_items = (
        f'<a href="{href}" target="{target}">{text}</a>'
        for target, href, text in (
            (f"_{key}", link.get('href'), link.get('title', key))
            for key, link in links.items()
        )
        if href
    )
    if not link_items:
        return ''
    return " | ".join(link_items)


class InfoTool:
    """Client tool that exposes information about the provided services, recources and operations."""

    def __init__(self, context: WaylayServiceContext):
        """Create a _info_ tool."""
        self._service_context = context

    def action_info_df(
        self,
        service: Optional[Union[str, List[str]]] = None,
        resource: Optional[Union[str, List[str]]] = None,
        links: Optional[Union[str, List[str]]] = None,
    ) -> pd.DataFrame:
        """Produce a pandas DataFrame with an overview of the provided actions.

        Parameters:
            service     filter on the services to be listed
            resource    filter on the resources to be listed
            links       filter on the documentation link names
        """
        def service_filter(name):
            return service is None or name == service or name in service

        def resource_filter(name):
            return resource is None or name == resource or name in resource

        def format_filtered_links(hal_links):
            if not hal_links:
                return ''
            return format_links_html(
                {
                    link: ref
                    for link, ref in hal_links.items()
                    if not links or link in links
                }
            )

        df_doc = pd.DataFrame(np.transpose([
            [
                service.service_key,
                resource.resource_name,
                action.name,
                action.method,
                action.url,
                action.description + "<br>" +
                format_filtered_links(action.hal_links)
            ]
            for service in self._service_context.list()
            if service_filter(service.name)
            for resource in service.list_resources()
            if resource_filter(resource.name)
            for action_name, action in resource.actions.items()
        ]), index=[
            'service',
            'resource',
            'action',
            'method',
            'url',
            'description'
        ], ).T
        return df_doc.set_index(['service', 'resource', 'action'])

    def action_info_html(
        self,
        service: Optional[Union[str, List[str]]] = None,
        resource: Optional[Union[str, List[str]]] = None,
        links: Optional[Union[str, List[str]]] = None,
    ) -> str:
        """Render the service/resource/action listing as an html table.

        Parameters:
            service     filter on the services to be listed
            resource    filter on the resources to be listed
            links       filter on the documentation link names
        """
        return self.action_info_df(service, resource, links).to_html(escape=False)
