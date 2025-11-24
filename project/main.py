#!/usr/bin/env python3
"""
Nexus Populator - Hello World
"""
import json
import os
import urllib.request
import urllib.error
import urllib.parse


def get_nexus_url():
    """
    Get the Nexus URL from environment variables or use defaults.
    
    Reads NEXUS_HOSTNAME and NEXUS_PORT from environment variables.
    Defaults to localhost:48481 if not set.
    
    Returns:
        str: The base URL of the Nexus instance (e.g., "http://localhost:48481")
    """
    hostname = os.getenv( "NEXUS_HOSTNAME", "localhost" )
    port = os.getenv( "NEXUS_PORT", "48481" )
    return f"http://{hostname}:{port}"


def get_repository_names( nexus_url=None ):
    """
    Retrieve a list of repository names from a Nexus instance.
    
    Args:
        nexus_url (str, optional): Base URL of the Nexus instance.
                                   If not provided, will use NEXUS_HOSTNAME and NEXUS_PORT
                                   environment variables, or default to http://localhost:48481
    
    Returns:
        list: A list of repository names (strings)
    
    Raises:
        urllib.error.URLError: If the request fails
        ValueError: If the response cannot be parsed
    """
    if nexus_url is None:
        nexus_url = get_nexus_url()
    
    api_endpoint = f"{nexus_url}/service/rest/v1/repositories"
    
    try:
        with urllib.request.urlopen( api_endpoint ) as response:
            data = json.loads( response.read( ).decode( 'utf-8' ) )
            
            # Extract repository names from the response
            repository_names = [repo.get( 'name' ) for repo in data if 'name' in repo]
            
            return repository_names
    except urllib.error.URLError as e:
        raise urllib.error.URLError( f"Failed to connect to Nexus API at {api_endpoint}: {e}" )
    except json.JSONDecodeError as e:
        raise ValueError( f"Failed to parse JSON response: {e}" )


def get_all_assets( nexus_url=None, repositories=None ):
    """
    Retrieve a list of all assets from specified repositories in a Nexus instance.
    
    This function iterates through the specified repositories and collects assets from each,
    handling pagination automatically. If no repositories are specified, it retrieves assets
    from all repositories.
    
    Args:
        nexus_url (str, optional): Base URL of the Nexus instance.
                                   If not provided, will use NEXUS_HOSTNAME and NEXUS_PORT
                                   environment variables, or default to http://localhost:48481
        repositories (list, optional): List of repository names to retrieve assets from.
                                      If None or empty list, retrieves assets from all repositories.
    
    Returns:
        list: A list of asset dictionaries, each containing asset information
              (id, path, repository, format, downloadUrl, etc.)
    
    Raises:
        urllib.error.URLError: If the request fails
        ValueError: If the response cannot be parsed
    """
    if nexus_url is None:
        nexus_url = get_nexus_url()
    
    # Get all repository names
    all_repository_names = get_repository_names( nexus_url )
    
    # Filter repositories if specified
    if repositories and len( repositories ) > 0:
        # Only use repositories that exist in the Nexus instance
        repository_names = [repo for repo in repositories if repo in all_repository_names]
    else:
        # Use all repositories if repositories is None or empty
        repository_names = all_repository_names
    
    all_assets = []
    
    # Iterate through each repository
    for repository_name in repository_names:
        api_endpoint = f"{nexus_url}/service/rest/v1/assets"
        continuation_token = None
        
        # Handle pagination
        while True:
            # Build URL with query parameters
            params = {"repository": repository_name}
            if continuation_token:
                params["continuationToken"] = continuation_token
            
            # Build query string
            query_string = "&".join( [f"{k}={urllib.parse.quote( str( v ) )}" for k, v in params.items( )] )
            full_url = f"{api_endpoint}?{query_string}"
            
            try:
                with urllib.request.urlopen( full_url ) as response:
                    data = json.loads( response.read( ).decode( 'utf-8' ) )
                    
                    # Extract assets from the response
                    if 'items' in data:
                        all_assets.extend( data['items'] )
                    
                    # Check if there's a continuation token for pagination
                    continuation_token = data.get( 'continuationToken' )
                    if not continuation_token:
                        break  # No more pages
                        
            except urllib.error.URLError as e:
                raise urllib.error.URLError( f"Failed to connect to Nexus API at {full_url}: {e}" )
            except json.JSONDecodeError as e:
                raise ValueError( f"Failed to parse JSON response: {e}" )
    
    return all_assets


