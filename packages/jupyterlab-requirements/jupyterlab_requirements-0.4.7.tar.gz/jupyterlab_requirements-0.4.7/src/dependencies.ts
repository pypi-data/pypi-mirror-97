/**
 * Jupyterlab requirements.
 *
 * Jupyterlab extension for managing dependencies.
 *
 * @link   https://github.com/thoth-station/jupyterlab-requirements#readme
 * @file   Jupyterlab extension for managing dependencies.
 * @author Francesco Murdaca <fmurdaca@redhat.com>
 * @since  0.0.1
 */

// Reference: https://github.com/thoth-station/jupyter-nbrequirements/blob/master/js/src/ui/store.ts

import _ from "lodash";
import { PyPIPackageData } from './types/pypi';
import axios from 'axios'


/**
 * Function: loadDependenciesData from PyPI
 */
export async function load_dependencies_data (
    package_name: string,
    installed_packages: {},
    package_version?: string,
  ): Promise<PyPIPackageData> {

    // get info about the package from PyPI
    let item: PyPIPackageData

    try {
        await axios
            .get( `https://pypi.org/pypi/${ package_name }/json` )
            .then( async response => {
                const package_data = response.data
                const package_urls: { [ k: string ]: string } | null = package_data.info.project_urls

                let repo_data = {}
                if ( package_urls !== null ) {
                    const github_url = Object.values( package_urls )
                        .filter( ( url: string ) => url.match( /github.com/ ) )
                    if ( github_url.length != 0 ) {
                        const m = github_url[ 0 ].match( /github.com\/(.*?)\// )
                        if ( m && m[ 1 ].length > 0 ) {
                            const owner = m[ 1 ]
                            const api_url = `https://api.github.com/repos/${ owner }/${ package_name }`

                            repo_data = await axios.get( api_url )
                                .then( resp => resp.data )
                                .catch( () => { } )
                        }
                    }
                }

                let version = package_version
                if ( typeof package_version !== "string" ) {
                    version = package_version ? package_version : "*"
                }

                item = new PyPIPackageData( package_name, {
                    constraint: version as string,
                    locked: true,
                    package_data: package_data,
                    package_name: package_name,
                    repo_data: repo_data,
                    version: _.get( installed_packages, package_name ),
                } )
        } )
        return JSON.parse(JSON.stringify(item));

    } catch (reason) {
      console.error('Could not retrieve information for package' + package_name + 'due to the following reason:', reason);
    }
}

/**
 * Function: loadDependenciesData from Thoth
 */
// TODO: Load dependencies data from Thoth