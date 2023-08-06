// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { useState, useEffect } from "react";
import CircularProgress from "@material-ui/core/CircularProgress";

const StatusDiv = (props) => {
  if (props.channel.running !== "none") {
    return <CircularProgress size={35} title="Running Process" />;
  } else if (props.channel.success) {
    return <i className="far fa-check-circle" title="Process Complete"></i>;
  } else if (props.channel.error) {
    return <i className="fas fa-exclamation-circle" title="Error"></i>;
  }
  return <i title="Idle"></i>;
};

function Buttons(props) {
  const [running, setRunning] = useState(props.channel.running !== "none");

  useEffect(() => {
    setRunning(props.channel.running !== "none");
  }, [props.channel.running]);

  return (
    <div className="buttons-div">
      <StatusDiv channel={props.channel} />
      <button
        disabled={running}
        className="button-generic"
        id={"preview-button-" + props.formId}
        title="Generate Sample"
        onClick={(event) => {
          if (!props.isValid(props.formId)) {
            alert("Please select all options.");
          } else {
            props.changeChannelState(
              props.formId,
              ["running", "success", "error"],
              ["sample", false, false]
            );
            props.runModel(event, "preview", props.formId);
          }
        }}
      >
        <i className="fas fa-vial" />
      </button>

      <button
        disabled={running}
        className="button-generic"
        id={"run-button-" + props.formId}
        title="Run"
        onClick={(event) => {
          if (!props.isValid(props.formId)) {
            alert("Please select all options.");
          } else {
            props.changeChannelState(
              props.formId,
              ["running", "success", "error"],
              ["full", false, false]
            );
            props.runModel(event, "main", props.formId);
          }
        }}
      >
        <i className="far fa-play-circle"></i>
      </button>

      <button
        disabled={running}
        className="button-generic"
        id={"download-button-" + props.formId}
        title="Download Output"
        onClick={(event) => {
          if (props.channel.taskId === "") {
            alert("No output to download. Run test first.");
          } else {
            props.downloadFile(event, props.formId);
          }
        }}
      >
        <i className="fas fa-download" />
      </button>
    </div>
  );
}

export default Buttons;
