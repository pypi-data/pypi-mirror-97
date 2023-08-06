"""utility to print out the provided services on a SDK client"""

import pandas as pd
import numpy as np
from waylay import WaylayClient

def info(client: WaylayClient) -> pd.DataFrame:
    """Produce a pandas DataFrame with an overview of the provided services"""
    df_doc = pd.DataFrame(np.transpose([
        [service.service_key, resource_name, action_name, action.get('method', ''), action.get('url', ''), action.get('description', '')]
        for service in client._services
        for resource_name, res in service._resources.items()
        for action_name, action in res.actions.items()
    ]), index=['service', 'resource', 'action', 'method', 'url', 'description'], ).T
    return df_doc.set_index(['service', 'resource', 'action'])

if __name__ == "__main__":
    waylay_client = WaylayClient.from_profile()
    print(info(waylay_client).to_html(escape=False))
