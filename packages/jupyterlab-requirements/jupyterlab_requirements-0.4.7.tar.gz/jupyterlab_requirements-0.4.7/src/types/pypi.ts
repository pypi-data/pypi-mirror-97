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

// PyPI Data


export class PyPIPackageData {
    constraint: string = "*"
    package_data: any
    repo_data: any
    locked: boolean = true
    version: string | null = null

    constructor(
        readonly package_name?: string,
        data?: {
            constraint?: string,
            locked?: boolean,
            package_name: string,
            package_data: any,
            repo_data?: any,
            version?: string
        } ) {

        Object.assign( this, data )
    }

    get latest(): string { return this.package_data.info.version }

    get releases(): any[] {
        return this.package_data.releases
    }

    get summary(): string { return this.package_data.info.summary }
}