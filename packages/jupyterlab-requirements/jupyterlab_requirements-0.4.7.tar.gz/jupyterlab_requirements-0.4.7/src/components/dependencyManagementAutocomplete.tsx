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
import React from 'react';

export interface IProps {
    options: [];
}
export interface IState {
    activeOption: number;
    filteredOptions: [];
    showOptions: boolean;
    userInput: string;
}

export class Autocomplete extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);
        this.state = {
            activeOption: 0,
            filteredOptions: [],
            showOptions: false,
            userInput: ''
        };
        this.onChange = this.onChange.bind(this);
        this.onClick = this.onClick.bind(this);
        // this.onKeyDown = this.onKeyDown.bind(this);
    }

    onChange = (event: React.ChangeEvent<HTMLInputElement>) => {

        const { options } = this.props;
        const userInput = event.target.value;
        const filteredOptions = options;

        this.setState({
            activeOption: 0,
            filteredOptions,
            showOptions: true,
            userInput
            });
    };

    onClick = (event: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
          activeOption: 0,
          showOptions: false,
          userInput: event.target.value
        });
      };

    // onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    //     const { activeOption, filteredOptions } = this.state;
    //     if (e.key === 13) {
    //         this.setState({
    //             activeOption: 0,
    //             showSuggestions: false,
    //             userInput: filteredOptions[activeOption]
    //         });
    //         } else if (e.keyCode === 38) {
    //         if (activeOption === 0) {
    //             return;
    //         }
    //     this.setState({ activeOption: activeOption - 1 });
    //         } else if (e.keyCode === 40) {
    //         if (activeOption - 1 === filteredOptions.length) {
    //             return;
    //         }
    //     this.setState({ activeOption: activeOption + 1 });
    //         }
    //     };

    render() {
        const {
        onChange,
        // onKeyDown,
        state: { activeOption, filteredOptions, showOptions, userInput }
        } = this;

        let optionList;

        if (showOptions && userInput) {
          if (filteredOptions.length) {
            optionList = (
              <ul className="options">
                {filteredOptions.map((optionName, index) => {
                  let className;
                  if (index === activeOption) {
                    className = 'option-active';
                  }
                  return (
                    <li className={className} key={optionName} onClick={() => this.onClick.bind(this)}>
                      {optionName}
                    </li>
                  );
                })}
              </ul>
            );
          } else {
            optionList = (
              <div className="no-options">
                <em>No Option!</em>
              </div>
            );
          }
        }

        return (
            <React.Fragment>
                <div className="search">
                <input
                    type="text"
                    className="search-box"
                    onChange={onChange}
                    // onKeyDown={onKeyDown}
                    value={userInput}
                />
                <input type="submit" value="" className="search-btn" />
                {optionList}
                </div>
            </React.Fragment>
    );
  }
}
export default Autocomplete;