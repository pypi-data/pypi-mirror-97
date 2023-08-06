// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React from "react";
import { ChannelHeadingContainer } from "./styled/ChannelHeadingContainer";
import AddChannel from "./AddChannel";

function ColHeadings({ addChannel, channels }) {
  return (
    <div className="column-header">
      <ChannelHeadingContainer className="container-fluid-side row">
        <div className="card-heading is-light-text ">
          <AddChannel addChannel={addChannel} channels={channels} />
        </div>
        <div className="card-heading is-light-text ">
          <h2 className="is-dark-text-light letter-spacing text-medium">
            Data
          </h2>
        </div>
        <div className="card-heading is-light-text ">
          <h2 className="is-dark-text-light letter-spacing text-medium">
            Task
          </h2>
        </div>
        <div className="card-heading is-light-text ">
          <h2 className="is-dark-text-light letter-spacing text-medium">
            Model
          </h2>
        </div>
        <div className="card-heading is-light-text ">
          <h2 className="is-dark-text-light letter-spacing text-medium">
            Sample
          </h2>
        </div>
      </ChannelHeadingContainer>
      {/* Div To Emulate Buttons Div Spacing */}
      <div className="fill-block" />
    </div>
  );
}

export default ColHeadings;
