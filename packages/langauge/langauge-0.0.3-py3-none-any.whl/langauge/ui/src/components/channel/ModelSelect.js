// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { Component } from "react";

class ModelSelect extends Component {
  render() {
    return (
      <div>
        <div id={"model-" + this.props.formId}>
          <select
            className="custom-select"
            value={this.props.selectedModel}
            onChange={(event) =>
              this.props.onModelChange(this.props.formId, event.target.value)
            }
          >
            {/* Have we selected our task yet? */}
            {this.props.models.length === 0 ? (
              <option defaultValue>Select Task First</option>
            ) : (
              <option defaultValue>Select A Model</option>
            )}
            {/* Mapping over available models */}
            {this.props.models &&
              this.props.models.map((model) => (
                <option key={model.value} value={model.value}>
                  {model.display}
                </option>
              ))}
          </select>
        </div>
      </div>
    );
  }
}

export default ModelSelect;