def get_all_components( nexus_url=None, repositories=None ):
    """
    Retrieve a list of all components from specified repositories in a Nexus instance.
    
    This function iterates through the specified repositories and collects components from each,
    handling pagination automatically. If no repositories are specified, it retrieves components
    from all repositories.
    
    Args:
        nexus_url (str, optional): Base URL of the Nexus instance.
                                   If not provided, will use NEXUS_HOSTNAME and NEXUS_PORT
                                   environment variables, or default to http://localhost:48481
        repositories (list, optional): List of repository names to retrieve components from.
                                      If None or empty list, retrieves components from all repositories.
    
    Returns:
        list: A list of component dictionaries, each containing component information
              (id, repository, format, group, name, version, assets, etc.)
    
    Raises:
        urllib.error.URLError: If the request fails
        ValueError: If the response cannot be parsed
    """
    if nexus_url is None:
        nexus_url = get_nexus_url()
    
    # Get all repository names
    all_repository_names = get_repository_names( nexus_url )
    
    # Filter repositories if specified
    if repositories and len( repositories ) > 0:
        # Only use repositories that exist in the Nexus instance
        repository_names = [repo for repo in repositories if repo in all_repository_names]
    else:
        # Use all repositories if repositories is None or empty
        repository_names = all_repository_names
    
    all_components = []
    
    # Iterate through each repository
    for repository_name in repository_names:
        api_endpoint = f"{nexus_url}/service/rest/v1/components"
        continuation_token = None
        
        # Handle pagination
        while True:
            # Build URL with query parameters
            params = {"repository": repository_name}
            if continuation_token:
                params["continuationToken"] = continuation_token
            
            # Build query string
            query_string = "&".join( [f"{k}={urllib.parse.quote( str( v ) )}" for k, v in params.items( )] )
            full_url = f"{api_endpoint}?{query_string}"
            
            try:
                with urllib.request.urlopen( full_url ) as response:
                    data = json.loads( response.read( ).decode( 'utf-8' ) )
                    
                    # Extract components from the response
                    if 'items' in data:
                        all_components.extend( data['items'] )
                    
                    # Check if there's a continuation token for pagination
                    continuation_token = data.get( 'continuationToken' )
                    if not continuation_token:
                        break  # No more pages
                        
            except urllib.error.URLError as e:
                raise urllib.error.URLError( f"Failed to connect to Nexus API at {full_url}: {e}" )
            except json.JSONDecodeError as e:
                raise ValueError( f"Failed to parse JSON response: {e}" )
    
    return all_components


def generate_packages_list( repositories, components, output_file="packages_list.json" ):
    """
    Generate a JSON output file listing repository names and components.
    
    This function creates a JSON file containing the specified repositories and components
    in a structured format. Each component in the output will only contain the fields:
    repository, name, version, and assets. Each asset will only contain the fields:
    downloadUrl and path.
    
    Args:
        repositories (list): List of repository names to include in the output.
        components (list): List of component dictionaries to include in the output.
        output_file (str, optional): Path to the output JSON file. Defaults to "packages_list.json".
    
    Returns:
        str: The path to the created output file.
    
    Raises:
        IOError: If the file cannot be written.
        TypeError: If the data cannot be serialized to JSON.
    """
    # Filter components to only include specified fields
    filtered_components = []
    for component in components:
        filtered_component = {}
        # Only include repository, name, version, and assets fields
        if 'repository' in component:
            filtered_component['repository'] = component['repository']
        if 'name' in component:
            filtered_component['name'] = component['name']
        if 'version' in component:
            filtered_component['version'] = component['version']
        if 'assets' in component:
            # Filter assets to only include downloadUrl and path fields
            filtered_assets = []
            for asset in component['assets']:
                filtered_asset = {}
                if 'downloadUrl' in asset:
                    filtered_asset['downloadUrl'] = asset['downloadUrl']
                if 'path' in asset:
                    filtered_asset['path'] = asset['path']
                filtered_assets.append( filtered_asset )
            filtered_component['assets'] = filtered_assets
        filtered_components.append( filtered_component )
    
    # Structure the output data
    output_data = {
        "repositories": repositories,
        "components": filtered_components
    }
    
    try:
        # Write JSON to file with pretty formatting
        with open( output_file, 'w', encoding='utf-8' ) as f:
            json.dump( output_data, f, indent=2, ensure_ascii=False )
        
        return output_file
    except IOError as e:
        raise IOError( f"Failed to write to output file {output_file}: {e}" )
    except TypeError as e:
        raise TypeError( f"Failed to serialize data to JSON: {e}" )


def main():
    print( "Nexus Populator service is running!" )

    repository_names = get_repository_names()

    print( 'repository names' )
    print( '------------------------' )
    for repository_name in repository_names:
        print( f"repository: {repository_name}" )

    #print( 'assets' )
    #print( '------------------------' )
    #assets = get_all_assets( )
    #for asset in assets:
    #    print( f"asset: {asset}" )

    print( 'components' )
    print( '------------------------' )
    components = get_all_components()
    for component in components:
        print( f"component: {component}" )

    generate_packages_list( repository_names, components, '/app/data/packages.json' )


if __name__ == "__main__":
    main()

