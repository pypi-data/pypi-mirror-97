// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { useRef } from "react";

function ConfigUpload(props) {
  const fileInput = useRef(null);

  const fileChange = (e) => {
    // Grabbing last 4 chars of filename AKA the type
    const fileType = e.target.value.slice(e.target.value.length - 5);
    if (!fileType === ".json") {
      alert("Input only accepts JSON files.");
    }
  };

  return (
    <div className="upload-container">
      <input
        ref={fileInput}
        type="file"
        id="fetch-config-button"
        accept="application/JSON"
        onChange={(event) => {
          fileChange(event);
          props.fetchConfig(event);
        }}
      />

      <label
        className="button-generic config-label"
        htmlFor="fetch-config-button"
        title="Upload Settings"
      >
        <i className="fas fa-file-upload"></i>
      </label>
    </div>
  );
}

export default ConfigUpload;
