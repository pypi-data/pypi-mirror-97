// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { GeneralControlsBar } from "./styled/GeneralControlsBar";
import React from "react";
import ConfigUpload from "./ConfigUpload";

class ConfigButtons extends React.Component {
  render() {
    return (
      <GeneralControlsBar>
        <ConfigUpload fetchConfig={this.props.fetchConfig} />
        <button
          className="button-generic"
          id="save-config-button"
          title="Save Settings"
          onClick={(event) => this.props.saveConfig(event)}
        >
          <i className="fas fa-save" />
        </button>
        <button
          className="button-generic"
          id="run-config-button"
          title="Run"
          onClick={(event) => this.props.runAll(event)}
        >
          <i className="fas fa-play" />
        </button>
      </GeneralControlsBar>
    );
  }
}

export default ConfigButtons;
