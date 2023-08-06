// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React from "react";

const AddChannel = ({ addChannel, channels }) => {
  return (
    <div className="channel-button-container">
      <button
        disabled={channels.length === 4}
        className="channel-button"
        title="Add Channel"
        onClick={addChannel}
      >
        <i className="fas fa-plus-square"></i>
      </button>
    </div>
  );
};

export default AddChannel;
